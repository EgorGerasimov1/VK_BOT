import sqlite3
import os
from contextlib import contextmanager

class DataBase:
    def __init__(self, DATABASE_PATH):
        os.makedirs('data', exist_ok=True) 
        self.db_path = DATABASE_PATH
        self.init_db()

    @contextmanager
    def get_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')

        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init_db(self):
        with self.get_db() as conn:
            #Users
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    user_name TEXT NOT NULL,
                    height REAL,
                    weight REAL,
                    age INTEGER,
                    gender TEXT,
                    goal TEXT,
                    first_seen TIMESTAMP DEFAULT (datetime('now', 'localtime'))
                )
            ''')
            #food
            conn.execute('''
                CREATE TABLE IF NOT EXISTS food (
                    user_id INTEGER NOT NULL,
                    product TEXT NOT NULL,
                    protein REAL NOT NULL,
                    calories REAL NOT NULL,
                    date DATE DEFAULT (date('now', 'localtime')),
                    created_at TIMESTAMP DEFAULT (datetime('now', 'localtime')),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            ''')

            #sport
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sport (
                    user_id INTEGER NOT NULL,
                    estimation INTEGER NOT NULL,
                    condition TEXT NOT NULL
                )
            ''')

            #task
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    task_text TEXT NOT NULL,
                    priority INTEGER DEFAULT 0,
                    done INTEGER DEFAULT 0,
                    date DATE DEFAULT (date('now', 'localtime')),
                    created_at TIMESTAMP DEFAULT (datetime('now', 'localtime')),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            ''')
    # USER + PROFILE
    def add_user(self, user_id, user_info):
        with self.get_db() as conn:
            conn.execute('''
                INSERT OR IGNORE INTO users (user_id, user_name, age, gender)
                VALUES (?,?,?,?)
            ''', (user_id, user_info['name'], user_info['age'], user_info['gender']))

    def get_user_data(self, user_id):
        with self.get_db() as conn:
            cursor = conn.execute('''
                SELECT *
                FROM users
                WHERE user_id = ?
            ''', (user_id,))
            result = cursor.fetchone()
            return result
    
    def get_calculate_data(self, user_id):
        with self.get_db() as conn:
            cursor = conn.execute('''
                SELECT weight, height, age, gender
                FROM users
                where user_id = ?
            ''', (user_id,))
            result = cursor.fetchone()
            return result
        
    def get_user_name(self, user_id):
        with self.get_db() as conn:
            cursor = conn.execute('''
                SELECT user_name
                FROM users
                where user_id = ?
            ''', (user_id,))
            result = cursor.fetchone()
            return result['user_name']

    def edit_profile(self,user_id, height, weight, age):
        with self.get_db() as conn:
            conn.execute('''
                UPDATE users
                SET height = ?, weight = ?, age = ?
                WHERE user_id = ?
            ''', (height, weight, age, user_id))

    # FOOD CATEGORY
    def add_food(self, user_id, product, protein, calories):
        with self.get_db() as conn:
            conn.execute('''
                INSERT INTO food (user_id, product, protein, calories) 
                VALUES (?,?,?,?)
            ''', (user_id, product, protein, calories))

    def get_today_stats_food(self, user_id):
        with self.get_db() as conn:
            cursor = conn.execute('''
                SELECT SUM(protein) AS total_protein, SUM(calories) AS total_calories
                FROM food
                WHERE user_id = ? AND date = date('now', 'localtime')
            ''', (user_id,))
            result = cursor.fetchone()
            return result
        
    def get_today_food(self, user_id):
        with self.get_db() as conn:
            cursor = conn.execute('''
                SELECT product, protein, calories, strftime('%H:%M', created_at) as time_only
                FROM food 
                WHERE user_id = ? AND date = date('now', 'localtime')
                ORDER BY created_at DESC
            ''', (user_id,))
            result = cursor.fetchall()
            return result
    # TASK CATEGORY
    def add_task(self, user_id, task_text, priority):
        with self.get_db() as conn:
            conn.execute('''
                INSERT INTO tasks (user_id, task_text,  priority) 
                VALUES (?,?,?)
            ''', (user_id, task_text, priority))

    def get_tasks(self, user_id):
        with self.get_db() as conn:
            cursor = conn.execute('''
                SELECT id, task_text, priority, strftime('%H:%M', created_at) as time_only
                FROM tasks 
                WHERE user_id = ? 
                ORDER BY priority DESC
            ''', (user_id,))
            result = cursor.fetchall()
            return result
    
    def delete_task(self,user_id, id):
        with self.get_db() as conn:
            conn.execute('''
                DELETE FROM tasks where user_id = ? AND id = ?
            ''', (user_id, id))