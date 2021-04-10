from tkinter import *
from tkinter import messagebox

root = Tk()

# create frame for the right hand side of the program asking for user's personal review
user_review_frame = LabelFrame(root, text='User Review', padx=10, pady=10)
user_review_frame.grid(row=0, column=1, padx=15, pady=15)

leave_review_label = Label(user_review_frame, text='Leave Your Review')
leave_review_label.config(font=("Courier", 20))
leave_review_label.grid(row=0, column=0, padx=20, pady=20)

value_for_money_label = Label(user_review_frame, text='Please rate the value for money of the good/service: ')
value_for_money_label.config(font=("Italic", 12))
value_for_money_label.grid(row=1, column=0, padx=10, pady=10)





mainloop()
