# Код который работает уже на сессиях
# Квиз выбирается случайно
# Для каждого пользователя создается уникальная переменная текущий вопрос


# pastebin.com/raw/cJwHciMM
from random import randint
from flask import Flask, session, redirect, url_for
from db_scripts2 import get_question_after
import os

folder = os.getcwd() # запомнили текущую рабочую папку

css_start = """
   display: block;
   background-color: #f3eef4;
   border-radius: 60px;
   color: Purple;
   border: 3px solid;
   font-size: 9em;
   text-decoration: none;
   padding: 30px;
   box-shadow: 14px 20px 20px 4px #614d6f;
   text-shadow: 4px 4px 15px #332b37;
   text-align: center;
   width: 550px;
   height: 180px;
   position: absolute;
   top: 50%;                            
   left: 50%;
   margin: -120px 0 0 -300px;"""


css_end="""
    text-align: center;
    position: absolute;
    top: 50%;                            
    left: 50%;
    margin: -0.5em 0 0 -80px;
"""

css_end2="""      
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    /*transform: translateX(-50%);
    transform: translateY(-50%);*/
"""

html_start = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="style_quiz.css">
        <link rel="shortcut icon" href="favicon.ico" type="image/x-icon">
        <title>Викторина</title>
    </head>
    <body>
"""
html_end="""
    </body>
    </html>
"""

def index():
   max_quiz = 3
   # или если ученик написал get_quiz_count(), то можно её импортировать и указать:
   # max_quiz = get_quiz_count[0] 
   session['quiz'] = randint(1, max_quiz)
   # или если ученик написал get_random_quiz_id(), то можно её импортировать и указать:
   # session['quiz'] = get_random_quiz_id()
   session['last_question'] = 0
   html =  f'{html_start} <a style="{css_start}" href="/test">ТЕСТ {session["quiz"]}</a> {html_end}'
   return html

def test():    
   result = get_question_after(session['last_question'], session['quiz'])
   if result is None or len(result) == 0:
       return redirect(url_for('result'))
   else:
       session['last_question'] = result[0]
       # если мы научили базу возвращать Row или dict, то надо писать не result[0], а result['id']
       return '<h1>' + str(session['quiz']) + '<br>' + str(result) + '</h1>'

def result():
   return f"""
        <H1 style='{css_end2}'>that's all folks!</H1>
        <h5><a href='/'> Еще раз </a></H5>
        """

# Создаём объект веб-приложения:
app = Flask(__name__, static_folder=folder) 

app.add_url_rule('/', 'index', index)   # создаёт правило для URL '/'
app.add_url_rule('/test', 'test', test) # создаёт правило для URL '/test'
app.add_url_rule('/result', 'result', result) # создаёт правило для URL '/test'

# Устанавливаем ключ шифрования:
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

if __name__ == '__main__':
   # Запускаем веб-сервер:
   app.run(debug=True)
