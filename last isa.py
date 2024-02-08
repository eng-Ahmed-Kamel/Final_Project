# This is the final project at SIC.
import tkinter as tk
import json
from tkinter import messagebox,simpledialog,ttk
from PIL import Image, ImageTk  # Pillow library
import copy
import datetime

# Define functions for saving and loading data
def save():
    global data
    file = open("p3.json", "w")
    json.dump(data, file, indent=2)
    file.close()

def loadData():
    try:
        global data
        file = open("p3.json")
        data = json.load(file)
        file.close()
    # To force the creation of the file if it doesn't exist
    except FileNotFoundError:
        save()

def save_threads():
    global threads
    file = open("threads.json", "w")
    json.dump(threads, file, indent=2)
    file.close()

def loadThreads():
    try:
        global threads
        file = open("threads.json")
        threads = json.load(file)
        file.close()
    # To force the creation of the file if it doesn't exist
    except FileNotFoundError:
        save()

# Initialize global data and threads variables, and load data from files
data = []
threads = []
loadData()
loadThreads()

# Define a Stack class for managing threads
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return None if self.isEmpty() else self.items.pop()

    def peek(self):
        return None if self.isEmpty() else self.items[-1]

    def size(self):
        return len(self.items)

# Define the main GUI class
class project_GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1060x530")
        bg = tk.PhotoImage(file="back1.png")
        label1 = tk.Label(self.root, image=bg)
        label1.place(x=0, y=0)
        self.root.title("ZAA Social media platform")
        self.label = tk.Label(text="LOGIN PAGE", font=("comic"))
        self.label.pack(pady=50)
        self.label_email = tk.Label(text="Email")
        global data
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.label_email.pack()
        self.entry = tk.Entry(self.root, textvariable=self.email)
        self.entry.pack()
        self.label_pass = tk.Label(text="password")
        self.label_pass.pack()
        self.entry1 = tk.Entry(self.root, show="*", textvariable=self.password)
        self.entry1.pack()
        self.login_button = tk.Button(self.root, text="login", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.root, text="if you don't have an account 'register'", command=self.register)
        self.register_button.pack()
        self.root.mainloop()

    def login(self):
        for usr in data:
            if usr["Email"] == self.email.get() and usr["Password"] == self.password.get():
                self.root.destroy()
                homepage(usr)  # Pass usr to homepage
                return
        messagebox.showerror("Error", "Email or password may be wrong")

    def register(self):
        self.root.destroy()
        new_account()



class Comment:
    def __init__(self, text, author):
        self.text = text
        self.author = author




# Define the homepage class
class homepage:
    def __init__(self, user_data):
        self.root = tk.Tk()
        self.root.title("Home Page")
        self.root.geometry("1060x530")
        self.usr = user_data

        bg_image = Image.open("back1.png")
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.root, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)

        self.name = self.usr["Username"]
        self.label = tk.Label(self.root, text=f"Welcome, {self.name}", font=("Arial", 15))
        self.label.pack(padx=10, pady=10)

        self.button2 = tk.Button(self.root, text="Log Out", font=("Arial", 15), command=self.goBack)
        self.button2.place(x=0, y=0)
        self.userprofile = tk.Button(self.root, text="User Profile", font=("Arial", 15), command=self.userprofilefunction)
        self.userprofile.place(relx=1.0, rely=0.0, anchor='ne')
        self.add_title = tk.Entry(self.root)
        self.add_title.insert(0, "Add Title")
        self.add_title.pack(padx=10, pady=10)
        self.add_thread = tk.Entry(self.root)
        self.add_thread.insert(0, "Add Thread")
        self.add_thread.pack(padx=10, pady=10)
        self.publishButton = tk.Button(self.root, text="Publish", font=("Arial", 15), command=self.publish)
        self.publishButton.pack(padx=10, pady=10)
        self.search_title = tk.Entry(self.root)
        self.search_title.insert(0, "Search Title")
        self.search_title.pack(padx=10, pady=10)
        self.search_title_button = tk.Button(self.root, text="Search Title", font=("Arial", 15), command=self.search)
        self.search_title_button.pack(padx=10, pady=10)


        self.like = tk.Button(self.root , text = "like" , font=("Arial", 15), command= self.likedpost )
        self.like.pack(padx=10 , pady=10)

        self.chat_messages = []  # Create a list to store chat messages
        self.load_chat()  # Load chat messages from the JSON file
        self.comments = {}

        self.add_comment_button = tk.Button(self.root, text="Add Comment", font=("Arial", 15), command=self.add_comment)
        self.add_comment_button.pack(padx=10, pady=10)



        self.room_bot = tk.Button(self.root, text="Room", command=self.open_room)
        self.room_bot.pack(side=tk.BOTTOM, pady=10)
        global threads
        self.sta = Stack()
        for data in threads:
            self.sta.push(data)

        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.remove_post_button = tk.Button(self.root, text="Remove Post", font=("Arial", 15), command=self.remove_post)
        self.remove_post_button.pack(padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.update_listbox()

        self.root.mainloop()

 

    def search(self):
        max_title_length = 60
        s_title = self.search_title.get()
        if s_title == '':
            messagebox.showerror("Error", "An error occurred: Title is missing")
            return
        for item in self.sta.items:
            title, thread, timestamp, author = item
            if title == s_title:
                messagebox.showinfo("Search Result", f"Author: {author}\nTitle: {title}\nThread: {thread}\nTime_Stamp:{timestamp}")
                return
        messagebox.showerror("Error", "An error occurred: Title not found")
    
    def remove_post(self):
        # Get the currently selected post from the listbox
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            removed_post = self.sta.items.pop(index)
            threads.remove(removed_post)
            
            save_threads()
            self.update_listbox()
        else:
            messagebox.showerror("Error", "Please select a post to remove.")

    def likedpost(self):
            self.like.destroy()
            self.likke = tk.Button(self.root, text="Liked", bg='red' , command= self.back5)
            self.likke.pack(padx=10, pady=10)

    def back5(self):
        self.likke.destroy()
        self.like = tk.Button(self.root, text="Like" , command=self.likedpost)
        self.like.pack()
    
    def add_comment(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if 0 <= index < len(self.sta.items):  # Check if the selected index is valid
                post = self.sta.items[index]

                # Prompt the user for a comment
                comment_text = simpledialog.askstring("Add Comment", "Enter your comment:")
                if comment_text:
                    author = self.usr["Username"]
                    comment = Comment(comment_text, author)

                    # Check if there are already comments for this post
                    if post in self.comments:
                        self.comments[post].append(comment)
                    else:
                        self.comments[post] = [comment]

                    # Update the listbox to display comments
                    self.update_listbox()
            else:
                messagebox.showerror("Error", "Invalid post selection.")
        else:
            messagebox.showerror("Error", "Please select a post to add a comment to.")


    def publish(self):
        title = self.add_title.get()
        thread = self.add_thread.get()

        if title == "" or thread == "":
            messagebox.showerror("Error", "Title or thread are missing")
            return
        messagebox.showinfo(message="you posted this thread")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        post = (title, thread, timestamp, self.usr["Username"])
        threads.append(post)
        save_threads()
        self.sta.push(post)  # Push the post to the stack
        self.update_listbox()

        self.add_title.delete(0, tk.END)
        self.add_title.insert(0, "Add Title")
        self.add_thread.delete(0, tk.END)
        self.add_thread.insert(0, "Add Thread")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        max_title_length = 60
        temp = copy.deepcopy(self.sta)

        while not temp.isEmpty():
            title, thread, timestamp, author = temp.pop()
            spaces = " "
            n = author
            padded_title = f"{spaces:<{max_title_length}}"
            self.listbox.insert(tk.END, f"Author: {n}")
            self.listbox.insert(tk.END, f"Title: {title}")
            self.listbox.insert(tk.END, f"Thread: {thread}")
            self.listbox.insert(tk.END, f"Timestamp: {timestamp}")

            # Display comments if available
            if (title, thread, timestamp, author) in self.comments:
                self.listbox.insert(tk.END, "Comments:")
                for comment in self.comments[(title, thread, timestamp, author)]:
                    self.listbox.insert(tk.END, f"{comment.author}: {comment.text}")

            self.listbox.insert(tk.END, "")

    def goBack(self):
        self.root.destroy()
        project_GUI()

    def userprofilefunction(self):
        profile_window = tk.Toplevel(self.root)
        profile_window.title("User Profile")

        profile_labels = ["Username", "Phone Number", "Email", "Gender", "Governorate", "Age", "National ID"]
        user_info = [self.usr["Username"], self.usr["Phone Number"], self.usr["Email"],
                     self.usr["Gender"], self.usr["Governorate"], self.usr["Age"],
                     self.usr["National ID"]]

        for label, info in zip(profile_labels, user_info):
            label_widget = tk.Label(profile_window, text=f"{label}:")
            label_widget.pack(anchor='w')
            info_widget = tk.Text(profile_window, height=1, width=30)
            info_widget.insert("1.0", info)
            info_widget.config(state="disabled")
            info_widget.pack(anchor='w')

        edit_button = tk.Button(profile_window, text="Edit Profile", command=lambda: self.edit_profile(profile_window))
        edit_button.pack()

    def edit_profile(self, profile_window):
        profile_window.destroy()
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Profile")

        labels = ["Username", "Phone Number", "password", "Governorate", "Age"]

        self.edit_username_var = tk.StringVar()
        self.edit_phone_var = tk.StringVar()
        self.edit_password_var = tk.StringVar()
        self.edit_governorate_var = tk.StringVar()
        self.edit_age_var = tk.StringVar()

        entry_username = tk.Entry(edit_window, textvariable=self.edit_username_var)
        entry_phone = tk.Entry(edit_window, textvariable=self.edit_phone_var)
        entry_password = tk.Entry(edit_window, textvariable=self.edit_password_var)
        entry_governorate = tk.Entry(edit_window, textvariable=self.edit_governorate_var)
        entry_age = tk.Entry(edit_window, textvariable=self.edit_age_var)

        self.edit_username_var.set(self.usr['Username'])
        self.edit_phone_var.set(self.usr['Phone Number'])
        self.edit_password_var.set(self.usr['Password'])
        self.edit_governorate_var.set(self.usr['Governorate'])
        self.edit_age_var.set(self.usr['Age'])

        for label_text, entry_widget in zip(labels,
                                            [entry_username, entry_phone,entry_password , entry_governorate, entry_age]):
            label = tk.Label(edit_window, text=label_text)
            label.pack()
            entry_widget.pack()

        save_button = tk.Button(edit_window, text="Save Changes", command=lambda: self.save_profile(edit_window))
        save_button.pack()

    def save_profile(self, edit_window):
        new_username = self.edit_username_var.get()
        new_phone = self.edit_phone_var.get()
        new_password = self.edit_password_var.get()
        new_governorate = self.edit_governorate_var.get()
        new_age = self.edit_age_var.get()

        self.usr['Username'] = new_username
        self.usr['Phone Number'] = new_phone
        self.usr['Password'] = new_password
        self.usr['Governorate'] = new_governorate
        self.usr['Age'] = new_age

        save()

        tk.messagebox.showinfo("Success", "Profile updated successfully!")

        edit_window.destroy()

    def load_chat(self):
        try:
            with open("chat.json", "r") as chat_file:
                self.chat_messages = json.load(chat_file)
        except FileNotFoundError:
            self.chat_messages = []

    def open_room(self):
        def send_message():
            message = message_entry.get()
            if message:
                author = self.usr["Username"]
                self.chat_messages.append({"author": author, "message": message})
                chat_area.insert(tk.END, f"{author}: {message}\n")
                message_entry.delete(0, tk.END)
                save_chat()  # Save chat after each message

        def save_chat():
            with open("chat.json", "w") as chat_file:
                json.dump(self.chat_messages, chat_file, indent=2)

        room_window = tk.Toplevel(self.root)
        room_window.title("Chat Room")

        chat_area = tk.Text(room_window, height=25, width=65)
        chat_area.pack(padx=10, pady=10)

        for chat in self.chat_messages:
            chat_area.insert(tk.END, f"{chat['author']}: {chat['message']}\n")

        message_entry = tk.Entry(room_window, width=50)
        message_entry.pack(padx=10, pady=10)

        send_button = tk.Button(room_window, text="Send", command=send_message)
        send_button.pack(padx=10, pady=10)

# Define a class for creating a new account
class new_account:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("700x700")
        self.root.title("Register")

        # Variables to store user input
        self.username_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.mail_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.governorate_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.national_id_var = tk.StringVar()

        # Create a centered frame to hold the form elements
        self.center_frame = tk.Frame(self.root)
        self.center_frame.pack(expand=True, pady=20)

        # Create labels and entry fields
        self.label_username = tk.Label(self.center_frame, text="Username:")
        self.label_phone = tk.Label(self.center_frame, text="Phone Number:")
        self.label_mail = tk.Label(self.center_frame, text="Email:")
        self.label_gender = tk.Label(self.center_frame, text="Gender:")
        self.label_governorate = tk.Label(self.center_frame, text="Governorate:")
        self.label_password = tk.Label(self.center_frame, text="Password:")
        self.label_age = tk.Label(self.center_frame, text="Age:")
        self.label_national_id = tk.Label(self.center_frame, text="National ID:")

        self.entry_username = tk.Entry(self.center_frame, textvariable=self.username_var)
        self.entry_phone = tk.Entry(self.center_frame, textvariable=self.phone_var)
        self.entry_mail = tk.Entry(self.center_frame, textvariable=self.mail_var)
        self.entry_governorate = tk.Entry(self.center_frame, textvariable=self.governorate_var)
        self.entry_password = tk.Entry(self.center_frame, show="*", textvariable=self.password_var)  # Password field
        self.entry_age = tk.Entry(self.center_frame, textvariable=self.age_var)
        self.entry_national_id = tk.Entry(self.center_frame, textvariable=self.national_id_var)

        # Create radio buttons for gender
        self.radio_male = tk.Radiobutton(self.center_frame, text="Male", variable=self.gender_var, value="Male")
        self.radio_female = tk.Radiobutton(self.center_frame, text="Female", variable=self.gender_var, value="Female")

        # Create a submit button
        self.submit_button = tk.Button(self.center_frame, text="Submit", command=self.register)

        # Layout using pack
        self.label_username.pack(fill='both', padx=10, pady=5)
        self.entry_username.pack(fill='both', padx=10, pady=5)
        self.label_phone.pack(fill='both', padx=10, pady=5)
        self.entry_phone.pack(fill='both', padx=10, pady=5)
        self.label_mail.pack(fill='both', padx=10, pady=5)
        self.entry_mail.pack(fill='both', padx=10, pady=5)
        self.label_gender.pack(fill='both', padx=10, pady=5)
        self.radio_male.pack(fill='both', padx=10, pady=5)
        self.radio_female.pack(fill='both', padx=10, pady=5)
        self.label_governorate.pack(fill='both', padx=10, pady=5)
        self.entry_governorate.pack(fill='both', padx=10, pady=5)
        self.label_password.pack(fill='both', padx=10, pady=5)
        self.entry_password.pack(fill='both', padx=10, pady=5)
        self.label_age.pack(fill='both', padx=10, pady=5)
        self.entry_age.pack(fill='both', padx=10, pady=5)
        self.label_national_id.pack(fill='both', padx=10, pady=5)
        self.entry_national_id.pack(fill='both', padx=10, pady=5)

        self.submit_button.pack(fill='both', padx=10, pady=10)

        self.root.mainloop()

    def register(self):
        username = self.username_var.get()
        phone = self.phone_var.get()
        mail = self.mail_var.get()
        gender = self.gender_var.get()
        governorate = self.governorate_var.get()
        password = self.password_var.get()
        age = self.age_var.get()
        national_id = self.national_id_var.get()

        # Check for missing user data
        if not username or not phone or not mail or not gender or not governorate or not password or not age or not national_id:
            messagebox.showerror("Error", "Please fill in all the fields.")
            return

        # Check if age and national ID are integers
        try:
            age = int(age)
            national_id = int(national_id)
            phone = int(phone)
        except ValueError:
            messagebox.showerror("Error", "Age, phone, and National ID must be integers.")
            return

        # Check if the user already has an account using the national_id
        if any(usr["National ID"] == national_id for usr in data):
            messagebox.showerror("Error", "This user already has an account")
            return
        else:
            user_data = {
                "Username": username,
                "Phone Number": phone,
                "Email": mail,
                "Gender": gender,
                "Governorate": governorate,
                "Password": password,
                "Age": age,
                "National ID": national_id,
            }
            data.append(user_data)
            save()
            messagebox.showinfo("Success", "Registration successful!")
            self.root.destroy()
            homepage(user_data)

# Start the GUI by creating an instance of the project_GUI class
project_GUI()
