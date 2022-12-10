import tkinter as tk
import sqlite3

# Create the root window
root = tk.Tk()

global name_entry, form, age_entry

# Create a label with text
label = tk.Label(root, text="Purrfect Match")

# Place the label in the root window
label.pack()

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

# Create a button with text
button = tk.Button(root, text="Add cat", command=on_button_click)

# Place the button below the label
button.pack()

# Create a Listbox widget in the root window
listbox = tk.Listbox(root)

# Query the database and update the Listbox widget
def update_listbox():

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

# Call the update_listbox function to populate the Listbox widget with data
update_listbox()

# Place the Listbox widget in the root window
listbox.pack()

# Run the main loop
root.mainloop()
