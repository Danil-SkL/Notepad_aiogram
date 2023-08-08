import sqlite3 as sq


async def db_connect():
    global db, cur

    db = sq.connect('Note.db')
    cur = db.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS remider(id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT, designer TEXT, time TEXT, date TEXT, confirm INTEGER DEFAULT 0''')
    cur.execute('''CREATE TABLE IF NOT EXISTS note(id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT, designer TEXT)''')
    

    db.commit()


async def get_reminder():
    res = cur.execute('SELECT * FROM remider').fetchall()

    if len(res) > 0:
        return res
    else:
        return 'Нет напоминалок'
    

async def get_note():
    res = cur.execute('SELECT * FROM note').fetchall()

    if len(res) > 0:
        return res
    else:
        return 'Нет заметок'
    

async def add_note(message):
    cur.execute(f"INSERT INTO note(designer) VALUES (?)", (message, ))
    db.commit()


async def del_note(message):
    cur.execute("DELETE FROM note WHERE id=?", (message, ))
    db.commit()


async def add_reminder(message, message1):
    cur.execute('INSERT INTO remider(designer, time) VALUES (?, ?)', (message, message1))
    db.commit()


async def get_remider_time():
    time_list = cur.execute('SELECT id, designer, time, date, confirm FROM remider').fetchall()
    a= []
    for i in time_list:
        a.append(i)

    return a


async def cmd_del_reminder(message):
    cur.execute('DELETE FROM remider WHERE id=?', (message,))
    db.commit()


async def cmd_changes_bool(message_conf, message_id):
    cur.execute('UPDATE remider SET confirm = ? WHERE id = ?', (message_conf, message_id))
    db.commit()
