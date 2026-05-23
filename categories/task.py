from keyboard import KeyboardManager
from .base import BaseHandler



class TaskHandler(BaseHandler):
    def __init__(self, db, waiting, bot):
        super().__init__(db, waiting, bot)

        self.task = {}
        self.state = {}
        self.tasks_map = {}
    
        self.actions = {
            'menu': self.handle_menu,
            'add': self.handle_add,
            'control': self.handle_control,
            'history': self.handle_history,
            'del': self.handle_del,
            'edit': self.handle_edit,
            'done': self.handle_done,
        }

        self.state_handle = {
            'title': self.title_task_input,
            'task_priority': self.priority_task_input,
            'delete': self.delete_task_input,
        }

    def handler(self, user_id, peer_id, message_id, action):
        handle_action = self.actions.get(action)
        if handle_action:
            handle_action(user_id, peer_id, message_id)
        else:
            print('Неизвестное действие')
       

    def handle_menu(self, user_id, peer_id, message_id):
        self.bot.edit_message(peer_id, message_id, 'Меню задач', KeyboardManager.get_task_menu())
    
    def handle_add(self, user_id, peer_id, message_id):
        self.bot.send_message(user_id, 'Опишите задачу')
        self.state[user_id] = 'title'
        self.waiting.insert_waiting(user_id, 'task')

    def handle_control(self, user_id, peer_id, message_id):
        message = self.show_tasks(user_id)
        self.bot.send_message(user_id, message, KeyboardManager.get_task_control_menu())

    def handle_history(self, user_id, peer_id, message_id):
        self.bot.send_message(user_id, 'История выполненных', KeyboardManager.get_task_control_menu())

    def handle_del(self, user_id, peer_id, message_id):
        self.bot.send_message(user_id, 'Укажи номер задачи которую хочешь удалить')
        self.state[user_id] = 'delete'
        self.waiting.insert_waiting(user_id, 'task')
    
    def handle_edit(self, user_id, peer_id, message_id):
        pass

    def handle_done(self, user_id, peer_id, message_id):
        pass

    def handler_waiting(self, user_id, text):
        state = self.state[user_id]
        handle_state = self.state_handle.get(state)

        if not handle_state:
            print('Неизвестное состояние')
            return
        
        if not handle_state(user_id, text):
            return
    
    def delete_task_input(self, user_id, text):
        error, number = self.valid_delete_input(user_id, text)

        if error:
            self.bot.send_message(user_id, error)
            return False
        
        delete_task_id = self.tasks_map[user_id][number]
        self.db.delete_task(user_id, delete_task_id)
        self.bot.send_message(user_id, 'Задача успешно удалена') 
        
    def valid_delete_input(self, user_id, text):
        error = None
        if not self.is_digit(text, allow_zero=False):
            error = 'Укажите числом!'
            return (error, None)
        num = float(text)
        if not num.is_integer():
            error = 'Число должно быть целым!'
            return (error, None)
        if num > len(self.tasks_map[user_id]):
            error = 'Такого номера нет в списке!'
            return (error, None)
        return (error, int(text))


    def title_task_input(self, user_id, text):
        error, task = self.valid_task_text_input(text)

        if error:
            self.bot.send_message(user_id, error)
            return False
            
        self.task[user_id] = task
        self.state[user_id] ='task_priority'
        self.bot.send_message(user_id, 'Укажите приоритет\nПриоритет указывается цифрой от 0 до 2!') 
        return True
    
    def priority_task_input(self, user_id, text):
        error, priority = self.valid_task_priority_input(text)

        if error:
            self.bot.send_message(user_id, error)
            return False
            
        task_text = self.task[user_id]
        self.db.add_task(user_id, task_text, priority)
        self.state.pop(user_id, None)
        self.waiting.clean_waiting(user_id)

        message = self.form_response(task_text, priority)
        self.bot.send_message(user_id, message)
        return True

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
        if not self.is_digit(text, allow_zero=False):
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
        return self.form_tasks_message(user_id, tasks)
    
    def form_tasks_message(self,  user_id, tasks):
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