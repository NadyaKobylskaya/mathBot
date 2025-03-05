import json
import random

# Список заданий
tasks = [
    {"question": "Найдите значение выражения 15/4 * 6/5.", "answer": "4.5"},
    {"question": "Решите уравнение: 2x + 3 = 9.", "answer": "3"},
    {"question": "Сколько будет 7.5 + 2.5?", "answer": "10"},
]

def handle(data):
    """Функция обработки запроса от SaleBot"""
    try:
        # Если в data есть поле userAnswer, значит, это проверка ответа
        if "userAnswer" in data:
            user_answer = str(data["userAnswer"]).strip()
            correct_answer = str(data["correctAnswer"]).strip()

            if user_answer == correct_answer:
                return json.dumps({"result": "✅ Верно! Отличная работа!"})
            else:
                return json.dumps({"result": "❌ Неверно. Попробуйте ещё раз!"})
        
        # Если userAnswer нет, значит, нужно выдать новое задание
        task = random.choice(tasks)
        return json.dumps({
            "taskQuestion": task["question"],
            "taskAnswer": task["answer"]
        })

    except Exception as e:
        return json.dumps({"error": str(e)})

