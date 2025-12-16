from tkinter import *
from tkinter import ttk
from login import Login, Registro
from container import Container


class Manager(Tk):
    def __init__(self, *args, **kwagrs):
        super().__init__(*args, **kwagrs)
        self.title("Mini market v1.0")
        self.geometry("1100x650+120+20")
        self.resizable(False, False)

        container = Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)

        self.frames = {}
        for i in (Login, Registro, Container):
            frame = i(container, self)
            self.frames[i] = frame
            frame.place(x=0, y=0, width=1100, height=650)

        self.show_frame(Login)  

        self.style = ttk.Style()
        self.style.theme_use("clam")

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


if __name__ == "__main__":
    app = Manager()
    app.mainloop()
