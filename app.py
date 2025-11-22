from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Храним состояние игры
game_state = {
    'hearts': 3,
    'gems': 150,
    'current_level': 4,
    'levels': [
        {'number': 1, 'title': 'Новая тема', 'type': 'book', 'completed': True, 'locked': False, 'stars': 3, 'xp': 20},
        {'number': 2, 'title': 'Решение задач', 'type': 'brain', 'completed': True, 'locked': False, 'stars': 3,
         'xp': 25},
        {'number': 3, 'title': 'Практика', 'type': 'practice', 'completed': True, 'locked': False, 'stars': 2,
         'xp': 30},
        {'number': 4, 'title': 'Самостоятельная работа', 'type': 'test', 'completed': False, 'locked': False,
         'stars': 0, 'xp': 35},
        {'number': 5, 'title': 'Повторение', 'type': 'repeat', 'completed': False, 'locked': True, 'stars': 0,
         'xp': 40},
        {'number': 6, 'title': 'Экзамен', 'type': 'exam', 'completed': False, 'locked': True, 'stars': 0, 'xp': 45}
    ]
}

# 21 тема для сетки ОГЭ
math_topics = [
    {'id': 1, 'number': '№1-5', 'title': 'Группы задач по тексту', 'completed': False},
    {'id': 2, 'number': '№6', 'title': 'Числа и вычисления', 'completed': False},
    {'id': 3, 'number': '№7', 'title': 'Числовые неравенства, координатная прямая', 'completed': False},
    {'id': 4, 'number': '№8', 'title': 'Числа, вычисления и алгебраические выражения', 'completed': False},
    {'id': 5, 'number': '№9', 'title': 'Уравнения', 'completed': False},
    {'id': 6, 'number': '№10', 'title': 'Теория вероятностей', 'completed': False},
    {'id': 7, 'number': '№11', 'title': 'Графики функций', 'completed': False},
    {'id': 8, 'number': '№12', 'title': 'Расчеты по формулам', 'completed': False},
    {'id': 9, 'number': '№13', 'title': 'Неравенства, системы неравенств', 'completed': False},
    {'id': 10, 'number': '№14', 'title': 'Прогрессии', 'completed': False},
    {'id': 11, 'number': '№15', 'title': 'Треугольники', 'completed': False},
    {'id': 12, 'number': '№16', 'title': 'Окружности', 'completed': False},
    {'id': 13, 'number': '№17', 'title': 'Четырёхугольники', 'completed': False},
    {'id': 14, 'number': '№18', 'title': 'Фигуры на клетчатой плоскости', 'completed': False},
    {'id': 15, 'number': '№19', 'title': 'Анализ геометрических высказываний', 'completed': False},
    {'id': 16, 'number': '№20', 'title': 'Алгебраические выражения, уравнения, неравенства и их системы',
     'completed': False},
    {'id': 17, 'number': '№21', 'title': 'Текстовые задачи', 'completed': False},
    {'id': 18, 'number': '№22', 'title': 'Графики функций', 'completed': False},
    {'id': 19, 'number': '№23', 'title': 'Геометрические задачи на вычисление', 'completed': False},
    {'id': 20, 'number': '№24', 'title': 'Геометрические задачи на доказательство', 'completed': False},
    {'id': 21, 'number': '№25', 'title': 'Геометрические задачи повышенной сложности', 'completed': False}
]

# 7 тем для №1-5 с разными PDF и изображениями
tasks_1_5 = [
    {
        'id': 1,
        'number': '№1-5',
        'title': 'Дороги',
        'completed': False,
        'pdf_url': 'https://smallpdf.com/ru/file#s=97ea26c5-15dd-4208-b3e1-fba2ac976378',
        'images': [
            'дороги/№1-5_дороги_1.jpg', 'дороги/№1-5_дороги_2.jpg', 'дороги/№1-5_дороги_3.jpg',
            'дороги/№1-5_дороги_4.jpg', 'дороги/№1-5_дороги_5.jpg', 'дороги/№1-5_дороги_6.jpg',
            'дороги/№1-5_дороги_7.jpg', 'дороги/№1-5_дороги_8.jpg', 'дороги/№1-5_дороги_9.jpg',
            'дороги/№1-5_дороги_10.jpg', 'дороги/№1-5_дороги_11.jpg', 'дороги/№1-5_дороги_12.jpg',
            'дороги/№1-5_дороги_13.jpg'
        ]
    },
    {
        'id': 2,
        'number': '№1-5',
        'title': 'Квартиры',
        'completed': False,
        'pdf_url': 'https://smallpdf.com/ru/file#s=квартиры-pdf-link',
        'images': [
            'квартиры/№1-5_квартиры_1.jpg', 'квартиры/№1-5_квартиры_2.jpg', 'квартиры/№1-5_квартиры_3.jpg',
            'квартиры/№1-5_квартиры_4.jpg', 'квартиры/№1-5_квартиры_5.jpg', 'квартиры/№1-5_квартиры_6.jpg',
            'квартиры/№1-5_квартиры_7.jpg'
        ]
    },
    {
        'id': 3,
        'number': '№1-5',
        'title': 'Участки',
        'completed': False,
        'pdf_url': 'https://smallpdf.com/ru/file#s=участки-pdf-link',
        'images': [
            'участки/№1-5_участки_1.jpg', 'участки/№1-5_участки_2.jpg', 'участки/№1-5_участки_3.jpg',
            'участки/№1-5_участки_4.jpg', 'участки/№1-5_участки_5.jpg', 'участки/№1-5_участки_6.jpg'
        ]
    },
    {
    'id': 4,
    'number': '№1-5',
    'title': 'Печи',
    'completed': False,
    'pdf_url': 'https://smallpdf.com/ru/file#s=печи-pdf-link',
    'images': [
        'печи/№1-5_печи_1.jpg', 'печи/№1-5_печи_2.jpg', 'печи/№1-5_печи_3.jpg', 'печи/№1-5_печи_4.jpg'
    ]
},
    {
        'id': 5,
        'number': '№1-5',
        'title': 'Бумага',
        'completed': False,
        'pdf_url': 'https://smallpdf.com/ru/file#s=бумага-pdf-link',
        'images': [
            'бумага/№1-5_бумага_1.jpg', 'бумага/№1-5_бумага_2.jpg', 'бумага/№1-5_бумага_3.jpg',
            'бумага/№1-5_бумага_4.jpg'
        ]
    },
    {
        'id': 6,
        'number': '№1-5',
        'title': 'мобильный_интернет',
        'completed': False,
        'pdf_url': 'https://smallpdf.com/ru/file#s=мобильный-интернет-pdf-link',
        'images': [
            'мобильный_интернет/№1-5_мобильный_интернет_1.jpg',
            'мобильный_интернет/№1-5_мобильный_интернет_2.jpg',
            'мобильный_интернет/№1-5_мобильный_интернет_3.jpg',
            'мобильный_интернет/№1-5_мобильный_интернет_4.jpg',
            'мобильный_интернет/№1-5_мобильный_интернет_5.jpg',
            'мобильный_интернет/№1-5_мобильный_интернет_6.jpg'
        ]
    },
    {
        'id': 7,
        'number': '№1-5',
        'title': 'Шины',
        'completed': False,
        'pdf_url': 'https://smallpdf.com/ru/file#s=шины-pdf-link',
        'images': [
            'шины/№1-5_шины_1.jpg', 'шины/№1-5_шины_2.jpg', 'шины/№1-5_шины_3.jpg',
            'шины/№1-5_шины_4.jpg'
        ]
    }
]


@app.route('/')
def index():
    """Главная страница с уровнями"""
    module_data = {
        'title': 'Модуль 3: Математика ОГЭ',
        'progress': 75,
        'hearts': game_state['hearts'],
        'gems': game_state['gems'],
        'levels': game_state['levels']
    }
    return render_template('index.html', **module_data)


@app.route('/math_topics')
def math_topics_page():
    """Страница со всеми темами ОГЭ"""
    return render_template('math_topics.html', topics=math_topics)


@app.route('/tasks_1_5')
def tasks_1_5_page():
    """Страница с задачами №1-5"""
    return render_template('tasks_1_5.html', tasks=tasks_1_5)


@app.route('/task_detail/<int:task_id>')
def task_detail(task_id):
    """Страница с деталями задачи (для №1-5)"""
    task = next((t for t in tasks_1_5 if t['id'] == task_id), None)
    if task:
        return render_template('task_detail.html', task=task)
    else:
        return "Задача не найдена", 404


@app.route('/topic_detail/<int:topic_id>')
def topic_detail(topic_id):
    """Страница с деталями темы (для №6-№25)"""
    topic = next((t for t in math_topics if t['id'] == topic_id), None)
    if topic:
        return render_template('topic_detail.html', topic=topic)
    else:
        return "Тема не найдена", 404


@app.route('/start_lesson')
def start_lesson():
    """API: Начать урок"""
    return jsonify({
        'message': '🎉 Урок математики начался! Удачи в решении задач!',
        'action': 'lesson_started'
    })


@app.route('/play_level/<int:level_number>')
def play_level(level_number):
    """API: Запустить уровень"""
    level = next((l for l in game_state['levels'] if l['number'] == level_number), None)

    if level and not level['locked']:
        return jsonify({
            'message': f'🚀 Запускаем уровень {level_number}: {level["title"]}',
            'action': 'level_started',
            'level': level_number,
            'title': level['title']
        })
    else:
        return jsonify({
            'message': '❌ Этот уровень заблокирован! Сначала завершите предыдущие.',
            'action': 'level_locked'
        }), 400


@app.route('/complete_level/<int:level_number>')
def complete_level(level_number):
    """API: Завершить уровень"""
    level = next((l for l in game_state['levels'] if l['number'] == level_number), None)

    if level and not level['locked']:
        level['completed'] = True
        level['stars'] = 3
        game_state['gems'] += 10

        # Разблокируем следующий уровень если есть
        if level_number < len(game_state['levels']):
            next_level = game_state['levels'][level_number]
            next_level['locked'] = False

        return jsonify({
            'message': f'🎊 Поздравляем! Уровень {level_number} завершен! +10 💎',
            'action': 'level_completed',
            'gems': game_state['gems']
        })
    else:
        return jsonify({
            'message': '❌ Не удалось завершить уровень',
            'action': 'level_complete_failed'
        }), 400


@app.route('/lose_heart')
def lose_heart():
    """API: Потерять сердце"""
    if game_state['hearts'] > 0:
        game_state['hearts'] -= 1
        return jsonify({
            'message': '💔 Потеряно одно сердце! Будьте внимательнее!',
            'action': 'heart_lost',
            'hearts': game_state['hearts']
        })
    else:
        return jsonify({
            'message': '😵 Закончились сердца! Подождите или купите еще.',
            'action': 'no_hearts'
        }), 400


@app.route('/add_gems')
def add_gems():
    """API: Добавить самоцветы"""
    game_state['gems'] += 5
    return jsonify({
        'message': '💰 +5 самоцветов! Продолжайте в том же духе!',
        'action': 'gems_added',
        'gems': game_state['gems']
    })


@app.route('/complete_topic/<int:topic_id>')
def complete_topic(topic_id):
    """API: Завершить тему"""
    topic = next((t for t in math_topics if t['id'] == topic_id), None)
    if topic:
        topic['completed'] = True
        game_state['gems'] += 15
        return jsonify({
            'message': f'🎉 Тема "{topic["title"]}" завершена! +15 💎',
            'action': 'topic_completed',
            'gems': game_state['gems']
        })
    else:
        return jsonify({
            'message': '❌ Тема не найдена',
            'action': 'topic_not_found'
        }), 404


@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    """API: Завершить задачу"""
    task = next((t for t in tasks_1_5 if t['id'] == task_id), None)
    if task:
        task['completed'] = True
        game_state['gems'] += 10
        return jsonify({
            'message': f'🎉 Задача "{task["title"]}" завершена! +10 💎',
            'action': 'task_completed',
            'gems': game_state['gems']
        })
    else:
        return jsonify({
            'message': '❌ Задача не найдена',
            'action': 'task_not_found'
        }), 404


if __name__ == '__main__':
    app.run(debug=True)