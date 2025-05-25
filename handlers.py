from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tasks.task_selector import select_task, get_task_content
from db_manager.db import SessionLocal
from db_manager.models import UserProgress
from datetime import datetime

user_task_map = {}

async def handle_get_task(message: types.Message, state: FSMContext):
    task = await select_task(topic="алгебра", difficulty="medium")
    if not task:
        await message.answer("Нет доступных заданий.")
        return
    content = await get_task_content(task.task_id)
    if content is None:
        await message.answer("Задание не найдено.")
        return
    user_task_map[message.from_user.id] = (task.task_id, content.answer_text.strip().lower() if content.answer_text else "")
    msg = f"<b>Задание по теме:</b> {task.topic}\n<b>Уровень:</b> {task.difficulty}\n"
    if content.question_text:
        msg += f"\n{content.question_text}"
    await message.answer(msg)

async def handle_answer(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_input = message.text.strip().lower()
    if user_id not in user_task_map:
        await message.answer("Сначала получите задание с помощью команды /task")
        return
    task_id, correct_answer = user_task_map[user_id]
    is_correct = user_input == correct_answer
    score = 100 if is_correct else 0
    async with SessionLocal() as session:
        progress = UserProgress(
            user_id=user_id,
            task_id=task_id,
            is_completed=True,
            score=score,
            last_attempt_date=datetime.utcnow()
        )
        session.add(progress)
        await session.commit()
    result_msg = "✅ Верно!" if is_correct else f"❌ Неверно. Правильный ответ: {correct_answer}"
    await message.answer(result_msg)
    user_task_map.pop(user_id, None)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_get_task, commands=["task"])
    dp.register_message_handler(handle_answer, state=None)