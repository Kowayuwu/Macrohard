from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import re
import pandas as pd
import os
import sys
import time


root = Tk()
root.title('NAME')

# Preset user profile rankings of attributes based on initial survey
# the difference between ranks start small (at 4 here), but the intervals will be reset to be larger as the users logs more personal ratings since they become more representative of thier true preferences
user_profile = {
	'cleaniness': 16,
	'hospitality': 12,
	'location': 8,
	'amenities': 4,
	'ease of booking': 0
}

# create frame for the right hand side of the program asking for user's personal review
user_review_frame = LabelFrame(root, text='User Review', padx=10, pady=10)
user_review_frame.grid(row=0, column=1, padx=15, pady=15)

leave_review_label = Label(user_review_frame, text='Leave Your Review')
leave_review_label.config(font=("Courier", 20))
leave_review_label.grid(row=0, column=0, columnspan=2, padx=20, pady=15)

value_for_money_label = Label(user_review_frame, text='Please rate the value for money of the good/service: ')
value_for_money_label.config(font=("Italic", 12))
value_for_money_label.grid(row=3, column=0, padx=10, pady=30)


# define bindings for focusin and focus out of entry box
def rating_input_focusin(event):
	if rating_input.get() == 'Enter a number from 1-5':
		rating_input.delete(0, END) 
		rating_input.config(fg='black')


value_for_money_rating = None
def rating_input_submit(event):
	if float(rating_input.get()) >= 1 and float(rating_input.get()) <= 5:
		global value_for_money_rating
		value_for_money_rating = rating_input.get()
		user_review_frame.destroy()
		# the LHS frame needs to be destroyed as well
		criteria_frame_location = LabelFrame(root, padx=10, pady=10)
		criteria_frame_location.grid(row=0, column=0, padx=10, pady=10)
		criteria_frame_hospitality = LabelFrame(root, padx=10, pady=10)
		criteria_frame_hospitality.grid(row=0, column=1, padx=10, pady=10)
		criteria_frame_cleaniness = LabelFrame(root, padx=10, pady=10)
		criteria_frame_cleaniness.grid(row=0, column=2, padx=10, pady=10)
		criteria_frame_amenities = LabelFrame(root, padx=10, pady=10)
		criteria_frame_amenities.grid(row=0, column=3, padx=10, pady=10)
		criteria_frame_EoB = LabelFrame(root, padx=10, pady=10)
		criteria_frame_EoB.grid(row=0, column=4, padx=10, pady=10)

		location_prompt = Label(criteria_frame_location, width=25, text='How satisfied were you with the \n location of the hotel?', anchor=W)
		location_prompt.grid(row=0, column=0, padx=5, pady=5)
		hospitality_prompt = Label(criteria_frame_hospitality, width=25, text="How satisfied were you with the \n hotel's hospitality?", anchor=W)
		hospitality_prompt.grid(row=0, column=0, padx=5, pady=5)
		cleaniness_prompt = Label(criteria_frame_cleaniness, width=25, text='How satisfied were you with the \n cleaniness of the hotel?', anchor=W)
		cleaniness_prompt.grid(row=0, column=0, padx=5, pady=5)
		amenities_prompt = Label(criteria_frame_amenities, width=25, text='How satisfied were you with the \n quality and range of amenities?', anchor=W)
		amenities_prompt.grid(row=0, column=0, padx=5, pady=5)
		EoB_prompt = Label(criteria_frame_EoB, width=25, text='How satisfied were you with the \n procedure for booking the hotel?', anchor=W)
		EoB_prompt.grid(row=0, column=0, padx=5, pady=5)




		# create radiobuttons
		satisfaction_levels = [
			("Very Satisfied", "VS", 1),
			("Satisfied", "S", 2),
			("Neutral", "N", 3),
			("Unsatisfied", "U", 4),
			("Very Unsatisfied", "VU", 5)
		]

		global var1
		global var2
		global var3
		global var4
		global var5
		var1 = StringVar()
		var1.set("VS")
		var2 = StringVar()
		var2.set("VS")
		var3 = StringVar()
		var3.set("VS")
		var4 = StringVar()
		var4.set("VS")
		var5 = StringVar()
		var5.set("VS")

		for level, syms, row_num in satisfaction_levels:
			Radiobutton(criteria_frame_location, text=level, variable=var1, value=syms).grid(row=row_num, column=0)
			Radiobutton(criteria_frame_hospitality, text=level, variable=var2, value=syms).grid(row=row_num, column=0)
			Radiobutton(criteria_frame_cleaniness, text=level, variable=var3, value=syms).grid(row=row_num, column=0)
			Radiobutton(criteria_frame_amenities, text=level, variable=var4, value=syms).grid(row=row_num, column=0)
			Radiobutton(criteria_frame_EoB, text=level, variable=var5, value=syms).grid(row=row_num, column=0)

		# gets all the symbols for whichever radiobutton is selected for each category
		def submit_satisfaction():
			global location_sym
			global hospitality_sym
			global cleaniness_sym
			global amenities_sym
			global EoB_sym
			global location_num
			global hospitality_num
			global cleaniness_num
			global amenities_num
			global EoB_num

			satisfaction_to_number_conversion = {
				"VS": 2,
				"S": 1,
				"N": 0,
				"U": -1, 
				"VU": -2
			}

			location_sym = var1.get()
			hospitality_sym = var2.get()
			cleaniness_sym = var3.get()
			amenities_sym = var4.get()
			EoB_sym = var5.get()

			location_num = satisfaction_to_number_conversion[var1.get()]
			hospitality_num = satisfaction_to_number_conversion[var2.get()]
			cleaniness_num = satisfaction_to_number_conversion[var3.get()]
			amenities_num = satisfaction_to_number_conversion[var4.get()]
			EoB_num = satisfaction_to_number_conversion[var5.get()]

			#updates numerical values of user_profile following data entries
			global user_profile
			user_profile['location'] = user_profile['location'] + abs(location_num)
			user_profile['hospitality'] = user_profile['hospitality'] + abs(hospitality_num)
			user_profile['cleaniness'] = user_profile['cleaniness'] + abs(cleaniness_num)
			user_profile['amenities'] = user_profile['amenities'] + abs(amenities_num)
			user_profile['ease of booking'] = user_profile['ease of booking'] + abs(EoB_num)
				
			# print(user_profile)

# ------------------------- insert values into database and personal profile!


			# new page to write an optional review
			criteria_frame_location.destroy()
			criteria_frame_hospitality.destroy()
			criteria_frame_cleaniness.destroy()
			criteria_frame_amenities.destroy()
			criteria_frame_EoB.destroy()
			submit_btn.destroy()

			optional_review_frame = LabelFrame(root, padx=10, pady=10)
			optional_review_frame.grid(row=0, column=0, padx=10, pady=10)

			review_prompt = Label(optional_review_frame, text='You can choose to write a short review for others to see')
			review_prompt.grid(row=0, column=0, padx=10, pady=10)
			review = Text(optional_review_frame, width=50, height=10)
			review.grid(row=1, column=0, padx=10, pady=10)

			def finish_review():
				global review_response
				review_response = ''
				if len(review.get("1.0", END)) != 0:
					review_response += review.get("1.0", END)
					print(review_response)
				optional_review_frame.destroy()
				finish_btn.destroy()

				thankyou_label = Label(root, text='Thank you\nYour response has been recorded')
				thankyou_label.config(font=('Italic', 40))
				thankyou_label.pack()



			finish_btn = Button(optional_review_frame, text='Finish', padx=10, pady=10, command=finish_review)
			finish_btn.grid(row=4, column=0, padx=10, pady=10)


		# create submit button
		submit_btn = Button(root, text='Submit', padx=10, pady=10, command=submit_satisfaction)
		submit_btn.config(font=("Italic", 11))
		submit_btn.grid(row=1, column=0, columnspan=5)

	# if input was not between 1&5
	else:
		messagebox.showerror("Input Error", "The inputed rating was not between 1 & 5")

rating_input = Entry(user_review_frame, width=22)
rating_input.grid(row=3, column=1, padx=5, pady=5)
rating_input.config(fg='grey')
rating_input.insert(0, 'Enter a number from 1-5')
rating_input.bind('<FocusIn>', rating_input_focusin)
rating_input.bind('<Return>', rating_input_submit)

value_for_money_btn = Button(user_review_frame, text='Submit')
value_for_money_btn.bind('<Button-1>', rating_input_submit)
value_for_money_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)





def select_hotel_focusin(event):
	if select_hotel.get() == 'Hotel Name':
		select_hotel.delete(0, END) 
		select_hotel.config(fg='black')

df = pd.read_csv('ratings.csv',encoding = 'ISO-8859-1')
df['mean'] = df.mean(axis=1)
df = df.groupby(by = ['ï»¿Hotel_Name']).agg({'mean':'mean'})


# search by character comparison
def prepos(contents, df, n_hotel):
    text = re.sub(r'[^a-zA-Z ]', '', contents)
    text = re.sub('\s+',' ', text)
    text = text.lower()
    match = 0
    for char in text:
        found = 0
        for char2 in n_hotel:
            if (char == char2 and found == 0):
                match = match + 1
                found = 1
    if match > 3:
        return match
    else:
        return False


def search(a):
    rel_hotel = None
    max = 0
    for ind in df.index:
        match = prepos(a, df, ind)
        if max < match:
            max = match
            rel_hotel = ind

    if rel_hotel:
        selected_msg = Label(user_review_frame, text='You have selected: ' + rel_hotel)
        selected_msg.grid(row=2, column=0, columnspan=2)
        global hotel_being_reviewed
        hotel_being_reviewed = rel_hotel
    else:
    	hotel_being_reviewed = 'Sorry, we could not find any similar hotels, please try again'
    	cannot_find_msg = Label(user_review_frame, text=hotel_being_reviewed)
    	cannot_find_msg.grid(row=2, column=0, columnspan=2)
    	

# --------------------can add a user verification option if time permits



select_hotel = Entry(user_review_frame, width=30)
select_hotel.grid(row=1, column=0, padx=5, pady=15)
select_hotel.config(fg='grey')
select_hotel.insert(0, 'Hotel Name')
select_hotel.bind('<FocusIn>', select_hotel_focusin)

select_hotel_btn = Button(user_review_frame, text='Select Hotel', padx=3, pady=3, command=lambda: search(select_hotel.get()))
select_hotel_btn.grid(row=1, column=1, pady=30)


mainloop()