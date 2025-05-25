import logging
from typing import Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass

import asyncpg
from asyncpg import Record
from asyncpg.pool import Pool

logger = logging.getLogger(__name__)


@dataclass
class UserProgress:
    progress_id: int
    user_id: int
    task_id: int
    is_completed: bool
    score: int
    last_attempt_date: datetime


class ProgressTracker:
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def get_user_progress(self, user_id: int) -> Dict[int, UserProgress]:
        """Получает весь прогресс пользователя по всем заданиям"""
        query = """
            SELECT progress_id, user_id, task_id, is_completed, score, last_attempt_date
            FROM user_progress
            WHERE user_id = $1
        """
        async with self.db_pool.acquire() as conn:
            records = await conn.fetch(query, user_id)

        progress = {}
        for record in records:
            progress[record['task_id']] = UserProgress(
                progress_id=record['progress_id'],
                user_id=record['user_id'],
                task_id=record['task_id'],
                is_completed=record['is_completed'],
                score=record['score'],
                last_attempt_date=record['last_attempt_date']
            )
        return progress

    async def update_progress(
            self,
            user_id: int,
            task_id: int,
            is_completed: bool,
            score: int
    ) -> Optional[UserProgress]:
        """Обновляет или создает запись о прогрессе пользователя"""
        query = """
            INSERT INTO user_progress (user_id, task_id, is_completed, score)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (user_id, task_id)
            DO UPDATE SET
                is_completed = EXCLUDED.is_completed,
                score = EXCLUDED.score,
                last_attempt_date = NOW()
            RETURNING progress_id, user_id, task_id, is_completed, score, last_attempt_date
        """
        try:
            async with self.db_pool.acquire() as conn:
                record = await conn.fetchrow(
                    query, user_id, task_id, is_completed, max(0, min(100, score))

                if record:
                    return UserProgress(
                        progress_id=record['progress_id'],
                        user_id=record['user_id'],
                        task_id=record['task_id'],
                        is_completed=record['is_completed'],
                        score=record['score'],
                        last_attempt_date=record['last_attempt_date']
                    )
        except Exception as e:
            logger.error(f"Error updating progress for user {user_id}: {e}")
            raise

    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Получает статистику пользователя: выполненные задания, средний балл"""
        query = """
            SELECT 
                COUNT(*) as total_tasks,
                SUM(CASE WHEN is_completed THEN 1 ELSE 0 END) as completed_tasks,
                AVG(score) as avg_score,
                MAX(last_attempt_date) as last_activity
            FROM user_progress
            WHERE user_id = $1
        """
        async with self.db_pool.acquire() as conn:
            record = await conn.fetchrow(query, user_id)

        return {
            'total_tasks': record['total_tasks'] or 0,
            'completed_tasks': record['completed_tasks'] or 0,
            'avg_score': round(float(record['avg_score'] or 0), 2),
            'last_activity': record['last_activity']
        }

    async def reset_progress(self, user_id: int, task_id: Optional[int] = None) -> bool:
        """Сбрасывает прогресс по конкретному заданию или всем заданиям"""
        try:
            async with self.db_pool.acquire() as conn:
                if task_id:
                    await conn.execute(
                        "DELETE FROM user_progress WHERE user_id = $1 AND task_id = $2",
                        user_id, task_id
                    )
                else:
                    await conn.execute(
                        "DELETE FROM user_progress WHERE user_id = $1",
                        user_id
                    )
            return True
        except Exception as e:
            logger.error(f"Error resetting progress for user {user_id}: {e}")
            return False