from sqlalchemy.future import select
from db_manager.db import SessionLocal
from db_manager.models import Task, TaskContent
import random

async def select_task(topic: str = None, difficulty: str = None):
    async with SessionLocal() as session:
        query = select(Task).join(TaskContent)
        if topic:
            query = query.filter(Task.topic == topic)
        if difficulty:
            query = query.filter(Task.difficulty == difficulty)
        result = await session.execute(query)
        tasks = result.scalars().all()
        if not tasks:
            return None
        return random.choice(tasks)

async def get_task_content(task_id: int):
    async with SessionLocal() as session:
        query = select(TaskContent).where(TaskContent.task_id == task_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()