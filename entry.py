from tkinter import *

# Create the main window
root = Tk()
root.title("Simple GUI")

# Create an entry widget
e = Entry(root, width=50)
e.pack()
e.insert(0, "Enter Your Name")

# Define a function to handle the button click
def myclick():
    hello = "Hello " + e.get()
    mylabel = Label(root, text=hello)
    mylabel.pack()

# Create a button and attach it to the function
mybutton = Button(root, text="Enter Your Name", command=myclick)
mybutton.pack()

# Start the application
root.mainloop()