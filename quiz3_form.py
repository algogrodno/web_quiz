from random import randint
from flask import Flask, session, redirect, url_for, request
from db_scripts3 import get_question_after, get_quises
import os

folder = os.getcwd() # запомнили текущую рабочую папку


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
css1 = ""

css2 ="""
    body{
        background-image: url(https://funart.pro/uploads/posts/2021-04/thumbs/1618568260_31-funart_pro-p-oboi-fon-bledno-fioletovii-33.jpg);
    }

    select{
        font-size: 20px; 
        border-radius: 10px; 
        padding: 5px;
        margin-bottom:12px;
        box-shadow: inset #46234e 1px 2px 6px 0px;
        background-color: #eaddf5;
        transition: all 250ms ease-out;
    }
    select:hover{
        /*box-shadow: inset #46234e 1px 2px 6px 0px;*/
        box-shadow: inset #d3d3d3 3px 4px 6px 0px;
        background-color: #f3f0f5;
        

    }

    .but{
        font-size: 20px; 
        border-radius: 10px; 
        padding: 2px 15px 2px 15px;
        background-color: #c785b747;
        transition: all 250ms ease-out;
    }

    .but:hover{
        box-shadow: #46234e 4px 5px 9px 1px;
    }

    form{
        display: block;
        background: linear-gradient(153deg, #e9f2f375 20%, #7531807a);
        border-radius: 30px;   
        border: 3px solid;
        padding: 30px;
        box-shadow: 14px 20px 20px 4px #614d6f;        
        text-align: center;
        width: 300px;
        height: 150px;
        position: absolute;
        top: 50%;                            
        left: 50%;
        margin: -115px 0 0 -180px; 
    }
"""

def start_quis(quiz_id):
    '''создаёт нужные значения в словаре session'''
    session['quiz'] = quiz_id
    session['last_question'] = 0
 
def end_quiz():
    session.clear()


def quiz_form__():
    ''' функция получает список викторин из базы и формирует форму с выпадающим списком'''
    html_beg = '''<html><body><h2>Выберите викторину:</h2><form method="post" action="index"><select name="quiz">'''
    frm_submit = '''<p><input type="submit" value="Выбрать"> </p>'''


    html_end = '''</select>''' + frm_submit + '''</form></body></html>'''
    options = ''' '''
    q_list = get_quises()
    for id, name in q_list:
        option_line = ('''<option value="''' +
                        str(id) + '''">''' +
                        str(name) + '''</option>
                      ''')
        options = options + option_line
    return html_beg + options + html_end


def quiz_form():
    
    options = ''
    q_list = get_quises()
    for id, name in q_list:
        option_line = f'<option value="{id}">{name}</option>'         
        options = options + option_line
        #print(option_line)

    html = f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <title>Викторина</title>
                <style>
                    {""}
                </style>
            </head>
        
            <body>
                
                <form  method="post" action="/">
                    <h2>Выберите викторину:</h2>
                    <select name="quiz">
                        {options}
                    </select>
                    <p><input class="but" type="submit" value="Выбрать"> </p>
                </form>
            </body>
        </html>
        
    """
    return html




def index():
    ''' Первая страница: если пришли запросом GET, то выбрать викторину, 
    если POST - то запомнить id викторины и отправлять на вопросы'''
    if request.method == 'GET':
        # викторина не выбрана, сбрасываем id викторины и показываем форму выбора
        start_quis(-1)
        return quiz_form()
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
        # тут пока старая версия функции:
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

app.add_url_rule('/', 'index', index, methods=['GET','POST'])   # создаёт правило для URL '/'
app.add_url_rule('/test', 'test', test) # создаёт правило для URL '/test'
app.add_url_rule('/result', 'result', result) # создаёт правило для URL '/test'

# Устанавливаем ключ шифрования:
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

if __name__ == '__main__':
   # Запускаем веб-сервер:
   app.run(debug=True)
   
