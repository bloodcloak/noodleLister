from tkinter import *
from tkinter import ttk,font,messagebox
import listerHelper as helpr
from time import sleep
from sys import exit

# Config Vars
progNam = "Noodlelister v2.0"

# Data class
class programData:
  def __init__(self):
    self.coverPath = 'Not Selected'
    self.listPath = 'Not Selected'
    self.genStatus = ''

data = programData()

def quitProg():
  result = messagebox.askyesno(progNam,"Are you sure you want to Quit?")
  if result:
    exit(0)

def generator():
  workLabel["text"] = "Generating..."
  result = helpr.generateList(root,listTitle.get(),listAuthr.get(),data.coverPath,data.listPath)
  if result == 1:
    workLabel["text"] = "Generation Failed! Enter Playlist Title"
  elif result == 2:
    workLabel["text"] = "Generation Failed! Enter Playlist Author"
  elif result == 3:
    workLabel["text"] = "Generation Failed! Select Cover Image"
  elif result == 4:
    workLabel["text"] = "Generation Failed! Select Song List File"
  else:
    workLabel["text"] = "Successfuly created bplist!"

def getImage():
  data.coverPath = helpr.selImage()
  coverPathLbl["text"] = data.coverPath
def getList():
  data.listPath = helpr.selListFile()
  listPathLbl["text"] = data.listPath

#tkinter setup
root = Tk()
root.title(progNam)
content = ttk.Frame(root)

headerFont = font.Font(family='Helvetica', size=20, weight='bold')
subheaderFont = font.Font(family='Helvetica', size=10)
header = ttk.Label(content, text=progNam, font = headerFont)
subheader = ttk.Label(content, text='by Bloodcloak', font = subheaderFont)

lstTtlLab = ttk.Label(content, text = "Playlist Title")
listTitle = ttk.Entry(content) # Content Entry

lstAthrLab = ttk.Label(content, text = "Playlist Author")
listAuthr = ttk.Entry(content) # Content Entry

selCover = ttk.Button(content, text="Select Cover Image",command = getImage)
coverPathLbl = ttk.Label(content, text = data.coverPath)

selTextFile = ttk.Button(content, text="Select Song List File",command = getList)
listPathLbl = ttk.Label(content, text = data.listPath)

generateList = ttk.Button(content, text="Generate", command = generator)
quitBtn = ttk.Button(content, text="Quit Program", command = quitProg)

workLabel = ttk.Label(content, text=data.genStatus)

# Setup Window
content.grid(column=0, row=0, sticky=(N, S, E, W))
header.grid(column=0, row=0, columnspan=2, pady = 5)
subheader.grid(column=2, row=0, columnspan=2, pady = 5)

lstTtlLab.grid(column=0, row=2, pady = 5)
listTitle.grid(column=1, row=2, columnspan=3, padx = 5, pady = 5)
listTitle.focus_set()

lstAthrLab.grid(column=0, row=3, pady = 5)
listAuthr.grid(column=1, row=3, columnspan=3, padx = 5, pady = 5)

selCover.grid(column=0, row=4, padx = 5, pady = 5)
coverPathLbl.grid(column=1, row=4, columnspan=3, padx = 5, pady = 5)

selTextFile.grid(column=0, row=5, padx = 5, pady = 5)
listPathLbl.grid(column=1, row=5, columnspan=3, padx = 5, pady = 5)

workLabel.grid(column=2, row=6, padx = 5, pady = 5)

quitBtn.grid(column=0, row=10, padx = 5, pady = 10)
generateList.grid(column=2, row=10, padx = 5, pady = 10)

root.mainloop()
