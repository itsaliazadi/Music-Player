import os
import customtkinter
from tkinter import *
import tkinter as ttk
from pygame import mixer
from tkinter import filedialog

# Set the default color theme and appearance mode for customtkinter
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_appearance_mode("dark")

# Create the main window
window = ttk.Tk()
window.title("Music Player")
window.geometry("900x600")
window.resizable(False, False)

# Set the background image
bgimg = PhotoImage(file="Background.png")
limg = Label(window, image=bgimg)
limg.place(x=0, y=0, relheight=1, relwidth=1)

# Function to add multiple music files to the playlist
def addManyMusics():
    musics = filedialog.askopenfilenames(initialdir="musics/", filetypes=(("mp3 Files", "*.mp3"), ))
    for music in musics:
        music = music.replace("/home/ali/test/code/music_player/musics/", "").replace(".mp3", "")
        if music not in music_box.get(0, END):
            music_box.insert(END, music)

# Creating the music list box
music_box = Listbox(window, bg="#A87BB9", highlightthickness=5, width=40, fg="white", font="Latha")
music_box.place(x=260)

menu = Menu(window)
window.config(menu=menu)

addMusic_menu = Menu(menu)
menu.add_cascade(label="Add musics", menu=addMusic_menu)
addMusic_menu.add_command(label="Add musics to your playlist", command=addManyMusics)

mixer.init()

# Creating a slider to display the music progress
slider = None

# Function to play the next music in the playlist
def playNext():
    global slider
    slider.destroy()
    next_music1 = music_box.curselection()[0] + 1
    music1 = music_box.get(next_music1)

    music_box.selection_clear(0, END)
    music_box.activate(next_music1)
    music_box.selection_set(next_music1, last=None)

    lenght1 = mixer.Sound("/home/ali/test/code/music_player/musics/"+music1+".mp3").get_length()
    print(music1, lenght1)
    slider = customtkinter.CTkSlider(window, from_=0, to=lenght1, width=400, height=20, bg_color="#9B57B5",
                                 fg_color="white", button_color="black", progress_color="#4B1B5E")
    slider.place(x=275, y=420)
    slider.set(0)

    def updateSlider():
        musicPosition = mixer.music.get_pos()/1000
        slider.set(musicPosition)
        window.after(1000, updateSlider)

    updateSlider()

    mixer.music.load("/home/ali/test/code/music_player/musics/"+music1+".mp3")
    mixer.music.play(loops=0)

# Function to play the selected music
def playMusic():
    global slider
    if slider:
        slider.destroy()
    music = music_box.get(ACTIVE)

    mixer.music.load("/home/ali/test/code/music_player/musics/"+music+".mp3")
    mixer.music.play(loops=0)
    
    pauseButtonImg = PhotoImage(file="2.png")
    playButton.config(image=pauseButtonImg, command=pauseMusic)
    playButton.photo = pauseButtonImg

    lenght = mixer.Sound("/home/ali/test/code/music_player/musics/"+music+".mp3").get_length()
    slider = customtkinter.CTkSlider(window, from_=0, to=lenght, width=400, height=20, bg_color="#9B57B5",
                                 fg_color="white", button_color="black", progress_color="#4B1B5E")
    slider.place(x=275, y=420)
    slider.set(0)

    l = music_box.get(first=0, last=4)
    c = 0
    for i in l:
        if music in l:
            break
        c += 1
    pre_music = l[c+1]
    print(pre_music)
    pre_length = mixer.Sound("/home/ali/test/code/music_player/musics/"+pre_music+".mp3").get_length()

    def updateSlider():
        global slider
        musicPosition = mixer.music.get_pos()/1000
        slider.set(musicPosition)
        window.after(1000, updateSlider)

        if int(slider.get()) == int(lenght) and int(lenght)!= int(pre_length):
            print(lenght, pre_length)
            playNext()

    updateSlider()

# Function to resume the music
def resumeMusic():
    mixer.music.unpause()
    
    pauseButtonImg = PhotoImage(file="2.png")
    playButton.config(image=pauseButtonImg, command=pauseMusic)
    playButton.photo = pauseButtonImg

# Function to pause the music
def pauseMusic():
    mixer.music.pause()
    
    playButtonImg = PhotoImage(file="1.png")
    playButton.config(image=playButtonImg, command=resumeMusic)
    playButton.photo = playButtonImg

# Function to play the previous music in the playlist
def playPre():
    global slider
    music = music_box.get(ACTIVE)
    if slider:
        slider.destroy()
    pre_music = music_box.curselection()[0] - 1
    music = music_box.get(pre_music)

    music_box.selection_clear(0, END)
    music_box.activate(pre_music)
    music_box.selection_set(pre_music, last=None)

    mixer.music.load("/home/ali/test/code/music_player/musics/"+music+".mp3")
    mixer.music.play(loops=0)

    lenght = mixer.Sound("/home/ali/test/code/music_player/musics/"+music+".mp3").get_length()
    slider = customtkinter.CTkSlider(window, from_=0, to=lenght, width=400, height=20, bg_color="#9B57B5",
                                 fg_color="white", button_color="black", progress_color="#4B1B5E")
    slider.place(x=275, y=420)
    slider.set(0)

    def updateSlider():
        global slider
        musicPosition = mixer.music.get_pos()/1000
        slider.set(musicPosition)
        window.after(1000, updateSlider)

    updateSlider()

# Creating the play button
playButtonImg = PhotoImage(file="1.png")
playButtonLabel = Label(image=playButtonImg, background="#7100ff")
playButtonLabel.place(x=450, y=500)
playButton = Button(window, image=playButtonImg, command=playMusic,
                    background="#7100ff", highlightthickness=0, activebackground="#7100ff")
playButton.place(x=450, y=500)

# Creating the next button
nextButtonImg = PhotoImage(file="3.png")
nextButtonLabel = Label(image=nextButtonImg, background="#8e01ff")
nextButtonLabel.place(x=650, y=500)
nextButton = Button(window, image=nextButtonImg, command=playNext, background="#8e01ff",
                    highlightthickness=0, activebackground="#8e01ff")
nextButton.place(x=650, y=500)

# Creating the previous button
preButtonImg = PhotoImage(file="4.png")
preButtonLabel = Label(image=preButtonImg, background="#8401ff")
preButtonLabel.place(x=250, y=500)
preButton = Button(window, image=preButtonImg, command=playPre, background="#8401ff",
                    highlightthickness=0, activebackground="#8401ff")
preButton.place(x=250, y=500)

window.mainloop()
