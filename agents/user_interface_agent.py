# This is the user interface agent that handles user input collection

import tkinter as tk
from tkinter import messagebox
from agents.time_parser_agent import TimeParserAgent  # Ensure you have this import

class UserInterfaceAgent:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Research Input Collection")

        # Create input fields
        tk.Label(self.root, text="Research Topic:").pack()
        self.entry_topic = tk.Entry(self.root)
        self.entry_topic.pack()

        tk.Label(self.root, text="Days Back:").pack()
        self.entry_days = tk.Entry(self.root)
        self.entry_days.pack()

        # Create a button to submit the input
        tk.Button(self.root, text="Submit", command=self.on_submit).pack()

        # Create a label for notifications
        self.notification_label = tk.Label(self.root, text="", wraplength=300)
        self.notification_label.pack(pady=10)

        # Create a label for completion message
        self.done_label = tk.Label(self.root, text="", wraplength=300)
        self.done_label.pack(pady=10)

        # Create buttons for New Topic and Quit, initially hidden
        self.new_topic_button = tk.Button(self.root, text="New Topic", command=self.reset_gui)
        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_program)

        # Pack buttons but keep them hidden initially
        self.new_topic_button.pack(pady=10)
        self.quit_button.pack(pady=10)
        self.new_topic_button.pack_forget()
        self.quit_button.pack_forget()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close

        # Initialize variables to store input
        self.query_input = None
        self.time_input = None
        self.time_parser = TimeParserAgent()  # Initialize the time parser

    def on_submit(self):
        self.query_input = self.entry_topic.get()
        time_input = self.entry_days.get()

        # Validate and process the input
        if not self.query_input or not time_input:
            self.notification_label.config(text="Please enter both topic and days back.", fg="red")
            return

        # Try to parse the days input
        try:
            days, explanation = self.time_parser.get_days_back(time_input)
            self.time_input = days
        except Exception as e:
            self.notification_label.config(text=str(e), fg="red")
            return

        # Display the topic and time frame back to the user in the same window
        self.notification_label.config(text=f"Searching for articles on '{self.query_input}' from the last {self.time_input} days.", fg="green")

        # Perform the research
        self.perform_research()

    def perform_research(self):
        from agents.manager_agent import ManagerAgent  # Move import here to avoid circular import
        self.manager_agent = ManagerAgent()  # Initialize the ManagerAgent

        # Call the research method from the ManagerAgent
        try:
            self.manager_agent.handle_interaction(self.query_input, self.time_input)
            self.show_completion()
        except Exception as e:
            self.notification_label.config(text=f"Research failed: {str(e)}", fg="red")

    def show_completion(self):
        # Display the "All done!" message
        self.done_label.config(text="All done!", fg="blue")

        # Show the New Topic and Quit buttons
        self.new_topic_button.pack()
        self.quit_button.pack()

        # Optionally, you can disable the input fields and submit button after completion
        self.entry_topic.config(state='disabled')
        self.entry_days.config(state='disabled')

    def reset_gui(self):
        # Reset the GUI for a new topic
        self.entry_topic.config(state='normal')
        self.entry_days.config(state='normal')
        self.entry_topic.delete(0, tk.END)
        self.entry_days.delete(0, tk.END)
        self.notification_label.config(text="", fg="black")
        self.done_label.config(text="", fg="black")

        # Hide the New Topic and Quit buttons
        self.new_topic_button.pack_forget()
        self.quit_button.pack_forget()

    def quit_program(self):
        self.root.destroy()  # Quit the program without further prompting

    def on_closing(self):
        self.root.destroy()  # Quit the program without further prompting

    def run(self):
        self.root.mainloop()  # Start the GUI event loop

    def collect_input(self):
        self.run()  # Start the GUI
        return self.time_input, self.query_input  # Return the collected inputs