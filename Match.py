import tkinter as tk
import sqlite3
from tkinter  import messagebox
from tkinter import OptionMenu

# Create the root window
root = tk.Tk()

# Set the size of the root window to 600x400
root.geometry("600x600")

# Create a label with text
title_label = tk.Label(root, text="Purrfect Match", font=("Helvetica", 24))

# Place the label in the root window
title_label.pack()

global name_entry, form, age_entry, activity_entry, activity_menu, rows

####################################################################################################
# Database Connection
####################################################################################################

# Create a database connection
connection = sqlite3.connect("survey.db")
cursor = connection.cursor()

# Check if the survey table exists
cursor.execute("PRAGMA table_info(survey)")
table_exists = cursor.fetchone()

# Create the survey table if it doesn't exist
if not table_exists:
    cursor.execute("CREATE TABLE survey (name TEXT, age INTEGER)")

# Try to add the activity column to the survey table
try:
    cursor.execute("ALTER TABLE survey ADD COLUMN activity TEXT")
except sqlite3.OperationalError as error:
    # Check if the error was caused by the activity column already existing
    if "duplicate column name" in str(error):
        # The activity column already exists, so we can ignore the error and continue
        pass
    else:
        # The error was caused by something else, so we should raise the error again
        raise error

####################################################################################################
# New Quiz
####################################################################################################

# Define a function that should be called when the button is clicked
def on_new_quiz_click():
    # This function creates and displays the quiz form

    global name_entry, form, age_entry, activity_var, activity_menu

    # Create the form window
    form = tk.Toplevel(root)
    
    # Create a form field
    age_label = tk.Label(form, text="What age animal are you looking for?")
    age_entry = tk.Entry(form)
    activity_label = tk.Label(form, text="What activity level are you looking for?")
    activity_var = tk.StringVar(form)
    activity_var.set("Lazy")  # Set the default value
    activity_menu = tk.OptionMenu(form, activity_var, "Lazy", "Active", "Hyper")
    
    # Create a submit button
    submit_button = tk.Button(form, text="Submit")
    
    # Place the form field and button in the form window
    age_label.grid(row=0, column=0)
    age_entry.grid(row=0, column=1)
    activity_label.grid(row=1, column=0)
    activity_menu.grid(row=1, column=1)
    submit_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))
    
    # Bind the submit button to a function that handles the form data
    submit_button.bind("<Button-1>", on_new_quiz_submit)
    
    # Show the form
    form.mainloop()

def on_new_quiz_submit(event):
    # This function handles the form data when the submit button is clicked

    global name_entry, form, age_entry, activity_var, activity_menu, rows

    # Get the data from the form field
    age = age_entry.get()
    activity = activity_var.get()
    
    # Query the database for records that match the specified age
    cursor.execute("SELECT name, age, activity FROM survey WHERE age = ? AND activity = ?", (age, activity))

    # Fetch the matching records
    records = cursor.fetchall()

    # If no records were found, display an error message
    if not records:
        messagebox.showwarning("No records found", "Sorry, there are no records that match your search criteria.")

    # Otherwise, display the matching records in the Listbox widget
    else:
        # Clear the Listbox widget
        listbox.delete(0, tk.END)

        # Add the column names to the Listbox widget
        listbox.insert(tk.END, "Name")
        listbox.insert(tk.END, "Age")
        listbox.insert(tk.END, "Activity")

        # Add a separator line to the Listbox widget
        listbox.insert(tk.END, "--------")

        # Add the records to the Listbox widget
        for record in records:
            listbox.insert(tk.END, record[0])
            listbox.insert(tk.END, str(record[1]))
            listbox.insert(tk.END, record[2])

    # Close the form window
    form.destroy()

# Create a button with text
new_quiz_button = tk.Button(root, text="New Quiz", command=on_new_quiz_click, font=("Helvetica", 18) )

# Place the button below the label
new_quiz_button.pack()

####################################################################################################
# Add Animal
####################################################################################################

# Define a function that should be called when the button is clicked
def on_button_click():
    # This function creates and displays the survey form

    global name_entry, form, age_entry, activity_menu, activity_variable
    
    # Create the form window
    form = tk.Toplevel(root)
    
    # Create form fields
    name_label = tk.Label(form, text="Name:")
    name_entry = tk.Entry(form)
    age_label = tk.Label(form, text="Age:")
    age_entry = tk.Entry(form)
    activity_label = tk.Label(form, text="Activity:")
    activity_variable = tk.StringVar(form)
    activity_variable.set("Lazy") # default value
    activity_menu = OptionMenu(form, activity_variable, "Lazy", "Active", "Hyper")
    activity_label.grid(row=2, column=0, pady=(10, 0))
    activity_menu.grid(row=2, column=1)
    
    # Create a submit button
    submit_button = tk.Button(form, text="Submit")
    
    # Place the form fields and button in the form window
    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    age_label.grid(row=1, column=0, pady=(10, 0))
    age_entry.grid(row=1, column=1)
    activity_label.grid(row=2, column=0, pady=(10,0))
    activity_menu.grid(row=2, column=1)
    submit_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))
    
    # Bind the submit button to a function that handles the form data
    submit_button.bind("<Button-1>", on_submit)
    
    # Show the form
    form.mainloop()

def on_submit(event):
    # This function handles the form data when the submit button is clicked

    global name_entry, form, age_entry, activity_variable
    
    # Get the data from the form fields
    name = name_entry.get()
    age = age_entry.get()
    activity = activity_variable.get()
    
    # Add the data to the database
    cursor.execute("INSERT INTO survey (name, age, activity) VALUES (?, ?, ?)", (name, age, activity))
    connection.commit()
    
    # Close the form window
    form.destroy()

    # Update the Listbox widget
    update_listbox()

# Create an add button with text
add_button = tk.Button(root, text="Add Animal", command=on_button_click, font=("Helvetica", 18))

# Place the button below the label
add_button.pack()

####################################################################################################
# Survey Table
####################################################################################################

# Create a Listbox widget in the root window
listbox = tk.Listbox(root, font=("Helvetica", 18))

# Query the database and update the Listbox widget
def update_listbox():

    global name_entry, form, age_entry, rows

    # Clear the Listbox widget
    listbox.delete(0, tk.END)

    # Add the column names to the Listbox widget
    listbox.insert(tk.END, ("Name", "Age", "Activity"))

    # Add padding to the column names
    listbox.insert(tk.END, ("", ""))

    # Query the database
    cursor.execute("SELECT name, age, activity FROM survey")
    rows = cursor.fetchall()

    # Loop through the rows of data and add each row to the Listbox widget
    for row in rows:
        listbox.insert(tk.END, row)

    # Select the first item in the Listbox widget
    listbox.select_set(2)

# Call the update_listbox function to populate the Listbox widget with data
update_listbox()

# Place the Listbox widget in the root window
listbox.pack()

####################################################################################################
# Refresh
####################################################################################################

# Define a function that should be called when the refresh button is clicked
def on_refresh_click():
    # This function updates the Listbox widget to show all records in the survey table

    # Query the database and update the Listbox widget
    update_listbox()

# Create a refresh button
refresh_button = tk.Button(root, text="Refresh", command=on_refresh_click, font=("Helvetica", 18))

# Place the refresh button below the new quiz button
refresh_button.pack()

####################################################################################################
# Edit Animal
####################################################################################################

def on_edit_click(event):
    # This function handles the editing of records

    global name_entry, form, age_entry, activity_menu, activity_label, activity_var

    # Get the selected item in the Listbox widget
    index = listbox.curselection()
    item = listbox.get(index)

    # Get the values for the selected record
    name = item[0]
    age = item[1]
    activity = item[2]

    # Create the form window
    form = tk.Toplevel(root)

    # Create form fields
    name_label = tk.Label(form, text="Name:")
    name_entry = tk.Entry(form)
    name_entry.insert(0, name)
    age_label = tk.Label(form, text="Age:")
    age_entry = tk.Entry(form)
    age_entry.insert(0, age)
    activity_label = tk.Label(form, text="Activity:")
    

    # Create a submit button
    submit_button = tk.Button(form, text="Submit")

    # Create a list of available activities
    activities = ["Lazy", "Active", "Hyper"]

    # Create a Tkinter variable to hold the selected activity
    activity_var = tk.StringVar()

    # Set the value of the Tkinter variable to the current activity
    activity_var.set(activity)

    # Create an OptionMenu widget for the activity
    activity_menu = tk.OptionMenu(form, activity_var, *activities)

    # Place the form fields and button in the form window
    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    age_label.grid(row=1, column=0, pady=(10, 0))
    age_entry.grid(row=1, column=1)
    activity_label.grid(row=2, column=0, pady=(10, 0))
    activity_menu.grid(row=2, column=1)
    submit_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))

    # Bind the submit button to a function that handles the form data
    submit_button.bind("<Button-1>", on_edit_submit)

    # Show the form
    form.mainloop()

def on_edit_submit(event):
    # This function handles the form data when the submit button is clicked

    global name_entry, form, age_entry, activity_menu, activity_var

    # Get the data from the form fields
    new_name = name_entry.get()
    new_age = age_entry.get()
    new_activity = activity_var.get()

    # Get the selected item in the Listbox widget
    index = listbox.curselection()
    item = listbox.get(index)

    # Get the values for the selected record
    old_name = item[0]
    old_age = item[1]
    old_activity = item[2]

    # Update the database with the new values
    cursor.execute("UPDATE survey SET name = ?, age = ?, activity = ? WHERE name = ? AND age = ? AND activity = ?", (new_name, new_age, new_activity, old_name, old_age, old_activity))

    # Close the form window
    form.destroy()

    # Update the Listbox widget
    update_listbox()

# Create an edit button
edit_button = tk.Button(root, text="Edit Animal", font=("Helvetica", 20))

# Bind the edit button to a function that handles the editing of records
edit_button.bind("<Button-1>", on_edit_click)

# Place the edit button below the add button
edit_button.pack()

####################################################################################################
# Delete Animal
####################################################################################################

# Define a function that should be called when the "Delete" button is clicked
def on_delete_click():
    # This function handles the deletion of records

    # Get the selected item in the Listbox widget
    index = listbox.curselection()
    item = listbox.get(index)

    # Get the values for the selected record
    name, age, activity = item

    # Ask the user for confirmation before deleting the record
    result = messagebox.askyesno("Confirm", "Are you sure you want to delete this record?")

    if result == True:
        # Delete the record from the database
        cursor.execute("DELETE FROM survey WHERE name = ? AND age = ?", (name, age))
        connection.commit()

        # Update the Listbox widget
        update_listbox()

# Create a button with text
delete_button = tk.Button(root, text="Delete Animal", command=on_delete_click, font=("Helvetica", 18) )

# Place the button below the label
delete_button.pack()

# Run the main loop
root.mainloop()


