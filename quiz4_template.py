# Финальный код на сессиях, с формами и шаблонами
# 


from random import randint, shuffle
from flask import Flask, session, redirect, url_for, request, render_template
from db_scripts3 import get_question_after, get_quises, check_answer
import os

folder = os.getcwd() # запомнили текущую рабочую папку



def start_quis(quiz_id):
    '''создаёт нужные значения в словаре session'''
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0
 
def end_quiz():    
    session['quiz'] = -1



def save_answers():
    '''получает данные из формы, проверяет, верен ли ответ, записывает итоги в сессию'''
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    # этот вопрос уже задан:
    session['last_question'] = quest_id
    # увеличиваем счетчик вопросов:
    session['total'] += 1
    # проверить, совпадает ли ответ с верным для этого id
    if check_answer(quest_id, answer):
        session['answers'] += 1




def index():
    ''' Первая страница: если пришли запросом GET, то выбрать викторину, 
    если POST - то запомнить id викторины и отправлять на вопросы'''
    if request.method == 'GET':
        # викторина не выбрана, сбрасываем id викторины и показываем форму выбора
        start_quis(-1)
        q_list = get_quises()
        return render_template('start.html', q_list=q_list)
    else:
        # получили дополнительные данные в запросе! Используем их:
        quest_id = request.form.get('quiz') # выбранный номер викторины 
        if quest_id:
            start_quis(quest_id)
            return redirect(url_for('test'))
        else:
            print("ERROR - ошибка запроса")
            return redirect(url_for('index'))
            

def test():    
    '''возвращает страницу вопроса'''
    # что если пользователь без выбора викторины пошел сразу на адрес '/test'? 
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        #если ответ
        if request.method == 'POST':
            save_answers()
        # 
        result = get_question_after(session['last_question'], session['quiz'])
        if result is None or len(result) == 0:
            return redirect(url_for('result'))
        else:
            # если нам пришли данные, то их надо прочитать и обновить информацию:
            #session['last_question'] = result[0]            
            l = list(result[2:])
            shuffle(l)            
            return render_template('test.html', 
                                id=result[0], 
                                q=result[1],
                                ans_list=l)
        


def result():
    
    html = render_template('result.html', right=session['answers'] or '0', total=session['total'] or '0')
    end_quiz()
    return html

# Создаём объект веб-приложения:
app = Flask(__name__, static_folder=folder, template_folder=folder) 

app.add_url_rule('/', 'index', index, methods=['GET','POST'])   # создаёт правило для URL '/'
app.add_url_rule('/test', 'test', test,  methods=['GET','POST']) # создаёт правило для URL '/test'
app.add_url_rule('/result', 'result', result) # создаёт правило для URL '/test'

@app.errorhandler(404)
def page_not_found(e):
    #snip
    return render_template('404.html')

# Устанавливаем ключ шифрования:
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

if __name__ == '__main__':
   # Запускаем веб-сервер:
   app.run(debug=True)
   
