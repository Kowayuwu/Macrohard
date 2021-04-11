import tkinter as tk
from tkinter import *
from tkinter import messagebox
import re
import pandas as pd
import os
import sys
import time
from csv import writer


global hotelname
root = Tk()
root.title('NAME')
root.config(bg='dim grey')

# Preset user profile rankings of attributes based on initial survey
# the difference between ranks start small (at 4 here), but the intervals will be reset to be larger as the users logs more personal ratings since they become more representative of thier true preferences
user_profile = {
	'cleaniness': 16,
	'hospitality': 12,
	'location': 8,
	'amenities': 4,
	'ease of booking': 0
}

username = ''
# password = ''

login_frame = LabelFrame(root, bg='grey23')
login_frame.grid(row=0, column=0)
# create login labels
login_label = Label(login_frame, text='LOGIN', bg='grey23', fg='white', font=('Helvetica', 18)) 
login_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
username_label = Label(login_frame, text='Username', bg='grey23', fg='white') 
username_label.grid(row=1, column=0, padx=5, pady=5)
password_label = Label(login_frame, text='Password', bg='grey23', fg='white') 
password_label.grid(row=2, column=0, padx=5, pady=5)

# create login entries
username_entry = Entry(login_frame, width=20)
username_entry.grid(row=1, column=1, padx=5, pady=5)
login_entry = Entry(login_frame, width=20)
login_entry.grid(row=2, column=1, padx=5, pady=5)


# create login button
def login():
	global username
	username = username_entry.get()
	login_frame.destroy()


		# create frame for the right hand side of the program asking for user's personal review
	user_review_frame = LabelFrame(root, text='User Review', padx=10, pady=10, bg='grey23', fg="white")
	user_review_frame.grid(row=0, column=1, padx=15, pady=15)

	leave_review_label = Label(user_review_frame, text='Leave Your Review', bg='grey23', fg='white', font=('Arial', 20))
	leave_review_label.grid(row=0, column=0, columnspan=2, padx=20, pady=15)

	value_for_money_label = Label(user_review_frame, text='Please rate the value for money of the good/service: ', bg='grey23', fg='white')
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
			# user_review_frame.destroy()
			# the LHS frame needs to be destroyed as well
			new_window = Toplevel(bg='grey50')
			new_window.title('Your Review')
			new_window.config(bg='dim grey')

			criteria_frame_location = LabelFrame(new_window, padx=10, pady=10, bg='grey23')
			criteria_frame_location.grid(row=0, column=0, padx=10, pady=10)
			criteria_frame_hospitality = LabelFrame(new_window, padx=10, pady=10, bg='grey23')
			criteria_frame_hospitality.grid(row=0, column=1, padx=10, pady=10)
			criteria_frame_cleaniness = LabelFrame(new_window, padx=10, pady=10, bg='grey23')
			criteria_frame_cleaniness.grid(row=0, column=2, padx=10, pady=10)
			criteria_frame_amenities = LabelFrame(new_window, padx=10, pady=10, bg='grey23')
			criteria_frame_amenities.grid(row=0, column=3, padx=10, pady=10)
			criteria_frame_EoB = LabelFrame(new_window, padx=10, pady=10, bg='grey23')
			criteria_frame_EoB.grid(row=0, column=4, padx=10, pady=10)

			location_prompt = Label(criteria_frame_location, width=25, text='How satisfied were you with the \n location of the hotel?', anchor=W, bg='grey23', fg='white')
			location_prompt.grid(row=0, column=0, padx=5, pady=5)
			hospitality_prompt = Label(criteria_frame_hospitality, width=25, text="How satisfied were you with the \n hotel's hospitality?", anchor=W, bg='grey23', fg='white')
			hospitality_prompt.grid(row=0, column=0, padx=5, pady=5)
			cleaniness_prompt = Label(criteria_frame_cleaniness, width=25, text='How satisfied were you with the \n cleaniness of the hotel?', anchor=W, bg='grey23', fg='white')
			cleaniness_prompt.grid(row=0, column=0, padx=5, pady=5)
			amenities_prompt = Label(criteria_frame_amenities, width=25, text='How satisfied were you with the \n quality and range of amenities?', anchor=W, bg='grey23', fg='white')
			amenities_prompt.grid(row=0, column=0, padx=5, pady=5)
			EoB_prompt = Label(criteria_frame_EoB, width=25, text='How satisfied were you with the \n procedure for booking the hotel?', anchor=W, bg='grey23', fg='white')
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
				Radiobutton(criteria_frame_location, text=level, variable=var1, value=syms, bg='grey23', fg='white', activeforeground='white', activebackground='grey23', selectcolor='grey23').grid(row=row_num, column=0)
				Radiobutton(criteria_frame_hospitality, text=level, variable=var2, value=syms, bg='grey23', fg='white', activeforeground='white', activebackground='grey23', selectcolor='grey23').grid(row=row_num, column=0)
				Radiobutton(criteria_frame_cleaniness, text=level, variable=var3, value=syms, bg='grey23', fg='white', activeforeground='white', activebackground='grey23', selectcolor='grey23').grid(row=row_num, column=0)
				Radiobutton(criteria_frame_amenities, text=level, variable=var4, value=syms, bg='grey23', fg='white', activeforeground='white', activebackground='grey23', selectcolor='grey23').grid(row=row_num, column=0)
				Radiobutton(criteria_frame_EoB, text=level, variable=var5, value=syms, bg='grey23', fg='white', activeforeground='white', activebackground='grey23', selectcolor='grey23').grid(row=row_num, column=0)

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

				optional_review_frame = LabelFrame(new_window, padx=10, pady=10, bg='grey23')
				optional_review_frame.grid(row=0, column=0, padx=10, pady=10)

				review_prompt = Label(optional_review_frame, text='You can choose to write a short review for others to see', bg='grey23', fg='white')
				review_prompt.grid(row=0, column=0, padx=10, pady=10)
				review = Text(optional_review_frame, width=50, height=10, bg='grey70', fg='black', font=('Arial', 11))
				review.grid(row=1, column=0, padx=10, pady=10)

				def finish_review():
					global review_response
					review_response = ''
					if len(review.get("1.0", END)) != 0:
						review_response += review.get("1.0", END)
						print(review_response)
					optional_review_frame.destroy()
					finish_btn.destroy()

					new_window.config(bg='grey23')
					thankyou_label = Label(new_window, text='Thank you\nYour response has been recorded', bg='grey23', fg='white')
					thankyou_label.config(font=('Helvetica', 40))
					thankyou_label.pack()
					sat = {"VS": 5,"S": 4,"N": 3,"U": 2, "VU": 1}
					final_list = [hotel_being_reviewed, username, sat.get(location_sym), sat.get(cleaniness_sym), sat.get(hospitality_sym), sat.get(EoB_sym), sat.get(amenities_sym), review_response]
					print(final_list)
					with open('ratings.csv', 'a') as f_object:
						writer_object = writer(f_object)
						writer_object.writerow(final_list)
						f_object.close()
					return final_list

				finish_btn = Button(optional_review_frame, text='Finish', padx=10, pady=10, bg='grey50', fg='white', command=finish_review)
				finish_btn.grid(row=4, column=0, padx=10, pady=10)

			# create submit button
			submit_btn = Button(new_window, text='Submit', padx=10, pady=10, bg='grey50', fg='white', command=submit_satisfaction)
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

	value_for_money_btn = Button(user_review_frame, text='Submit', bg='grey50', fg='white')
	value_for_money_btn.bind('<Button-1>', rating_input_submit)
	value_for_money_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)





	def select_hotel_focusin(event):
		if select_hotel.get() == 'Hotel Name':
			select_hotel.delete(0, END) 
			select_hotel.config(fg='black')
	def r2_insert_name_focusin(event):
		if r2_insert_name.get() == 'Hotel Name':
			r2_insert_name.delete(0, END) 
			r2_insert_name.config(fg='black')

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
	        selected_msg = Label(user_review_frame, text='You have selected: ' + rel_hotel, bg='grey23', fg='white')
	        selected_msg.grid(row=2, column=0, columnspan=2)
	        global hotel_being_reviewed
	        hotel_being_reviewed = rel_hotel
	    else:
	    	hotel_being_reviewed = 'Sorry, we could not find any similar hotels, please try again'
	    	cannot_find_msg = Label(user_review_frame, text=hotel_being_reviewed, bg='grey23', fg='white')
	    	cannot_find_msg.grid(row=2, column=0, columnspan=2)

	def search_get_review(a):
	    rel_hotel = None
	    max = 0
	    for ind in df.index:
	        match = prepos(a, df, ind)
	        if max < match:
	            max = match
	            rel_hotel = ind

	    if rel_hotel:
	        selected_msg = Label(get_review_frame, text='You have selected: ' + rel_hotel, bg='grey23', fg='white')
	        selected_msg.grid(row=3, column=2, columnspan=2)
	        global hotel_being_reviewed
	        hotel_being_reviewed = rel_hotel
	    else:
	    	hotel_being_reviewed = 'Sorry, we could not find any similar hotels, please try again'
	    	cannot_find_msg = Label(get_review_frame, text=hotel_being_reviewed)
	    	cannot_find_msg.grid(row=3, column=2, columnspan=2)
	    	

	# --------------------can add a user verification option if time permits

	select_hotel = Entry(user_review_frame, width=30, bg='white', fg='black')
	select_hotel.grid(row=1, column=0, padx=5, pady=15)
	select_hotel.config(fg='grey')
	select_hotel.insert(0, 'Hotel Name')
	select_hotel.bind('<FocusIn>', select_hotel_focusin)

	select_hotel_btn = Button(user_review_frame, text='Select Hotel', padx=3, pady=3, command=lambda: search(select_hotel.get()))
	select_hotel_btn.grid(row=1, column=1, pady=30)

	# interface for searching review
	# root2 = Tk()
	# root2.title('Personalized Review')

	get_review_frame = LabelFrame(root, text='Personalized Review', padx=10, pady=101, bg='grey23', fg='white')
	get_review_frame.grid(row=0, column=0, padx=15, pady=15)

	r2_enter_name = Label(get_review_frame, text='Enter Hotel Name: ', width=30, bg='grey23', fg='white')
	r2_enter_name.grid(row=1, column=2)
	r2_insert_name = Entry(get_review_frame, width = 50)
	r2_insert_name.grid(row=2, column=2)
	r2_insert_name.config(fg='grey')
	r2_insert_name.insert(0, 'Hotel Name')
	r2_insert_name.bind('<FocusIn>', r2_insert_name_focusin)

	r2_select_hotel_btn = Button(get_review_frame, text='Select Hotel', padx=3, pady=3, bg='grey50', fg='white', command=lambda: search_get_review(r2_insert_name.get()))
	r2_select_hotel_btn.grid(row=3, column=1)

	def give_rating():
		df = pd.read_csv('ratings.csv')
		df['mean'] = df.mean(axis=1)
		df = df.groupby(by = ['Hotel_Name']).agg({'Location Rating':'mean', 'hospitality':'mean', 'Cleanilness Rating':'mean', 'Facilities Rating':'mean', "Booking":'mean'})
		dic = {}
		dic["Location Rating"]=df.loc[[hotel_being_reviewed],['Location Rating']].iat[0,0]
		dic["hospitality"]=df.loc[[hotel_being_reviewed], ['hospitality']].iat[0,0]
		dic["Cleanilness Rating"]=df.loc[[hotel_being_reviewed], ['Cleanilness Rating']].iat[0,0]
		dic["Facilities Rating"]=df.loc[[hotel_being_reviewed], ['Facilities Rating']].iat[0,0]
		dic["Booking"]=df.loc[[hotel_being_reviewed], ['Booking']].iat[0,0]
		final_give_rating = 0.0
	    # this is a assumption of the user's prioirity, idealy this would be capture from past data and algorithms
		priority = ['Location Rating','hospitality','Facilities Rating','Cleanilness Rating','Booking']
		num_priority = len(priority)
		#the average rating score for a hotel with their every aspects score in user priority order 
		rating_in_prio = [0.0]*num_priority
		for i in range(0,num_priority):
			rating_in_prio[i] = dic[priority[i]]
			
		for i in range(1,num_priority+1): #the more right in rating_in_prior the more important it is therefore has higher ratio in final rating
			final_give_rating += rating_in_prio[i-1]*2*i
		
	    # showing the final personalized rating for the user
		final_give_rating /= ((i+1)*i)
		showing_num = tk.Label(get_review_frame, text = str(round(final_give_rating, 1)), fg='gold', bg = 'grey23', font=('times','18'))
		showing_num.place(x=265,y=70)
		
	    # get comments about the hotel from the csv  
		df = pd.read_csv('ratings.csv')
		df = df.set_index("Hotel_Name")
		df = df.sort_index()
		df = df.loc[hotel_being_reviewed:hotel_being_reviewed]
	    # show 3 comments, every hotel has at least 3 comments for this database
		comment=df['Comments'].tolist()
		show_comment1 = tk.Label(root, text = comment[0], fg='white', bg = 'grey23', font=('times','12'))
		show_comment1.place(x=260, y=250)
		show_comment2 = tk.Label(root, text = comment[1], fg='white', bg = 'grey23', font=('times','12'))
		show_comment2.place(x=260, y=270)
		show_comment3 = tk.Label(root, text = comment[2], fg='white', bg = 'grey23', font=('times','12'))
		show_comment3.place(x=260, y=290)

	r2_get_rating_btn = Button(get_review_frame, text='Get Personalized Rating', bg='grey50', fg='white', command=lambda: give_rating())
	r2_get_rating_btn.grid(row=4, column=1)

login_btn = Button(login_frame, text='Login', command=login, bg='grey50', fg='white')
login_btn.grid(row=3, column=0, columnspan=2)




mainloop()