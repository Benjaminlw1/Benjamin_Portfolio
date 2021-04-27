import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title('Staycation and Booking Management')

global dict
dict = {'GM1' : ['Grand Marina', 1, 238], 'GM2' : ['Grand Marina', 2, 398],
'HB1' : ['Hotel Bugis', 1, 168], 'HB2' : ['Hotel Bugis', 2, 300],
'HB3' : ['Hotel Bugis', 3 , 400]}

global bookinglist
bookinglist = []

# Divide into 3 frames
top_frame = tk.Frame(root, width=50, height=100)
middle_frame = tk.Frame(root, width=50, height=10)
bottom_frame = tk.Frame(root, width=50, height=100)
top_frame.grid(row=0)
middle_frame.grid(row=1)
bottom_frame.grid(row=2)

# function to enable fields for booking
def enableBooking():
    E3.configure(state='disabled')
    E4.configure(state='disabled')
    E5.configure(state='disabled')
    E6.configure(state='disabled')
    E1.configure(state='normal')
    E2.configure(state='normal')
    root.update()
# function to enable fields for staycation
def enableStaycation():
    E1.configure(state='disabled')
    E2.configure(state='disabled')
    E3.configure(state='normal')
    E4.configure(state='normal')
    E5.configure(state='normal')
    E6.configure(state='normal')
    root.update()

def onClickAddBtn():
    displayMessage.configure(state='normal')
    # get radiobutton value
    checkRb = var.get()
    # check if radiobutton equal to booking
    if checkRb == 2:
        # check if all fields are not empty
        if E1.get() == "" or E2.get() == "":
            displayMessage.insert(tk.END, 'Please complete all the fields.\n')
        elif E1.get() in dict.keys():
            addlist = []
            # add staycation code into a list
            addlist.append(E1.get())
            # add customer id code into a list
            addlist.append(E2.get())
            bookinglist.append(addlist)
            # clear the entry field
            E1.delete(0, tk.END)
            E2.delete(0, tk.END)
            displayMessage.insert(tk.END, 'Added a booking.\n')
        else:
            displayMessage.insert(tk.END, 'Invalid staycation code.\n')
    # elif radiobutton equal to staycation
    elif checkRb == 3:
        # check if all fields are not empty
        if E3.get() == "" or E4.get() == "" or E5.get() == "" or E6.get() == "":
            displayMessage.insert(tk.END, 'Please complete all the fields.\n')
        # check if staycation code is already inside dictionary
        elif E3.get() in dict.keys():
            displayMessage.insert(tk.END, 'This code belongs to an existing staycation. Check the input.\n')
        # else add all fields into dictionary
        else:
            dictlist = []
            dictlist.append(E4.get())
            dictlist.append(int(E5.get()))
            dictlist.append(int(E6.get()))
            dict[E3.get()] = dictlist
            E3.delete(0, tk.END)
            E4.delete(0, tk.END)
            E5.delete(0, tk.END)
            E6.delete(0, tk.END)
            displayMessage.insert(tk.END, 'Added a staycation.\n')
    else:
        displayMessage.insert(tk.END, 'Select either Booking or Staycation first. \n')

def onClickRemoveBtn():
    displayMessage.configure(state='normal')
    # get radiobutton value
    checkRb = var.get()
    # check if radiobutton equal to booking
    if checkRb == 2:
        if E1.get() == "" or E2.get() == "":
            displayMessage.insert(tk.END, 'Please complete all the fields.\n')
        # check if staycation code is in bookinglist
        elif any(E1.get() in i for i in bookinglist):
            # v is index of a list and i is element inside the nested list
            for v, i in enumerate(bookinglist):
                if i[0] == E1.get() and i[1] == E2.get():
                    bookinglist.remove(bookinglist[v])
                    E1.delete(0, tk.END)
                    E2.delete(0, tk.END)
                    displayMessage.insert(tk.END, 'Removed a booking.\n')
        else:
            displayMessage.insert(tk.END, 'No matching booking to remove. Check the input.\n')
    elif checkRb == 3:
        if E3.get() == "" or E4.get() == "" or E5.get() == "" or E6.get() == "":
            displayMessage.insert(tk.END, 'Please complete all the fields.\n')
        elif E3.get() in dict.keys():
            del dict[E3.get()]
            displayMessage.insert(tk.END, 'Removed a staycation.\n')
        else:
            displayMessage.insert(tk.END, 'No matching staycation to remove. Check the input.\n')

    else:
        displayMessage.insert(tk.END, 'Select either Booking or Staycation first. \n')

def onClickDisplayBtn():
    displayMessage.configure(state='normal')
    checkRb = var.get()
    if checkRb == 2:
        if not bookinglist:
            displayMessage.insert(tk.END, 'No booking currently. \n')
        else:
            for i in bookinglist:
                displayMessage.insert(tk.END, "Staycation code: {0} Customer Id: {1} \n".format(i[0], i[1]))
    elif checkRb == 3:
        for key, values in dict.items():
            if values[1] >= 2:
                displayMessage.insert(tk.END, "Staycation code: {0} {1} {2} nights $ {3} \n".format(key, values[0], values[1], values[2]))
            else:
                displayMessage.insert(tk.END, "Staycation code: {0} {1} {2} night $ {3} \n".format(key, values[0], values[1], values[2]))
    else:
        displayMessage.insert(tk.END, 'Select either Booking or Staycation first. \n')

var = tk.IntVar()
bookingRB = tk.Radiobutton(top_frame, text='Booking', variable=var, value=2, command=enableBooking)
staycationRB = tk.Radiobutton(top_frame, text='Staycation', variable=var, value=3, command=enableStaycation)

# this will arrange entry widgets
bookingRB.grid(row=0, column=0, sticky='W', columnspan=2)
staycationRB.grid(row=0, column=2)


label1 = tk.Label(top_frame, text='Staycation code:', justify='left')
label2 = tk.Label(top_frame, text='Customer Id:', justify='left')
label3 = tk.Label(top_frame, text='Staycation code:', justify='left')
label4 = tk.Label(top_frame, text='Hotel Name:', justify='left')
label5 = tk.Label(top_frame, text='Nights:', justify='left')
label6 = tk.Label(top_frame, text='Cost:$', justify='left')

label1.grid(row=1, column=0, sticky='W', pady=2)
label2.grid(row=2, column=0,  sticky='W', pady=2)
label3.grid(row=1, column=2,  sticky='W', pady=2)
label4.grid(row=2, column=2,  sticky='W', pady=2)
label5.grid(row=3, column=2,  sticky='W', pady=2)
label6.grid(row=4, column=2,  sticky='W', pady=2)

E1 = tk.Entry(top_frame, state='disabled')
E2 = tk.Entry(top_frame, state='disabled')
E3 = tk.Entry(top_frame, state='disabled')
E4 = tk.Entry(top_frame, state='disabled')
E5 = tk.Entry(top_frame, state='disabled')
E6 = tk.Entry(top_frame, state='disabled')

E1.grid(row=1, column=1, sticky='W', pady=2)
E2.grid(row=2, column=1,  sticky='W', pady=2)
E3.grid(row=1, column=3,  sticky='W', pady=2)
E4.grid(row=2, column=3, sticky='W', pady=2)
E5.grid(row=3, column=3,  sticky='W', pady=2)
E6.grid(row=4, column=3,  sticky='W', pady=2)


addBtn = tk.Button(middle_frame, text='Add', width=9, command = onClickAddBtn)
removeBtn = tk.Button(middle_frame, text='Remove', width=9, command =onClickRemoveBtn)
displayBtn = tk.Button(middle_frame, text='Display', width=9, command=onClickDisplayBtn)

# this will arrange button widgets
addBtn.grid(row=0, column=0, sticky='E')
removeBtn.grid(row=0, column=1, sticky='E')
displayBtn.grid(row=0, column=2, sticky='E')

displayMessage = tk.Text(bottom_frame, state='disabled')
displayMessage.grid(row=0,column=0, sticky="nsew")
scroll = ttk.Scrollbar(bottom_frame)
scroll.grid(row=0, column=1, sticky="nse")
scroll.configure(command=displayMessage.yview)
displayMessage.configure(yscrollcommand=scroll.set)

root.mainloop()