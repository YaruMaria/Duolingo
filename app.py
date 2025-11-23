from flask import Flask, render_template, jsonify
from flask import Flask, render_template, jsonify, redirect, url_for
app = Flask(__name__)
from flask import request  # Добавьте этот импорт в начало файла

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

# Добавим в начало файла после game_state
practice_answers = {
    '6': {
        '1': {
            'correct_answers': ['ответ1', 'ответ2', 'ответ3', 'ответ4', 'ответ5', 'ответ6', 'ответ7', 'ответ8', 'ответ9', 'ответ10', 'ответ11', 'ответ12', 'ответ13', 'ответ14', 'ответ15', 'ответ16', 'ответ17'],  # Правильные ответы для 4 изображений
            'user_answers': [None, None, None, None]  # Ответы пользователя
        }
    },
    '7': {
        '1': {
            'correct_answers': ['ответ1', 'ответ2', 'ответ3', 'ответ4', 'ответ5', 'ответ6', 'ответ7', 'ответ8', 'ответ9', 'ответ10'],
            'user_answers': [None] * 10
        }
    },
    # Добавьте аналогично для остальных номеров...
}

# Функция для получения правильных ответов (позже вы их заполните)
def get_correct_answers(task_number, task_id):
    # Здесь будут реальные правильные ответы
    # Пока заглушки
    if task_number == '6':
        return ['1,55', '2,05', '10,1', '10,5', '10,1', '3,3', '1,325', '6,2', '2', '0,5', '9', '0,8', '8', '-0,12', '-6,25','0,7305', '1,875']
    elif task_number == '7':
        return ['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B']
    # Добавьте для остальных номеров...
    return ['ответ'] * 10

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
        'title': 'Мобильный интернет',
        'completed': False,
        'pdf_url': 'https://smallpdf.com/ru/file#s=мобильный-интернет-pdf-link',
        'images': [
            'мобильный_интернет/№1-5_мобильный_интернет_1.jpg', 'мобильный_интернет/№1-5_мобильный_интернет_2.jpg',
            'мобильный_интернет/№1-5_мобильный_интернет_3.jpg', 'мобильный_интернет/№1-5_мобильный_интернет_4.jpg',
            'мобильный_интернет/№1-5_мобильный_интернет_5.jpg', 'мобильный_интернет/№1-5_мобильный_интернет_6.jpg'
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

# 5 тем для №6 (Числа и вычисления)
tasks_6 = [
    {
        'id': 1,
        'number': '№6',
        'title': 'Числа и вычисления',
        'completed': False,
        'pdf_url': 'https://smallpdf.com/ru/file#s=целые-числа-pdf-link',
        'images': [
            '№6/№6_целые_числа_1.jpg',
            '№6/№6_целые_числа_2.jpg',
            '№6/№6_целые_числа_3.jpg',
            '№6/№6_целые_числа_4.jpg'
        ]
    }
]

tasks_7 = [
    {
        'id': 1,
        'number': '№7',
        'title': 'Числовые неравенства, координатная прямая',
        'completed': False,
        'pdf_url': 'https://smallpdf.com/ru/file#s=целые-числа-pdf-link',
        'images': [
            '№7/№7_целые_числа_1.jpg',
            '№7/№7_целые_числа_2.jpg',
            '№7/№7_целые_числа_3.jpg',
            '№7/№7_целые_числа_4.jpg',
            '№7/№7_целые_числа_5.jpg',
            '№7/№7_целые_числа_6.jpg',
            '№7/№7_целые_числа_7.jpg',
            '№7/№7_целые_числа_8.jpg',
            '№7/№7_целые_числа_9.jpg',
            '№7/№7_целые_числа_10.jpg'
        ]
    }
]

tasks_8 = [
    {
        'id': 1,
        'number': '№8',
        'title': 'Числа, вычисления и алгебраические выражения',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№8/№8_целые_числа_1.jpg',
            '№8/№8_целые_числа_2.jpg',
            '№8/№8_целые_числа_3.jpg',
            '№8/№8_целые_числа_4.jpg',
            '№8/№8_целые_числа_5.jpg',
            '№8/№8_целые_числа_6.jpg',
            '№8/№8_целые_числа_7.jpg',
            '№8/№8_целые_числа_8.jpg',
            '№8/№8_целые_числа_9.jpg',
            '№8/№8_целые_числа_10.jpg'
        ]
    }
]

tasks_9 = [
    {
        'id': 1,
        'number': '№9',
        'title': 'Уравнения',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№9/№9_1.png',
            '№9/№9_2.jpg'
        ]
    }
]
tasks_10 = [
    {
        'id': 1,
        'number': '№10',
        'title': 'Теория вероятностей',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№10/№10_1.jpg',
            '№10/№10_2.jpg',
            '№10/№10_3.jpg'
        ]
    }
]

tasks_11 = [
    {
        'id': 1,
        'number': '№11',
        'title': 'Графики функций',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№11/№11_1.jpg',
            '№11/№11_2.jpg',
            '№11/№11_3.jpg',
            '№11/№11_4.jpg',
            '№11/№11_5.jpg',
            '№11/№11_6.jpg',
            '№11/№11_7.jpg',
            '№11/№11_8.jpg',
            '№11/№11_9.jpg'
        ]
    }
]

tasks_12 = [
    {
        'id': 1,
        'number': '№12',
        'title': 'Расчеты по формулам',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№12/№12_1.jpg',
            '№12/№12_2.jpg',
            '№12/№12_3.jpg',
            '№12/№12_4.jpg',
            '№12/№12_5.jpg',
            '№12/№12_6.jpg',
            '№12/№12_7.jpg',
            '№12/№12_8.jpg'
        ]
    }
]

tasks_13 = [
    {
        'id': 1,
        'number': '№13',
        'title': 'Неравенства, системы неравенств',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№13/№13_1.jpg',
            '№13/№13_2.jpg',
            '№13/№13_3.jpg',
            '№13/№13_4.jpg',
            '№13/№13_5.jpg',
            '№13/№13_6.jpg',
            '№13/№13_7.jpg',
            '№13/№13_8.jpg',
            '№13/№13_9.jpg'


        ]
    }
]

tasks_14 = [
    {
        'id': 1,
        'number': '№14',
        'title': 'Прогрессии',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№14/№14_1.jpg',
            '№14/№14_2.png',
            '№14/№14_3.jpg',
            '№14/№14_4.png',
            '№14/№14_5.jpg',
            '№14/№14_6.jpg',
            '№14/№14_7.jpg',
            '№14/№14_8.jpg',
            '№14/№14_9.jpg',
            '№14/№14_10.jpg',
            '№14/№14_11.jpg',
            '№14/№14_12.png',
            '№14/№14_13.jpg',
            '№14/№14_14.jpg',
            '№14/№14_15.png',
            '№14/№14_16.png',
            '№14/№14_17.png'



        ]
    }
]

tasks_15 = [
    {
        'id': 1,
        'number': '№15',
        'title': 'Треугольники',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№15/№15_1.jpg',
            '№15/№15_2.jpg',
            '№15/№15_3.jpg',
            '№15/№15_4.jpg'
        ]
    }
]

tasks_16 = [
    {
        'id': 1,
        'number': '№16',
        'title': 'Окружности',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№16/№16_1.jpg',
            '№16/№16_2.jpg',
            '№16/№16_3.jpg',
            '№16/№16_4.jpg'
        ]
    }
]


tasks_17 = [
    {
        'id': 1,
        'number': '№17',
        'title': 'Четырёхугольники',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№17/№17_1.jpg',
            '№17/№17_2.jpg',
            '№17/№17_3.jpg',
            '№17/№17_4.jpg',
            '№17/№17_5.jpg',
            '№17/№17_6.jpg',
            '№17/№17_7.jpg',
            '№17/№17_8.jpg',
            '№17/№17_9.jpg',
            '№17/№17_10.jpg',
            '№17/№17_11.jpg',
            '№17/№17_12.jpg',
            '№17/№17_13.jpg'


        ]
    }
]

tasks_18 = [
    {
        'id': 1,
        'number': '№18',
        'title': 'Фигуры на клетчатой плоскости',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№18/№18_1.jpg',
            '№18/№18_2.jpg',
            '№18/№18_3.jpg',
            '№18/№18_4.jpg',
            '№18/№18_5.jpg',
            '№18/№18_6.jpg',
            '№18/№18_7.jpg',
            '№18/№18_8.jpg',
            '№18/№18_9.jpg'


        ]
    }
]

tasks_19 = [
    {
        'id': 1,
        'number': '№19',
        'title': 'Анализ геометрических высказываний',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№19/№19_1.jpg',
            '№19/№19_2.jpg',
            '№19/№19_3.jpg'
        ]
    }
]

tasks_20 = [
    {
        'id': 1,
        'number': '№20',
        'title': 'Алгебраические выражения, уравнения, неравенства и их системы',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№20/№20_1.jpg',
            '№20/№20_2.jpg',
            '№20/№20_3.jpg',
            '№20/№20_4.jpg',
            '№20/№20_5.jpg',
            '№20/№20_6.jpg',
            '№20/№20_7.jpg',
            '№20/№20_8.jpg',
            '№20/№20_9.jpg',
            '№20/№20_10.jpg',
            '№20/№20_11.jpg',
            '№20/№20_12.jpg',
            '№20/№20_13.jpg',
            '№20/№20_14.jpg',
            '№20/№20_15.jpg',
            '№20/№20_16.jpg',
            '№20/№20_17.jpg',
            '№20/№20_18.jpg',
            '№20/№20_19.jpg',
            '№20/№20_20.jpg',
            '№20/№20_21.jpg',
            '№20/№20_22.jpg',
            '№20/№20_23.jpg',
            '№20/№20_24.jpg'



        ]
    }
]

tasks_21 = [
    {
        'id': 1,
        'number': '№21',
        'title': 'Текстовые задачи',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№21/№21_1.jpg',
            '№21/№21_2.jpg',
            '№21/№21_3.jpg',
            '№21/№21_4.jpg',
            '№21/№21_5.jpg',
            '№21/№21_6.jpg',
            '№21/№21_7.jpg',
            '№21/№21_8.jpg',
            '№21/№21_9.jpg',
            '№21/№21_10.jpg',
            '№21/№21_11.jpg',
            '№21/№21_12.jpg',
            '№21/№21_13.jpg',
            '№21/№21_14.jpg',
            '№21/№21_15.jpg',
            '№21/№21_16.jpg',
            '№21/№21_17.jpg',
            '№21/№21_18.jpg',
            '№21/№21_19.jpg',
            '№21/№21_20.jpg',
            '№21/№21_21.jpg',
            '№21/№21_22.jpg',
            '№21/№21_23.jpg',
            '№21/№21_24.jpg',
            '№21/№21_25.jpg'

        ]
    }
]

tasks_22 = [
    {
        'id': 1,
        'number': '№22',
        'title': 'Графики функций',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№22/№22_1.jpg',
            '№22/№22_2.jpg',
            '№22/№22_3.jpg',
            '№22/№22_4.jpg',
            '№22/№22_5.jpg',
            '№22/№22_6.jpg',
            '№22/№22_7.jpg',
            '№22/№22_8.jpg',
            '№22/№22_9.jpg',
            '№22/№22_10.jpg',
            '№22/№22_11.jpg',
            '№22/№22_12.jpg',
            '№22/№22_13.jpg',
            '№22/№22_14.jpg'
        ]
    }
]


tasks_23 = [
    {
        'id': 1,
        'number': '№23',
        'title': 'Геометрические задачи на вычисление',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№23/№23_1.jpg',
            '№23/№23_2.jpg',
            '№23/№23_3.jpg'
        ]
    }
]

tasks_24 = [
    {
        'id': 1,
        'number': '№24',
        'title': 'Геометрические задачи на доказательство',
        'completed': False,
        'pdf_url': '№8/№8.jpg',
        'images': [
            '№24/№24_1.jpg',
            '№24/№24_2.jpg',
            '№24/№24_3.jpg'
        ]
    }
]

# Словарь всех задач по номерам
all_tasks = {
    '1-5': tasks_1_5,
    '6': tasks_6,
    '7': tasks_7,
    '8': tasks_8,
    '9': tasks_9,
    '10': tasks_10,
    '11': tasks_11,
    '12': tasks_12,
    '13': tasks_13,
    '14': tasks_14,
    '15': tasks_15,
    '16': tasks_16,
    '17': tasks_17,
    '18': tasks_18,
    '19': tasks_19,
    '20': tasks_20,
    '21': tasks_21,
    '22': tasks_22,
    '23': tasks_23,
    '24': tasks_24,
    # '25': tasks_10
}

def get_task_number(topic_id):
    mapping = {
        1: '1-5',
        2: '6',
        3: '7',
        4: '8',
        5: '9',
        6: '10',
        7: '11',
        8: '12',
        9: '13',
        10: '14',
        11: '15',
        12: '16',
        13: '17',
        14: '18',
        15: '19',
        16: '20',
        17: '21',
        18: '22',
        19: '23',
        20: '24',
        21: '25'
    }
    return mapping.get(topic_id)


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
    return render_template('tasks_1_5.html', tasks=tasks_1_5, topic_number='1-5', topic_title='Группы задач по тексту')


@app.route('/tasks_6')
def tasks_6_page():
    """Страница с задачами №6"""
    return render_template('tasks_1_5.html', tasks=tasks_6, topic_number='6', topic_title='Числа и вычисления')


@app.route('/task_detail/<task_number>/<int:task_id>')
def task_detail(task_number, task_id):
    """Страница с деталями задачи для любого номера"""
    tasks_list = all_tasks.get(task_number)
    if not tasks_list:
        return f"Номер задачи '{task_number}' не найден", 404

    task = next((t for t in tasks_list if t['id'] == task_id), None)
    if task:
        return render_template('task_detail.html', task=task)
    else:
        return f"Задача с ID {task_id} не найдена", 404


@app.route('/topic_detail/<int:topic_id>')
def topic_detail(topic_id):
    """Страница с деталями темы (для №6-№25)"""
    topic = next((t for t in math_topics if t['id'] == topic_id), None)
    if topic:
        # Определяем какой номер задачи показывать
        if topic_id == 1:  # №1-5
            return render_template('tasks_1_5.html',
                                 tasks=tasks_1_5,
                                 topic_number='1-5',
                                 topic_title=topic['title'])
        elif topic_id == 2:  # №6 - сразу открываем первую задачу
            return redirect(url_for('task_detail', task_number='6', task_id=1))
        else:
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


@app.route('/complete_task/<task_number>/<int:task_id>')
def complete_task(task_number, task_id):
    """API: Завершить задачу для любого номера"""
    tasks_list = all_tasks.get(task_number)
    if not tasks_list:
        return jsonify({
            'message': '❌ Номер задачи не найден',
            'action': 'task_number_not_found'
        }), 404

    task = next((t for t in tasks_list if t['id'] == task_id), None)
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

@app.route('/practice_task/25/1')
def practice_task_25():
    """Страница с практическим заданием №25"""
    tasks_list = all_tasks.get('25')
    if not tasks_list:
        return "Номер задачи '25' не найден", 404

    task = next((t for t in tasks_list if t['id'] == 1), None)
    if task:
        correct_answers = get_correct_answers('25', 1)
        return render_template('practice_task.html',
                             task=task,
                             correct_answers=correct_answers,
                             task_number='25')
    else:
        return "Задача с ID 1 не найдена", 404

# Практические задания №6-№25 (отдельные от теории)
practice_tasks_6 = [
    {
        'id': 1,
        'number': '№6',
        'title': 'Числа и вычисления - Практика',
        'completed': False,
        'images': [
            'practice/№6/1.png',
            'practice/№6/2.png',
            'practice/№6/3.png',
            'practice/№6/4.png',
            'practice/№6/5.png',
            'practice/№6/6.png',
            'practice/№6/7.png',
            'practice/№6/8.png',
            'practice/№6/9.png',
            'practice/№6/10.png',
            'practice/№6/11.png',
            'practice/№6/12.png',
            'practice/№6/13.png',
            'practice/№6/14.png',
            'practice/№6/15.png',
            'practice/№6/16.png',
            'practice/№6/17.png'
        ]
    }
]

practice_tasks_7 = [
    {
        'id': 1,
        'number': '№7',
        'title': 'Числовые неравенства, координатная прямая - Практика',
        'completed': False,
        'images': [
            'practice/№7/№7_практика_1.jpg',
            'practice/№7/№7_практика_2.jpg',
            'practice/№7/№7_практика_3.jpg',
            'practice/№7/№7_практика_4.jpg',
            'practice/№7/№7_практика_5.jpg'
        ]
    }
]

# Добавьте аналогично для остальных номеров...
practice_tasks_8 = [
    {
        'id': 1,
        'number': '№8',
        'title': 'Числа, вычисления и алгебраические выражения - Практика',
        'completed': False,
        'images': [
            'practice/№8/№8_практика_1.jpg',
            'practice/№8/№8_практика_2.jpg',
            'practice/№8/№8_практика_3.jpg'
        ]
    }
]

practice_tasks_9 = [
    {
        'id': 1,
        'number': '№9',
        'title': 'Уравнения - Практика',
        'completed': False,
        'images': [
            'practice/№9/№9_практика_1.jpg',
            'practice/№9/№9_практика_2.jpg'
        ]
    }
]

practice_tasks_10 = [
    {
        'id': 1,
        'number': '№10',
        'title': 'Теория вероятностей - Практика',
        'completed': False,
        'images': [
            'practice/№10/№10_практика_1.jpg',
            'practice/№10/№10_практика_2.jpg',
            'practice/№10/№10_практика_3.jpg'
        ]
    }
]

# Словарь практических задач
practice_tasks = {
    '6': practice_tasks_6,
    '7': practice_tasks_7,
    '8': practice_tasks_8,
    '9': practice_tasks_9,
    '10': practice_tasks_10,
    '11': tasks_11,  # Пока используем теорию, потом замените
    '12': tasks_12,
    '13': tasks_13,
    '14': tasks_14,
    '15': tasks_15,
    '16': tasks_16,
    '17': tasks_17,
    '18': tasks_18,
    '19': tasks_19,
    '20': tasks_20,
    '21': tasks_21,
    '22': tasks_22,
    '23': tasks_23,
    '24': tasks_24,
    '25': tasks_21  # Временная заглушка
}

@app.route('/practice_topics')
def practice_topics_page():
    """Страница с темами для практики"""
    return render_template('practice_topics.html', topics=math_topics)

@app.route('/practice_tasks_1_5')
def practice_tasks_1_5_page():
    """Страница с задачами №1-5 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_1_5, topic_number='1-5', topic_title='Группы задач по тексту')

@app.route('/practice_task_detail/<task_number>/<int:task_id>')
def practice_task_detail(task_number, task_id):
    """Страница с деталями задачи для практики"""
    tasks_list = all_tasks.get(task_number)
    if not tasks_list:
        return f"Номер задачи '{task_number}' не найден", 404

    task = next((t for t in tasks_list if t['id'] == task_id), None)
    if task:
        return render_template('practice_task_detail.html', task=task)
    else:
        return f"Задача с ID {task_id} не найдена", 404

@app.route('/complete_practice_task/<task_number>/<int:task_id>')
def complete_practice_task(task_number, task_id):
    """API: Завершить задачу для практики"""
    tasks_list = all_tasks.get(task_number)
    if not tasks_list:
        return jsonify({
            'message': '❌ Номер задачи не найден',
            'action': 'task_number_not_found'
        }), 404

    task = next((t for t in tasks_list if t['id'] == task_id), None)
    if task:
        game_state['gems'] += 15
        return jsonify({
            'message': f'🎉 Практика по задаче "{task["title"]}" завершена! +15 💎',
            'action': 'practice_task_completed',
            'gems': game_state['gems']
        })
    else:
        return jsonify({
            'message': '❌ Задача не найдена',
            'action': 'task_not_found'
        }), 404


@app.route('/empty_task/<task_number>/<int:task_id>')
def empty_task(task_number, task_id):
    """Пустая страница для задач (временно)"""
    tasks_list = all_tasks.get(task_number)
    if not tasks_list:
        return f"Номер задачи '{task_number}' не найден", 404

    task = next((t for t in tasks_list if t['id'] == task_id), None)
    if task:
        return render_template('empty_task.html', task=task)
    else:
        return f"Задача с ID {task_id} не найдена", 404

@app.route('/empty_practice_task/<task_number>/<int:task_id>')
def empty_practice_task(task_number, task_id):
    """Пустая страница для практики (временно)"""
    tasks_list = all_tasks.get(task_number)
    if not tasks_list:
        return f"Номер задачи '{task_number}' не найден", 404

    task = next((t for t in tasks_list if t['id'] == task_id), None)
    if task:
        return render_template('empty_practice_task.html', task=task)
    else:
        return f"Задача с ID {task_id} не найдена", 404


@app.route('/practice_tasks_6')
def practice_tasks_6_page():
    """Страница с задачами №6 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_6, topic_number='6', topic_title='Числа и вычисления')

@app.route('/practice_tasks_7')
def practice_tasks_7_page():
    """Страница с задачами №7 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_7, topic_number='7', topic_title='Числовые неравенства, координатная прямая')

@app.route('/practice_tasks_8')
def practice_tasks_8_page():
    """Страница с задачами №8 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_8, topic_number='8', topic_title='Числа, вычисления и алгебраические выражения')

@app.route('/practice_tasks_9')
def practice_tasks_9_page():
    """Страница с задачами №9 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_9, topic_number='9', topic_title='Уравнения')

@app.route('/practice_tasks_10')
def practice_tasks_10_page():
    """Страница с задачами №10 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_10, topic_number='10', topic_title='Теория вероятностей')

@app.route('/practice_tasks_11')
def practice_tasks_11_page():
    """Страница с задачами №11 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_11, topic_number='11', topic_title='Графики функций')

@app.route('/practice_tasks_12')
def practice_tasks_12_page():
    """Страница с задачами №12 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_12, topic_number='12', topic_title='Расчеты по формулам')

@app.route('/practice_tasks_13')
def practice_tasks_13_page():
    """Страница с задачами №13 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_13, topic_number='13', topic_title='Неравенства, системы неравенств')

@app.route('/practice_tasks_14')
def practice_tasks_14_page():
    """Страница с задачами №14 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_14, topic_number='14', topic_title='Прогрессии')

@app.route('/practice_tasks_15')
def practice_tasks_15_page():
    """Страница с задачами №15 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_15, topic_number='15', topic_title='Треугольники')

@app.route('/practice_tasks_16')
def practice_tasks_16_page():
    """Страница с задачами №16 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_16, topic_number='16', topic_title='Окружности')

@app.route('/practice_tasks_17')
def practice_tasks_17_page():
    """Страница с задачами №17 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_17, topic_number='17', topic_title='Четырёхугольники')

@app.route('/practice_tasks_18')
def practice_tasks_18_page():
    """Страница с задачами №18 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_18, topic_number='18', topic_title='Фигуры на клетчатой плоскости')

@app.route('/practice_tasks_19')
def practice_tasks_19_page():
    """Страница с задачами №19 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_19, topic_number='19', topic_title='Анализ геометрических высказываний')

@app.route('/practice_tasks_20')
def practice_tasks_20_page():
    """Страница с задачами №20 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_20, topic_number='20', topic_title='Алгебраические выражения, уравнения, неравенства и их системы')

@app.route('/practice_tasks_21')
def practice_tasks_21_page():
    """Страница с задачами №21 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_21, topic_number='21', topic_title='Текстовые задачи')

@app.route('/practice_tasks_22')
def practice_tasks_22_page():
    """Страница с задачами №22 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_22, topic_number='22', topic_title='Графики функций')

@app.route('/practice_tasks_23')
def practice_tasks_23_page():
    """Страница с задачами №23 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_23, topic_number='23', topic_title='Геометрические задачи на вычисление')

@app.route('/practice_tasks_24')
def practice_tasks_24_page():
    """Страница с задачами №24 для практики"""
    return render_template('practice_tasks_1_5.html', tasks=tasks_24, topic_number='24', topic_title='Геометрические задачи на доказательство')

@app.route('/practice_development/<int:topic_id>')
def practice_development(topic_id):
    """Страница "в разработке" для практики"""
    topic = next((t for t in math_topics if t['id'] == topic_id), None)
    if topic:
        return render_template('practice_development.html', topic=topic)
    else:
        return "Тема не найдена", 404

@app.route('/practice_task/<task_number>/<int:task_id>')
def practice_task(task_number, task_id):
    """Страница с практическим заданием"""
    # Используем отдельные задачи для практики
    tasks_list = practice_tasks.get(task_number)
    if not tasks_list:
        return f"Практика для номера '{task_number}' не найдена", 404

    task = next((t for t in tasks_list if t['id'] == task_id), None)
    if task:
        correct_answers = get_correct_answers(task_number, task_id)
        return render_template('practice_task.html',
                             task=task,
                             correct_answers=correct_answers,
                             task_number=task_number)
    else:
        return f"Задача с ID {task_id} не найдена", 404


@app.route('/complete_practice/<task_number>/<int:task_id>', methods=['POST'])
def complete_practice(task_number, task_id):
    """API: Завершить практику"""
    data = request.json
    user_answers = data.get('answers', [])
    correct_count = data.get('correct_count', 0)
    total_count = data.get('total_count', 0)

    # Начисляем самоцветы
    gems_earned = max(5, correct_count * 2)  # Минимум 5, плюс за правильные ответы
    game_state['gems'] += gems_earned

    return jsonify({
        'message': f'🎉 Практика завершена! Правильно {correct_count} из {total_count}. +{gems_earned} 💎',
        'action': 'practice_completed',
        'gems': game_state['gems'],
        'correct_count': correct_count,
        'total_count': total_count
    })

if __name__ == '__main__':
    app.run(debug=True)