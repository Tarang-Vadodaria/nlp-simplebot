# WRITE YOUR CODE HERE
import tkinter.scrolledtext as tks #creates a scrollable text window
import openai
from datetime import datetime
import os
from tkinter import *

# Initialize the OpenAI client with the API key

#client.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key=os.getenv('OPENAI_API_KEY')

# Generating response
def get_bot_response(user_input):
    prompt = f"Please provide a response to the following user input: '{user_input}'"
    response = openai.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "user", "content": prompt}
      ],
      temperature=0.5
    )
    return response.choices[0].message.content


def create_and_insert_user_frame(user_input):
  userFrame = Frame(chatWindow, bg="#d0ffff")
  Label(
      userFrame,
      text=user_input,
      font=("Arial", 11),
      bg="#d0ffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
  Label(
      userFrame,
      text=datetime.now().strftime("%H:%M"),
      font=("Arial", 7),
      bg="#d0ffff"
  ).grid(row=1, column=0, sticky="w")

  chatWindow.insert('end', '\n ', 'tag-right')
  chatWindow.window_create('end', window=userFrame)


def create_and_insert_bot_frame(bot_response):
  botFrame = Frame(chatWindow, bg="#ffffd0")
  Label(
      botFrame,
      text=bot_response,
      font=("Arial", 11),
      bg="#ffffd0",
      wraplength=400,
      justify='left'
  ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
  Label(
      botFrame,
      text=datetime.now().strftime("%H:%M"),
      font=("Arial", 7),
      bg="#ffffd0"
  ).grid(row=1, column=0, sticky="w")

  chatWindow.insert('end', '\n ', 'tag-left')
  chatWindow.window_create('end', window=botFrame)
  chatWindow.insert(END, "\n\n" + "")


def place_automatically(widget, parent, x_offset, y_offset):
    """Places a widget automatically below the last widget in the parent."""

    # Get the bounding box of the last child widget in the parent
    last_child = parent.winfo_children()[-1]
    x, y, width, height = parent.bbox(last_child)

    # Place the new widget below the last child
    widget.place(x=x + x_offset, y=y + height + y_offset)

def get_display_size():
    root = Tk()
    
    # set the Tk window to transparent
    root.attributes("-alpha", 0)
    
    display_height = root.winfo_screenheight()
    display_width = root.winfo_screenwidth()
    
    root.destroy()

    return display_width, display_height

def send(event):
    chatWindow.config(state=NORMAL)

    user_input = userEntryBox.get("1.0",'end-2c')
    user_input_lc = user_input.lower()
    bot_response = get_bot_response(user_input_lc) 

    create_and_insert_user_frame(user_input)
    create_and_insert_bot_frame(bot_response)

    chatWindow.config(state=DISABLED)
    userEntryBox.delete("1.0","end")
    chatWindow.see('end')

# Create the main application window using Tk()
baseWindow = Tk()

#Initialize the screen resolution of tkinter
#baseWindow.wm_state('zoomed')

# Set the title of the window
baseWindow.title("The Simple Bot")

base_width, base_height = get_display_size()
baseWindow.geometry('%dx%d+%d+%d' % (base_width * 0.9, base_height * 0.9, 0, 0))

# Set background color for the main window
baseWindow.configure(bg='lightblue')

# Create the chat window as a ScrolledText widget with "Arial" font
chatWindow = tks.ScrolledText(baseWindow, font="Arial", width=int(base_width * 0.8), height=int(base_height * 0.8), bg='white', fg='black')

# Configure tags for message alignment: 'tag-left' for bot messages, '
# tag-right' for user messages
chatWindow.tag_configure('tag-left', justify='left', background='white', foreground='black')
chatWindow.tag_configure('tag-right', justify='right', background='white', foreground='black')

# Disable the chat window initially (it should not be editable by the user)
chatWindow.config(state=DISABLED)

# Add the chat window to the main window
chatWindow.pack(padx=20, pady=20)

# Create the send button, with specific font, text, and background color
# The 'command' option is commented out. Uncomment it and replace 'send' with your send function's name
sendButton = Button(
    baseWindow,
    font=("Verdana", 12, 'bold'),
    text="Send",
    bg="#fd94b4",
    activebackground="#ff467e",
    fg='#ffffff',
    command=send)
sendButton.bind("<Button-1>", send)
baseWindow.bind('<Return>', send)

# Create the user entry box where the user types their messages
userEntryBox = Text(baseWindow, bd=1, bg="white", height=4,width=80, font="Arial")

# Place the chat window, user entry box, and send button on the main window using specific coordinates and sizes

place_automatically(userEntryBox, baseWindow, base_width * 0.4, base_height * 0.8)

sendButton.place(x=base_width * 0.8, y=base_height * 0.8 + 50)

# Start the main event loop to keep the application running and responsive
baseWindow.mainloop()