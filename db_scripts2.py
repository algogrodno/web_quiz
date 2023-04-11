# pastebin.com/raw/Ky5vuR8D

import sqlite3
db_name = 'quiz.sqlite'
conn = None
curor = None


def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()


def close():
    cursor.close()
    conn.close()


def do(query):
    cursor.execute(query)
    conn.commit()


def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()
    




def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    res =  cursor.fetchall()
    print(f"-------------------------------------- {table} ---------------------------------")
    for row in res:
        print("  /  ".join(list(map(str,row))) if row else "------")
    close()
    return res


def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')




def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    add_links()
    show_tables()
    
    # Вывод в консоль вопросов квиза номер 2
    print("\n Квиз 2")
    res = get_quiz(2)
    if res:
        for row in res:
            print(row)

    # Вывод в консоль вопроса с id=3, id викторины = 1
    print("\n Квиз 1 вопрос 2")
    print(get_question_after(3, 1))
    
        



# -----------------------------
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')


    do('''CREATE TABLE IF NOT EXISTS quiz (
           id INTEGER PRIMARY KEY,
           name VARCHAR)''')


    do('''CREATE TABLE IF NOT EXISTS question (
               id INTEGER PRIMARY KEY,
               question VARCHAR,
               answer VARCHAR,
               wrong1 VARCHAR,
               wrong2 VARCHAR,
               wrong3 VARCHAR)''')


    do('''CREATE TABLE IF NOT EXISTS quiz_content (
               id INTEGER PRIMARY KEY,
               quiz_id INTEGER,
               question_id INTEGER,
               FOREIGN KEY (quiz_id) REFERENCES quiz (id),
               FOREIGN KEY (question_id) REFERENCES question (id) )''')
    close()


# -----------------------------
def add_questions():
    questions = [
        ('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
        ('Каким станет зелёный утёс, если упадёт в Красное море?', 'Мокрым', 'Красным', 'Не изменится', 'Фиолетовым'),
        ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
        ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако')
    ]
    open()
    cursor.executemany('''
            INSERT INTO question 
            (question, answer, wrong1, wrong2, wrong3) 
            VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close()


# -----------------------------
def add_quiz():
    quizes = [
        ('Своя игра', ),
        ('Кто хочет стать миллионером?', ),
        ('Самый умный', )
    ]
    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()


def add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = """INSERT INTO quiz_content 
        (quiz_id, question_id) 
        VALUES (?,?)"""
    #answer = input("Добавить связь (y / n)?")
    links = [
        (1,1), (1,2), (1,4), (1,6), 
        (2,2), (2,5), (2,3), (2,1), 
        (3,3), (3,6), (3,5), (3,2)
    ]

    for link in links:
        quiz_id = link[0]
        question_id = link[1]
        cursor.execute(query, [quiz_id, question_id])
    
    conn.commit()        
    close()


# -----------------------------
def get_question_after(question_id = 0, quiz_id=1):
    ''' 
        возвращает следующий вопрос после вопроса с переданным id
        для первого вопроса передаётся значение по умолчанию 
    '''
    open()
    query = '''
        SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
        FROM question, quiz_content
        WHERE quiz_content.question_id == question.id
        AND quiz_content.id > ? AND quiz_content.quiz_id == ?
        ORDER BY quiz_content.id '''
    cursor.execute(query, [question_id, quiz_id] )
    result = cursor.fetchone()
    close()
    return result

def get_quiz(quiz_id):
    open()
    query = '''
    SELECT question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM quiz_content
    LEFT  JOIN question ON quiz_content.question_id = question.id 
    WHERE quiz_content.quiz_id = ?
    ORDER BY quiz_content.id '''
    cursor.execute(query, [quiz_id])
    result = cursor.fetchall()        
    close()
    return result


if __name__ == "__main__":
    main()