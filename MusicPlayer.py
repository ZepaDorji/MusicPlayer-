import os # used for removing the pathname while showing in status bar.
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog   # able to search the files
import threading
from ttkthemes import themed_tk as tk
from tkinter import ttk          #ttk= theme tkinter.
from mutagen.mp3 import MP3
from pygame import mixer


#root window : status bar, rightframe, leftframe.
#rightfrma - listbox(play list)
#leftframe - topframe, middleframe and button frame.

root = tk.ThemedTk()# this creates the window.
root.get_themes()
root.set_theme("radiance")

#adding statubar
statusbar = ttk.Label(root,text = "Music Player",relief = SUNKEN,anchor = W,font = "Time 15  italic")#W = west.
statusbar.pack(side = BOTTOM,fill = X) # to fill the statusbar all alone button

menubar = Menu(root)          #creating menu bar
root.configure(menu = menubar)

playlist = []

def browseFile():                 # able to add and search the files.
    global fileName_path
    fileName_path = filedialog.askopenfilename()
    add_to_playlist(fileName_path)


#adding song to playlist.
def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index,fileName_path)
    index += 1


#creating submenu
submenu = Menu(menubar,tearoff = 0)  #tearoff will removed the dashed line.
menubar.add_cascade(label = "File",menu = submenu)
submenu.add_command(label ="Open",command = browseFile)
submenu.add_command(label ="Exit",command = root.destroy)



def Developer():
    tkinter.messagebox.showinfo("Developer","བཟོད་པ་།།This simple music player is developed"
    " by Zepa Dorji as the part of Python class assignment.")


def Features():
    tkinter.messagebox.showinfo("Features","You can either add or remove the song,"
    " volume of song can increase or decrease. Also you can"
    " pause or stop the song. ")



submenu = Menu(menubar,tearoff = 0) #tearoff will removed the dashed line.
menubar.add_cascade(label = "About",menu = submenu)
submenu.add_command(label ="Developer ",command = Developer)
submenu.add_command(label ="Features",command = Features)


def Mission():
    tkinter.messagebox.showinfo("Mission","To develop Simple Music player "
    " with learnig of tkinter and pygame.")


submenu = Menu(menubar,tearoff = 0) #tearoff will removed the dashed line.
menubar.add_cascade(label = "Mission",menu = submenu)
submenu.add_command(label ="Short term",command = Mission)


def help():
    tkinter.messagebox.showinfo("Help","Press add button or open under file menu to add  files."
    "the songs to the list. Select one song from the list and press play button to play."
    "Select the song you want to remove from the list, then press delete button."
    "press cross button or exit under file menu to exit from the music player.")

submenu = Menu(menubar,tearoff = 0) #tearoff will removed the dashed line.
menubar.add_cascade(label = "Help",menu = submenu)
submenu.add_command(label ="How to play",command = help)


mixer.init()     # initializing mixer
#root.geometry('300x400') # reside the window,width:height.
root.title("Music Player") # window title.:support only .ico extension image.
# to converter it to go to icoconver.com
root.iconbitmap(r'Game\favicon.ico') # icon on window.

#dividing screen to two parts
leftframe = Frame(root)
leftframe.pack(side = LEFT,padx = 30,pady = 30)

#creating list of songs
playlistbox = Listbox(leftframe)
playlistbox.pack()

addbtn = ttk.Button(leftframe,text = "+ Add",command = browseFile)
addbtn.pack(side = LEFT)

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song) # removed the song from list box
    playlist.pop(selected_song)       # delete the song from list.


delbtn = ttk.Button(leftframe,text = "- Delete",command = del_song)
delbtn.pack(side = LEFT)

rightframe = Frame(root)
rightframe.pack(pady = 30)


#inside the right frame.
topframe = Frame(rightframe)
topframe.pack()

# everything you add inside the window of tkinter is called widget.
# if you enter text is called label.
#fileText = Label(root,text = "WELLCOME TO MUSIC PLAYER") # takes two parameter, 1.where the text you want
# to appear.2. The actual text.
#fileText.pack(pady = 10)# after adding text if you don't pack the label it will give the error.
#pady = adding padding:


filelength = ttk.Label(topframe,text = "Total length: --:--")
filelength.pack()


currentTime = ttk.Label(topframe,text = "Current time: --:--",relief = GROOVE)
currentTime.pack()




#for total length and name of song displaying.
def songDetails(play_sound):
    #fileText['text'] = "Playing..." + os.path.basename(fileName)
    fileData = os.path.splitext(play_sound)
    if fileData[1] == '.mp3':
        audio = MP3(play_sound)
        totalLength = audio.info.length
    else:
        a = mixer.music.Sound(play_sound)
        totalLength = a.get_length()

    # div:mins = totalLength/60, mod: secs = totalLength%60
    mins,secs = divmod(totalLength,60)
    mins = round(mins)
    secs = round(secs)
    timeformate = '{:02d}:{:02d}'.format(mins,secs)
    filelength['text'] = "Total Length:" + timeformate
    #for handiling the the mult-task.
    t1 = threading.Thread(target= count_start,args=(totalLength,))
    t1.start()



# for current time displaying.
def count_start(t):
    global paused
    current_time = 0
    #mixer.music.get_busy(): will return FALSE if we press the stop button:
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformate = '{:02d}:{:02d}'.format(mins, secs)
            currentTime['text'] = "Current Time:" + timeformate
            time.sleep(1)
            current_time += 1



# play music
def playMusic():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Playing Resume" + "-" + os.path.basename(fileName_path)
        paused = FALSE
    else:
        try:
            stopMusic()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing Music" + "-" + os.path.basename(play_it)
            # to update the statusbar when playing music
            # fileName shows the file name of song you are playing
            songDetails(play_it)
        except:
            tkinter.messagebox.showerror("Music not found", "Music player could"
            " not found the music you are trying to play, please try again.")


# stop music
def stopMusic():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"
    # to update  the status bar when stop the music.



paused = FALSE
def pauseMusic():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused" +"-"+ os.path.basename(fileName_path)



def rewindMusic():
    playMusic()
    statusbar['text'] = "Music Restarted" + "-" + os.path.basename(fileName_path)



mute = FALSE
def muteMusic():
    global mute
    if mute:    # mute = TRUE
        mixer.music.set_volume(0.5)  # set volume to 50
        volumebtn.configure(image=volumePhoto)
        # will change the mute photo to volume photo.
        scale.set(50)  # setting scale back to 70.
        mute = FALSE
    else:         # mute = FALSE
        mixer.music.set_volume(0) # set volume to zero
        volumebtn.configure(image = mutePhoto)
        # will change the volume photo to mute photo.
        scale.set(0) # setting scale to zero.
        mute = TRUE


#volume control
def set_vol(val):
    volume = float(val) / 100 # val converting to int.
    mixer.music.set_volume(volume)
    #set_volume take value between 0 to 1: eg:0.1,0.3,0.5,0.99, 1:
    #so we are dividing by 100 to convert the value between 0 to 1.



#creating frame inside root window, so we can aligne the btns in horizantal.
middleframe = Frame(rightframe)
middleframe.pack(pady = 10)


# button
playphoto = PhotoImage(file ='Game/play.png')
playbtn = ttk.Button(middleframe,image = playphoto,command= playMusic)
playbtn.grid(row = 0,column = 0,padx = 10)


#stopbtn
stopPhoto = PhotoImage(file = "Game/stop.png")
stopbtn = ttk.Button(middleframe,image = stopPhoto,command = stopMusic)
stopbtn.grid(row = 0,column = 1,padx = 10)


#pause
pausePhoto = PhotoImage(file = "Game/pause.png")
pausebtn = ttk.Button(middleframe,image = pausePhoto,command = pauseMusic)
pausebtn.grid(row = 0,column = 2,padx = 10)


buttonframe = Frame(rightframe)
buttonframe.pack(pady = 30,padx = 30)


#rewind
rewindPhoto = PhotoImage(file = "Game/rewind.png")
rewindbtn = ttk.Button(buttonframe,image = rewindPhoto,command =rewindMusic)
rewindbtn.grid(row = 0, column = 0)


#Mute
mutePhoto = PhotoImage(file = "Game/mute.png")
volumePhoto = PhotoImage(file = "Game/volume.png")
volumebtn = ttk.Button(buttonframe,image = volumePhoto,command =muteMusic)
volumebtn.grid(row = 0, column = 1)



scale = ttk.Scale(buttonframe, from_ =0, to =100, orient = HORIZONTAL, command = set_vol)
scale.set(50) # set default value of volume as 50.
mixer.music.set_volume(0.5)
scale.grid(row = 0,column = 2,pady = 15,padx = 30)




#overridding the close button on windows.
def on_closing():
    stopMusic()
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()