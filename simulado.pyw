from tkinter import *
import time
from matplotlib.pyplot import Figure as Fig
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Model(object):
    def __init__(self):
        self.question_number = 90
        self.questions_done = 0
        self.total_time = 300
        self.master = Tk()
        self.start_point = 0
        self.memo = [(0, 0)]

    def store(self, question, total):
        self.question_number = question
        self.total_time = total
        self.master.destroy()
        self.master = Tk()
        self.master.title('Stats')
        self.master.attributes("-topmost", True)
        self.start_point = time.time()
        running()


model = Model()
model.master.title('Stats ')
model.master.attributes("-topmost", True)


def main():
    time_text = Label(model.master, text='Time(in minutes): ')
    question_txt = Label(model.master, text='Question number:')

    time_text.grid(row=0, column=0)
    question_txt.grid(row=1, column=0)

    time_entry = Entry(model.master)
    question_entry = Entry(model.master)

    time_entry.grid(row=0, column=1)
    question_entry.grid(row=1, column=1)

    button = Button(model.master, text='OK',
                    command=lambda: model.store(question_entry.get(), time_entry.get()), width=10)
    button.grid(row=2, column=0, columnspan=2)
    for i in range(2):
        model.master.grid_columnconfigure(i, weight=1, uniform='foo')

    model.master.mainloop()


def running():
    hour_label = Label(model.master, font=('Courier', 44))
    minute_label = Label(model.master, font=('Courier', 44))

    def tick():
        actual_point = time.time()
        time_passed = actual_point - model.start_point
        time_left = 60 * int(model.total_time) - int(time_passed)
        if time_left <= 0:
            while len(model.memo) <= int(model.question_number):
                model.memo.append((0, model.memo[-1][1]))
            model.master.destroy()
            model.master = Tk()
            model.master.title('Stats')
            model.master.attributes("-topmost", True)
            graph()
        hour = str(round(time_left // 60 // 60))
        if len(hour) == 1:
            hour = '0' + hour

        minute = str(round(time_left // 60 % 60))
        if len(minute) == 1:
            minute = '0' + minute
        hour_label.config(text=hour)
        minute_label.config(text=minute)
        minute_label.after(60000, tick)
        tfq = round(time_left / (int(model.question_number) - model.questions_done))
        time_for_question.config(text=('Remaining time per question:' + str(tfq // 60) + 'm' + str(tfq % 60) + 's'))

    def do():
        actual_point = time.time()
        time_passed = actual_point - model.start_point
        if model.questions_done < int(model.question_number):
            model.questions_done += 1
            model.memo.append((int(time_passed) - int(model.memo[-1][1]), int(time_passed)))
        if model.questions_done == int(model.question_number):
            model.master.destroy()
            model.master = Tk()
            model.master.title('Stats')
            model.master.attributes("-topmost", True)
            graph()
        qd.config(text=('Questions done: ' + str(model.questions_done)))
        pqd.config(text=(str(round(100 * model.questions_done / int(model.question_number), 1)) + '%'))
        tpq = round(time_passed / model.questions_done)
        time_per_question.config(text=('Average time per question: ' + str(tpq // 60) + 'm' + str(tpq % 60) + 's'))

    def undo():
        actual_point = time.time()
        time_passed = actual_point - model.start_point
        if model.questions_done > 0:
            model.questions_done -= 1
            model.memo.remove(model.memo[-1])
        qd.config(text=('Questions done: ' + str(model.questions_done)))
        pqd.config(text=(str(round(100 * model.questions_done / int(model.question_number), 1)) + '%'))
        try:
            tpq = round(time_passed / model.questions_done)
            time_per_question.config(text=('Average time per question: ' + str(tpq // 60) + 'm' + str(tpq % 60) + 's'))
        except ZeroDivisionError:
            time_per_question.config(text=('Average time per question: ' + '0'))

    hour_label.grid()
    minute_label.grid(row=0, column=1)

    do_question = Button(model.master, text='Do question', width=15, height=5, command=do)
    do_question.grid(row=1, column=0)

    undo_question = Button(model.master, text='Undo question', width=15, height=5, command=undo)
    undo_question.grid(row=1, column=1)

    qd = Label(model.master, text='Questions done: 0')
    qd.grid(row=2, column=0)

    pqd = Label(model.master, text='0%')
    pqd.grid(row=2, column=1)

    time_per_question = Label(model.master, text='Average time per question: 0')
    time_per_question.grid(row=3, column=0)

    time_for_question = Label(model.master)
    time_for_question.grid(row=3, column=1)

    tick()
    model.master.mainloop()


def graph():
    data = {'Question': [x for x in range(1, int(model.question_number) + 1)],
            'Time spent': [x[0] for x in model.memo][1:]}
    df = DataFrame(data)
    figure = Fig()
    ax = figure.add_subplot()
    ax.set_facecolor("black")
    bar = FigureCanvasTkAgg(figure, model.master)
    bar.get_tk_widget().grid()
    df = df[['Question', 'Time spent']].groupby('Question').sum()
    df.plot(kind='line', legend=True, ax=ax, color='orange')
    ax.set_title('Time per question')
    model.master.mainloop()


main()
