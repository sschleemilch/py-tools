from os import path
import sys
sys.path.append(path.join(path.dirname(path.abspath(__file__)), '..', '..', 'lib'))

from lib.log import get_logger
from lib.json_database import JSONDatabase
from item import TodoItem

LOGGER = get_logger()


class TodoDatabase(JSONDatabase):

    @staticmethod
    def get_template():
        json_database_template = {}
        json_database_template['todos'] = []
        json_database_template['todos-done'] = []
        return json_database_template

    def __init__(self):
        super().__init__('todos', TodoDatabase.get_template())

    def add_todo_item(self, todo_item, done=False):
        if self.todo_item_exists(todo_item) and not done:
            LOGGER.warning("Todo item '" + todo_item.content + "' already exists. Not adding item again.")
        else:
            if done:
                LOGGER.debug("Moving todo item to done")
            else:
                LOGGER.debug("Adding new todo item.")
            todo_entry = {}
            todo_entry['content'] = todo_item.content
            todo_entry['date_created'] = str(todo_item.date_created)
            todo_entry['date_due'] = str(todo_item.date_due)
            if done:
                todo_entry['date_done'] = str(todo_item.date_done)
                self.data['todos-done'].append(todo_entry)
            else:
                self.data['todos'].append(todo_entry)
            self.save()

    def get_all_todo_items_sorted(self, show_done=False):
        todo_items = []
        if show_done:
            todos = self.data['todos-done']
        else:
            todos = self.data['todos']
        for todo_entry in todos:
            todo_content = todo_entry['content']
            todo_date_created = todo_entry['date_created']
            todo_date_due = todo_entry['date_due']
            if show_done:
                todo_date_done = todo_entry['date_done']
                todo_item = TodoItem(todo_content, todo_date_due, todo_date_created, todo_date_done)
            else:
                todo_item = TodoItem(todo_content, todo_date_due, todo_date_created)
                todo_item.update_remaining_days()

            todo_items.append(todo_item)
        todo_items.sort()
        return todo_items

    def todo_item_exists(self, todo_item):
        for todo_entry in self.data['todos']:
            if todo_item.content == todo_entry['content']:
                return True
        return False

    def update_todo_item(self, todo_item):
        for todo_entry in self.data['todos']:
            if todo_item.content == todo_entry['content']:
                self.data['todos'].remove(todo_entry)
                self.add_todo_item(todo_item)

    def delete_todo_item(self, todo_item):
        if self.todo_item_exists(todo_item):
            for todo_entry in self.data['todos']:
                if todo_item.content == todo_entry['content']:
                    self.add_todo_item(todo_item, done=True)
                    self.data['todos'].remove(todo_entry)
                    self.save()
