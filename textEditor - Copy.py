from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser
import google.generativeai as genai
from dotenv import load_dotenv
import os


# loading env file with api key environmen variable
load_dotenv()
API_KEY = os.getenv('API_KEY')
# configuring gemini ai api
genai.configure(api_key=API_KEY)
# setting tone for text rephraser
tone = "formal"
# initializing tk root
root = Tk()
filename = StringVar()
findText = StringVar()
# initializing data variable for further extracting of data from text widget
data = ""  
# initializing corrected variable for further extracting of corrected text from ai panel and storing it in this panel for further use
correctedText = ""
color = "black"
#funtion for setting data variable to value of text widget
def getText():
    global data
    data = text.get("1.0","end-1c")     
# changing name of root's title based on filename
def changeName(name):
     
     root.title(name)
# detecting key press for saving data if ctrl+s is pressed           
def detect_key_press(event):
    if (event.state & 0x0004 and  event.keysym == 's'):
            print("Ctrl+S is pressed")
            saveas()
# saveas function
def saveas():
     path = filedialog.asksaveasfilename(
          title="Save file as",
          defaultextension='.txt',
          filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
     )
     with open(f'{path}','w') as f:
        getText()        
        f.write(data)
     name = filename.get()   
     changeName(name=name) 
def setColor():



     global color
     color = colorchooser.askcolor(title="set font color")
     bg= color[0]
     fg = f"({255-(color[0][0])}, {255-(color[0][1])}, {255-(color[0][2])})"
     text.config(bg=color[1])
def resize(event):
     w = event.width
     h = event.height
# openFile function for opening a specific file in editor
def openFile():
     file = filedialog.askopenfilename(
          title="Open file"
     )
     with open(f'{file}','r') as f:
          text.delete("1.0",tk.END)
          textDoc = f.readlines()  
          print(textDoc)
          i = 1
          for line in textDoc:
               
               text.insert(f"{len(textDoc)}.0",line)
               print(line)
             
     print(file)
# copy function currently not working
def copy():
     getText()
     root.clipboard_append(data)
# function for ai based rephrasing of text 
def rephrase():
     ai_suggestions.configure(state="normal")
     ai_suggestions.delete("1.0",tk.END)
     button5.grid(row=0, column=6)
     button6.grid(row=0, column=7)
     button7.grid(row=0, column=8)
     getText()
     model = genai.GenerativeModel("gemini-1.5-flash")
     response = model.generate_content(f"{data}, rephrase it in a {tone} tone, just give the rephared text(s) and nothing else")
     print(response.text)
     lines = response.text.splitlines()
     ai_suggestions.insert(f"{len(lines)}.0",response.text)
     ai_suggestions.configure(state="disabled") 
# setting the rephrase tone to informal         
def informal():
     global tone
     tone = "informal"
# setting tone to creative 
def creative():
     global tone
     tone = "creative"  
#  setting tone to formal  
def formal():
     global tone
     tone = "formal"     
def spellChecker():
     global correctedText
     ai_suggestions.configure(state="normal")
     model = genai.GenerativeModel("gemini-1.5-flash")
     getText()
     res= model.generate_content(f'{data}, return the same text with all spelling corrected, if spelling are alreafdy correct thewn return that part as it is')  
     print(res.text) 
     lines= res.text.splitlines()
     ai_suggestions.delete("1.0",tk.END)
     ai_suggestions.insert(f'{len(lines)}.0',res.text)
     correctedText = res.text
     ai_suggestions.configure(state="disabled") 
     button9.grid(row=0,column=10)
# function for ai based spell checking 
def correct():
     global correctedText
     text.delete("1.0",tk.END)
     text.insert(f"{len(correctedText.splitlines())}.0",correctedText)
# function for inserting the correctly spelled text in editor
root.minsize(400,400)
# initializing all widgets
label = ttk.Label(text="Enter file name")
textBox = ttk.Entry(textvariable=findText)
text = tk.Text(fg= "black")
ai_suggestions = tk.Text(bg="black", fg="white")
button = ttk.Button(text="save" ,command=saveas)
button1 = ttk.Button(text="color" ,command=setColor)
button2 = ttk.Button(text="open" ,command=openFile)
button3 = ttk.Button(text="copy" ,command=copy)
button4 = ttk.Button(text="ai rephrase" ,command=rephrase)
button5 = ttk.Button(text="formal" ,command=formal)
button6 = ttk.Button(text="informal" ,command=informal)
button7 = ttk.Button(text="creative" ,command=creative)
button8 = ttk.Button(text="spellCheck",command=spellChecker)
button9 = ttk.Button(text="correct",command=correct)

# binding keypress event to detect_key_press function
root.bind("<KeyPress>", detect_key_press) 
root.bind("<Configure>", resize)  
# displaying all widgets on root(window) 
button.grid(row=0, column=0)
button1.grid(row=0, column=1)
button2.grid(row=0, column=2)
button3.grid(row=0, column=3)
button4.grid(row=0, column=4)
button8.grid(row=0,column=5)
text.grid(row=1,columnspan=8)
ai_suggestions.grid(row=1,column= 10,columnspan=4)

# end of mainloop
root.mainloop()