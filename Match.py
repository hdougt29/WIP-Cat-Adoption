import tkinter as tk
import sqlite3
from tkinter  import messagebox

# Create the root window
root = tk.Tk()

# Set the size of the root window to 600x400
root.geometry("600x500")

# Create a label with text
title_label = tk.Label(root, text="Purrfect Match", font=("Helvetica", 24), bg="Dark orange")

# Place the label in the root window
title_label.pack()

global name_entry, form, age_entry

# Create a database connection
connection = sqlite3.connect("survey.db")
cursor = connection.cursor()

# Check if the survey table exists
cursor.execute("PRAGMA table_info(survey)")
table_exists = cursor.fetchone()

# Create the survey table if it doesn't exist
if not table_exists:
    cursor.execute("CREATE TABLE survey (name TEXT, age INTEGER)")

# Define a function that should be called when the button is clicked
def on_button_click():
    # This function creates and displays the survey form

    global name_entry, form, age_entry
    
    # Create the form window
    form = tk.Toplevel(root)
    
    # Create form fields
    name_label = tk.Label(form, text="Name:")
    name_entry = tk.Entry(form)
    age_label = tk.Label(form, text="Age:")
    age_entry = tk.Entry(form)
    
    # Create a submit button
    submit_button = tk.Button(form, text="Submit")
    
    # Place the form fields and button in the form window
    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    age_label.grid(row=1, column=0, pady=(10, 0))
    age_entry.grid(row=1, column=1)
    submit_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))
    
    # Bind the submit button to a function that handles the form data
    submit_button.bind("<Button-1>", on_submit)
    
    # Show the form
    form.mainloop()

def on_submit(event):
    # This function handles the form data when the submit button is clicked

    global name_entry, form, age_entry
    
    # Get the data from the form fields
    name = name_entry.get()
    age = age_entry.get()
    
    # Add the data to the database
    cursor.execute("INSERT INTO survey (name, age) VALUES (?, ?)", (name, age))
    connection.commit()
    
    # Close the form window
    form.destroy()

    # Update the Listbox widget
    update_listbox()

# Create an add button with text
add_button = tk.Button(root, text="Add Animal", command=on_button_click, font=("Helvetica", 18))

# Place the button below the label
add_button.pack()

# Create a Listbox widget in the root window
listbox = tk.Listbox(root, font=("Helvetica", 18))

# Query the database and update the Listbox widget
def update_listbox():

    global name_entry, form, age_entry

    # Clear the Listbox widget
    listbox.delete(0, tk.END)

    # Add the column names to the Listbox widget
    listbox.insert(tk.END, ("Name", "Age"))

    # Add padding to the column names
    listbox.insert(tk.END, ("", ""))

    # Query the database
    cursor.execute("SELECT name, age FROM survey")
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

def on_edit_click(event):
    # This function handles the editing of records

    global name_entry, form, age_entry

    # Get the selected item in the Listbox widget
    index = listbox.curselection()
    item = listbox.get(index)

    # Get the values for the selected record
    name = item[0]
    age = item[1]

    # Create the form window
    form = tk.Toplevel(root)

    # Create form fields
    name_label = tk.Label(form, text="Name:")
    name_entry = tk.Entry(form)
    name_entry.insert(0, name)
    age_label = tk.Label(form, text="Age:")
    age_entry = tk.Entry(form)
    age_entry.insert(0, age)

    # Create a submit button
    submit_button = tk.Button(form, text="Submit")

    # Place the form fields and button in the form window
    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    age_label.grid(row=1, column=0, pady=(10, 0))
    age_entry.grid(row=1, column=1)
    submit_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))

    # Bind the submit button to a function that handles the form data
    submit_button.bind("<Button-1>", on_edit_submit)

    # Show the form
    form.mainloop()

def on_edit_submit(event):
    # This function handles the form data when the submit button is clicked

    global name_entry, form, age_entry

    # Get the data from the form fields
    name = name_entry.get()
    age = age_entry.get()

    # Update the database with the new values
    cursor.execute("UPDATE survey SET name = ?, age = ? WHERE name = ?", (name, age, name))
    connection.commit()

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

# Define a function that should be called when the "Delete" button is clicked
def on_delete_click():
    # This function handles the deletion of records

    # Get the selected item in the Listbox widget
    index = listbox.curselection()
    item = listbox.get(index)

    # Get the values for the selected record
    name, age = item

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

