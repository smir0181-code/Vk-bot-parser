import sqlite3
from datetime import datetime
import json
from logger import log
from google_sheets import append_row



class DatabaseManager:
    def __init__(self,db_path='bot_data.db'):
        self.db_path=db_path
        self._init_tables=self.init_db()
        
        
        
    def init_db(self):
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        # существующая таблица posts
        c.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                post_id INTEGER PRIMARY KEY,
                title TEXT,
                article TEXT,
                price TEXT,
                post_date TEXT,
                parsed_at TEXT
            )
        ''')
        # новая таблица для очереди комментариев
        c.execute('''
            CREATE TABLE IF NOT EXISTS comments_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                comment_id INTEGER UNIQUE,
                from_id INTEGER,
                text TEXT,
                synced INTEGER DEFAULT 0,
                created_at TEXT,
                comment_date TEXT
            )
        ''')
        self.conn.commit()
        self.conn.close()
        
    def save_post(self,post_id, title, article, price, post_date):
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO posts (post_id, title, article, price, post_date, parsed_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (post_id, title, article, price, post_date, datetime.now().isoformat()))
        self.conn.commit()
        self.conn.close()

    def get_post(self,post_id):
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        c.execute('SELECT title, article, price, post_date FROM posts WHERE post_id = ?', (post_id,))
        row = c.fetchone()
        self.conn.close()
        return row if row else None

    def save_comment_to_queue(self,post_id, comment_id, from_id, text, comment_date):
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        # Проверяем, есть ли уже такой comment_id
        c.execute('SELECT 1 FROM comments_queue WHERE comment_id = ?', (comment_id,))
        if c.fetchone():
            log.info(f"Комментарий {comment_id} уже есть в очереди, пропускаем")
            self.conn.close()
            return
        c.execute('''
            INSERT INTO comments_queue (post_id, comment_id, from_id, text, comment_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (post_id, comment_id, from_id, text, comment_date, datetime.now().isoformat()))
        self.conn.commit()
        self.conn.close()
        log.info(f"Комментарий {comment_id} добавлен в очередь")
    
    def sync_comments_to_sheets(self):
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        # Выбираем несинхронизированные комментарии
        c.execute('''
            SELECT q.id, q.post_id, q.comment_id, q.from_id, q.text, 
                p.title, p.article, p.price, q.comment_date
            FROM comments_queue q
            JOIN posts p ON q.post_id = p.post_id
            WHERE q.synced = 0
            ORDER BY q.comment_date
            LIMIT 10
        ''')
        rows = c.fetchall()
        for row in rows:
            queue_id, post_id, comment_id, from_id, text, title, article, price, comment_date = row
            try:
                row_data = [
                    comment_date,title, article, price,
                    f"https://vk.com/wall-238461188_{post_id}",
                    from_id, text
                ]
                append_row(row_data)  # вызвать Google Sheets API
                # Помечаем как синхронизированный
                c.execute('UPDATE comments_queue SET synced = 1 WHERE id = ?', (queue_id,))
                self.conn.commit()
                log.info(f"Синхронизирован комментарий {comment_id}")
            except Exception as e:
                log.error(f"Ошибка синхронизации комментария {comment_id}: {e}")
                # Не обновляем synced, повторим в следующий раз
        self.conn.close()