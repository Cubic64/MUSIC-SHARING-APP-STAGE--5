import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
import ftplib
from ftplib import FTP
import ntpath

from tkinter import filedialog
from pathlib import Path

from playsound import playsound
import pygame
from pygame import mixer
import os
import time

PORT = 8050
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096

song_counter = 0

for file in os.listdir('shared_files'):
    filename = os.fsdecode(file)
    Listbox.insert(song_counter, filename)
    song_counter = song_counter + 1

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect({IP_ADDRESS,PORT})

    musicWindow()
setup()

def musicWindow():
    window = Tk()
    window.title('Music Window')
    window.geometry("300x300")
    window.configure(bg = 'LightSkyBlue')

    selectlabel = Label(window, text= "Select Song",bg = 'LightSkyBlue', font = {"Calibri",6})
    selectlabel.place(x=2, y=1)

    listbox = Listbox(window,height = 10,width = 39,activatestyle = 'dotbox',bg = 'LightSkyBlue',borderwidth = 2, font=("Calibri",10))
    listbox.place(x=10,y=10)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight=1,relx=1)
    scrollbar1.config(command = listbox.yview)

    resumeButton = Button(window,text="Resume", width=10,bd=1,bg='SkyBlue',font=("Calibri",10), command=resume)
    resumeButton.place(x=30,y=250)

    pauseButton = Button(window,text="Pause", width=10,bd=1,bg='SkyBlue',font=("Calibri",10), command=pause)
    pauseButton.place(x=200,y=250)

    PlayButton = Button(window,text="Play",width=10,bd=1,bg='SkyBlue',font={"Calibri",10}, command=play)
    PlayButton.place(x=30,y=200)

    Stop = Button(window,text="Stop",width=10,bd=1,bg='SkyBlue',font={"Calibri",10}, command=stop)
    Stop.place(x=200,y=200)

    Upload = Button(window,text="Upload",width=10,bd=1,bg='SkyBlue',font={"Calibri",10})
    Upload.place(x=30,y=250)

    Download = Button(window,text="Download",width=10,bd=1,bg='SkyBlue',font={"Calibri",10})
    Download.place(x=200,y=250)

    window.mainloop()

def play():
    global song_selected
    song_selected = Listbox.get(ANCHOR)

    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()
    if(song_selected !=""):
        infoLabel.configure(text = "Now Playing: "+song_selected)
    else:
        infoLabel.configure(text = "")

def stop():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause()
    infoLabel.configure(text = "")

def resume():
    global song_selected
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()

def pause():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause()

def browserFiles():
    global Listbox
    global song_counter
    global filePathLabel

    try:
        filename = filedialog.askopenfilename()
        HOSTNAME = "127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD = "lftpd"

        ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd('shared_files')
        fname = ntpath.basename(filename)
        with open(filename, 'rb') as file:
            ftp_server.storbinary(f"STOR {fname}", file)

        ftp_server.dir()
        ftp_server.quit()

        Listbox.insert(song_counter, fname)
        song_counter = song_counter + 1

    except FileNotFoundError:
        print("Cancel Button Pressed")

def download():
    song_to_download = Listbox.get(ANCHOR)
    infoLabel.configure(text = "Downloading" + song_to_download)
    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"
    home = str(Path.home())
    download_path = home + "/Downloads"
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"
    ftp_server.cwd('shared_files')
    local_filename = os.path.join(download_path, song_to_download)
    file = open(local_filename, 'wb')
    ftp_server.retrbinary('RETR' + song_to_download, file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()
    infoLabel.configure(text = "Donwload Complete")
    time.sleep(1)
    if(song_selected != ""):
        infoLabel.configure(text = "Now Playing" + song_selected)
    else:
        infoLabel.configure(text = "")
