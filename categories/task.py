from keyboard import KeyboardManager
from .base import BaseHandler


class TaskHandler(BaseHandler):
    def __init__(self, db, waiting, bot):
        super().__init__(db, waiting, bot)
        self.task = {}
        self.task_state = {}
        self.tasks_map = {}

    def handler(self, user_id, peer_id, message_id, action):
        if action == 'menu':
            self.bot.edit_message(peer_id, message_id, 'Меню задач', KeyboardManager.get_task_menu())
        elif action == 'add':
            self.bot.send_message(user_id, 'Опишите задачу')
            self.task_state[user_id] = 'title'
            self.waiting.insert_waiting(user_id, 'task')
        elif action == 'control':
            message = self.show_tasks(user_id)
            self.bot.send_message(user_id, message)

    def handler_waiting(self, user_id, text):
        state = self.task_state[user_id]

        if state == 'title':
            error, task = self.valid_task_text_input(text)

            if error:
                self.bot.send_message(user_id, error)
                return
            
            self.task[user_id] = task
            self.task_state[user_id] ='task_priority'
            self.bot.send_message(user_id, 'Укажите приоритет\nПриоритет указывается цифрой от 0 до 2!') 

        elif state == 'task_priority':
            error, priority = self.valid_task_priority_input(text)

            if error:
                self.bot.send_message(user_id, error)
                return
            
            task_text = self.task[user_id]
            self.db.add_task(user_id, task_text, priority)
            self.task_state.pop(user_id, None)
            self.waiting.clean_waiting(user_id)

            message = self.form_response(task_text, priority)
            self.bot.send_message(user_id, message)      

    def valid_task_text_input(self, text):
        error = None
        if len(text) < 5:
            error = 'Слишком короткая задача'
            return (error, None)
        if not self.is_text(text):
            error = 'Текст задачи не может быть числом'
            return (error, None)
        return (error, text)
    
    def valid_task_priority_input(self, text):
        error = None
        if not self.is_digit(text):
            error = 'Укажите число!'
            return (error, None)
        
        num = float(text)
        if not num.is_integer():
            error = 'Укажите целое число!'
            return (error, None)
        
        if num > 2:
            error = 'Приоритет указывается цифрой от 0 до 2!'
            return (error, None)
        return (error, text)
    
    def form_response(self, task_text, priority):
        message = 'Задача добавлена:\n'
        message += f'Задача: {task_text}, Приоритет: {priority}'
        return message

    def show_tasks(self, user_id):
        tasks = self.db.get_tasks(user_id)
        return self.form_tasks_message(tasks, user_id)
    
    def form_tasks_message(self, tasks, user_id):
        message = 'Поставленные задачи(Вывод в зависимости от приоритета)\n'
        tasks_map = {}

        if not tasks:
            message += 'На данный момент задач нету'
            return message
        
        for i, task in enumerate(tasks, start=1):
            message += f"{i}){task['task_text']}: {task['priority']}-приоритет, {task['time_only']}"
            message += '\n'
            tasks_map[i] = task['id']
        
        self.tasks_map[user_id] = tasks_map
        return message
        

