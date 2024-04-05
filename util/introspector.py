from tkinter import Tk, END, E, W, ttk, StringVar, BooleanVar, NORMAL, DISABLED, Text, Event
from tkinter.ttk import Treeview, Style

from db.db_entities import DBProgram


class TreeApp:
    def __init__(self):
        self.window = Tk()
        self.window.title("Introspector")
        self.window.state("zoomed")
        style = Style()
        style.theme_use("vista")
        self.tree = Treeview(self.window)

    def run(self, program: DBProgram):
        self.add_item("", program)
        self.tree.pack(fill="both", expand=True)
        self.window.mainloop()

    def add_item(self, parent, node):
        item = self.tree.insert(parent, END, text=node.__class__.__name__)
        for attr_name, attr_value in node.__dict__.items():
            self.tree.insert(item, END, text=attr_name + ': ' + str(attr_value))


if __name__ == "__main__":
    app = TreeApp()
    app.run(DBProgram())

