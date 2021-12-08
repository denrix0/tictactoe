import tkinter
from board import Board

tk = tkinter.Tk()

board = Board()

tk.title("GAME")
tk.geometry("110x150")
tk.resizable(0, 0)

btns = []
btn_labels = [tkinter.StringVar() for i in range(9)]

def b_clicked(btn):
    sym = board.click_check(btn.get(), btn_labels.index(btn))
    if sym == '':
        for i in btn_labels:
                    i.set('')
    else:
        btn.set(sym)
        txt.set(board.bottom_text)


row = 0
col = 0

for i in range(9):
        if col==3: row += 1
        if i in (3, 6): col = 0 
        btns.append(tkinter.Button(tk, bg='white', fg='black', height=2, width=4, textvariable=btn_labels[i]))
        btns[i].config(command=lambda btn=btn_labels[i]: b_clicked(btn) )
        btns[i].grid(row=row, column=col)
        col += 1

txt = tkinter.StringVar()

txt.set(board.bottom_text)

tkinter.Label(textvariable=txt).grid(row=4, columnspan=3)

tk.mainloop()
