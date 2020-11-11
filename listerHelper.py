import json
import tkinter, tkinter.filedialog, tkinter.messagebox
from tkinter import ttk
import requests
import time
from os import getcwd, path
from sys import exit
import base64
import re

def keyInDict(dict, key): # Helper to check if song already has been added to playlist 
    if key in dict: 
        return True
    else: 
        return False

# Config Vars
progNam = "Noodlelister v1.1.1"
apiURL = 'https://beatsaver.com/api/maps/detail/'
headers = {'User-Agent': 'Noodlelister v1.1.1'}

currentDirectory = getcwd()

# Get image path
def selImage():
  while(True):
    coverImg =  tkinter.filedialog.askopenfilename(initialdir = currentDirectory,title = "Select Cover Image",filetypes = (("png files","*.png"),("Any file","*.*")))
    if not coverImg:
        return 'Not Selected'
    try:
      fiExt = coverImg.split('.')[-1]
      if((fiExt == 'png') or (fiExt == 'PNG')):
          with open(coverImg,"rb") as imgPtr:
            return coverImg
      else:
        result = tkinter.messagebox.askyesno(progNam,"File is not a png, choose a different one?")
        if (result == False):
          return 'Not Selected'
    except:
      result = tkinter.messagebox.askyesno(progNam,"Invalid File, choose a different one?")
      if (result == False):
        return 'Not Selected'
  return 'Not Selected'  

# Get Song List path
def selListFile():
  while(True):
    songList =  tkinter.filedialog.askopenfilename(initialdir = currentDirectory,title = "Select Song List Text File",filetypes = (("txt files","*.txt"),("Any file","*.*")))
    if not songList:
      return 'Not Selected'
    try:
      fiExt = songList.split('.')[-1]
      if((fiExt == 'txt') or (fiExt == 'TXT')):
          with open(songList,"r") as listPtr:
            return songList
      else:
        result = tkinter.messagebox.askyesno(progNam,"File is not a txt, choose a different one?")
        if (result == False):
          return 'Not Selected'
    except:
      result = tkinter.messagebox.askyesno(progNam,"Invalid File, choose a different one?")
      if (result == False):
        return 'Not Selected'
  return 'Not Selected'  

# Convert Image to base64 data
def processImg(coverImg):
  try:
    with open(coverImg,"rb") as imgPtr:
      img = imgPtr.read()
      return "data:image/png;base64,"+base64.encodebytes(img).decode("utf-8")
  except Exception as e:
    tkinter.messagebox.showerror(progNam,"Something went wrong... \nException in Img Conversion: {}".format(e))
    exit(1)

# Get Songs and pack into file
def processSongs(songList):
  textSongCount = 0
  successCount = 0
  messageLog = ''
  songKeysChecked = {}
  songOutput = []

  try:
    with open(songList,"r") as listPtr:
      songs = listPtr.readlines()

      # Request Map Hash from Beatsaver API, assemble json object and put into list
      try:
        for i in songs:
          time.sleep(.1) # Prevent Rate Limiting
          textSongCount += 1

          # Regex Processing to Sanitize Input
          cleanStr = re.sub('[^A-Fa-f0-9]+', '', i)
          
          # Convert to python hex
          hex_int = int(cleanStr, base=16)
          mapKey = hex(hex_int).split('x')[1]
          
          # Duplicate entry check
          if (keyInDict(songKeysChecked,mapKey) == False):
            songKeysChecked[mapKey] = 1

            r = requests.get(apiURL+mapKey ,headers = headers) # request song from api
              
            if r.status_code != 200: # If response not success skip map key
              messageLog = messageLog+("Skipping Map: {} | API returned code: {} \n".format(mapKey, r.status_code))
              continue
            
            # Cleanup response to process as python dictionary
            rDict = json.loads(r.text)

            try:
              mapObject = {'key': rDict['key'],
                          'hash': rDict['hash'],
                          'songName': '{} - {}'.format(rDict['metadata']['songAuthorName'], rDict['metadata']['songName']),
                          'uploader': rDict['uploader']['username']}
            except:
              messageLog = messageLog+("Map Key: {} API Response Not Valid! Skipping...\n".format(mapKey))
              continue
            songOutput.append(mapObject)
            successCount += 1
          else:
            messageLog = messageLog+("Map: {} | Has a duplicate entry on line {}\n".format(mapKey,textSongCount))

      except Exception as e:
        tkinter.messagebox.showerror(progNam,"Something went wrong... \nException in API Processing: {}".format(e))
        exit(2)
      
      # Processing Complete Package and Notify
      successString = "Imported {} out of {} entries successfully!\n".format(successCount,textSongCount)
      if messageLog:
        messageLog = successString+"======\n"+messageLog
        tkinter.messagebox.showwarning(progNam,messageLog)
      else:
        tkinter.messagebox.showinfo(progNam, successString)
      return songOutput # Send all responses to the json dict for export
  
  except Exception as e:
    tkinter.messagebox.showerror(progNam,"Something went wrong... \nException in Song List Processing: {}".format(e))
    exit(3)


# Generate File Name and save info
def generateList(rootWindow,listTitle, listAuthr, coverImg, songList):
  if not listTitle:
    return 1
  if not listAuthr:
    return 2
  if(coverImg == 'Not Selected'):
    return 3
  if(songList == 'Not Selected'):
    return 4
  jsonOutput = {}

  jsonOutput['playlistTitle'] = str(listTitle)
  jsonOutput['playlistAuthor'] = str(listAuthr)
  jsonOutput['image'] = processImg(coverImg)
  jsonOutput['songs'] = processSongs(songList)

  try:
      # Process Starting File Name
      cleanName = re.sub('[^A-Za-z0-9]+', '', listTitle) # Sanitize Input
      savePath = path.join(currentDirectory,cleanName+".bplist") # use initialfile when transfer to tkinter

      with open(savePath,"w") as fileLoc:
        fileLoc.write(json.dumps(jsonOutput, indent=4))

  except Exception as e:
    tkinter.messagebox.showerror(progNam,"Something went wrong... \nException in Playlist Exporting: {}".format(e))
    exit(4)

  #tkinter.messagebox.showinfo(progNam, "Successfuly created bplist!")
  return 0
