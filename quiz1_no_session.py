# Код который работает еще без сессий
# Квиз выбирается случайно
# Для всех пользователей одна и таже переменная текущий вопрос


# Здесь будет код веб-приложенияfrom random import randint
from flask import Flask, session, redirect, url_for
from db_scripts2 import get_question_after
from random import randint

quiz = 0
last_question = 0

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

def index():
   global quiz, last_question
   max_quiz = 3
   # или если ученик написал get_quiz_count(), то можно её импортировать и указать:
   # max_quiz = get_quiz_count[0] 
   quiz = randint(1, max_quiz)
   # или если ученик написал get_random_quiz_id(), то можно её импортировать и указать:
   # session['quiz'] = get_random_quiz_id()
   last_question = 0
   return f'<a style="" href="/test">ТЕСТ {quiz}</a>'


def test():    
   global last_question
   result = get_question_after(last_question, quiz)
   if result is None or len(result) == 0:   
           return redirect(url_for('result'))


   else:
       last_question = result[0]
       # если мы научили базу возвращать Row или dict, то надо писать не result[0], а result['id']
       return '<h1>' + str(quiz) + '<br>' + str(result) + '</h1>'

def result():
   return "<h1>that's all folks!</h1>"
   

# Создаём объект веб-приложения:
app = Flask(__name__)  
app.add_url_rule('/', 'index', index)   # создаёт правило для URL '/'
app.add_url_rule('/test', 'test', test) # создаёт правило для URL '/test'
app.add_url_rule('/result', 'result', result) # создаёт правило для URL '/test'

if __name__ == '__main__':
    app.run()