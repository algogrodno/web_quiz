# Код работает на адресной строке
# чтобы показать определенный квиз нужно добавить его номер к главной странице через /
# например http://127.0.0.1:5000/2/ - показать квиз №2
# чтобы показать определенный вопрос из определенного квиза нужно  
#       через / указать сначала номер квиза, затем еще рез / номер вопроса
# например http://127.0.0.1:5000/2//3 - показать квиз №2 вопрос №3
#
#

from flask import Flask
import db_scripts2 as db

app = Flask(__name__)

@app.route("/")
def hello_world():    
    html = ""
    res = db.show('question')
    for row in res:
        html += f"<p class='qst'> {'  /  '.join(list(map(str,row)))} </p>"
    return html

@app.route("/<quiz>/")
def get_quiz(quiz): 
    
    if not quiz.isdigit(): return ""
    html = f"<h1> ВЫБРАН КВИЗ №{quiz} </h1>"
    print(f"quiz = {quiz}")
    res = db.get_quiz(int(quiz))
    if res:
        for row in res:
            html += f"<p class='qst'> {'  /  '.join(list(map(str,row)))} </p>"
    else:
        html = "<h2> НЕТ ДАННЫХ </h2>"
    
    return html

@app.route("/<quiz>/<q>/")
def get_question(quiz, q):    
    if not quiz.isdigit() or not q.isdigit(): return ""
    html = f"<h1> ВЫБРАН КВИЗ №{quiz} ВОПРРОС №{q}</h1>"
    res = db.get_question_after(int(quiz), int(q))
    if res:
        for row in res[1:]:
            html += f"<p> {row} </p>"
    else:
        html = "<h2> НЕТ ДАННЫХ </h2>"
    
    return html    
app.run() 