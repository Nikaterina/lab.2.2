from flask import Flask
from datetime import datetime
import os

app = Flask(__name__)

weekday = ('Хорошего понедельника!',
           'Хорошего вторника!',
           'Хорошей среды!',
           'Хорошего четверга!',
           'Хорошей пятницы!',
           'Хорошей субботы!',
           'Хорошего воскресенья!'
           )

storage = {}


@app.route("/hello-world/<name>")
def hello_world(name):
    day = datetime.now().weekday()
    return f'Привет, {name}. {weekday[day]}'


@app.route("/max_number/<path:nums>")
def max_nums(nums):
    nums = nums.split('/')
    try:
        nums_int = [int(x) for x in nums]
    except ValueError:
        return 'Ошибка, должны быть только числа!'
    return f'Максимальное число: {max(nums_int)}'


@app.route("/preview/<int:size>/<path:relative_path>")
def head_file(size, relative_path):
    abs_path = os.path.abspath(relative_path)
    with open(abs_path, 'r') as file:
        result_text = file.read(size)
        result_size = len(result_text)
    return f'<b>{abs_path}</b>{result_size}<br>{result_text}'


@app.route("/add/<date>/<int:number>")
def add(date, number):
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:8])
    if check_date(year, month, day):
        storage.setdefault(year, {}).setdefault(month, 0)
        storage[year] [month] += number
        return f'данные записаны! {storage}'
    else:
        return 'Введенная дата некорректна, исправьте!'


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    sum_expense = 0
    try:
        for expense in storage[year].values():
            sum_expense += expense
        return f'Paсходы за {year} год составили: {sum_expense} руб.'
    except KeyError:
        return f'У меня пока нет данных по {year} году'


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    try:
        return (f'Paсходы за {year} год и {month} '
                f'месяц составили: {storage[year] [month]}')
    except KeyError:
        return f'У меня пока нет данных по {year} году и {month} месяцу.'


def check_date(year, month, day):
    """Проверка даты на валидность"""
    try:
        datetime(year, month, day)
        correct_date = True
    except ValueError:
        correct_date = False
    return correct_date


if __name__ == '__main__':
    app.run(debug=True)
