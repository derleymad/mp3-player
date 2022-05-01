import os 
import threading
from pygame.mixer import *
from pygame.time import *
from pathlib import Path
from tkinter import ANCHOR, Tk,Frame,Label,Button,Listbox,PhotoImage,BOTH,CENTER,ACTIVE
from tkinter.filedialog import askdirectory

song_list = ''; threads = []; parado = False ; tocando = '';index = 0

#ROOT
root = Tk()
root.geometry('280x400')
root.title('MP3 Adênia')
root.config(cursor="heart") 
root.resizable(0,0)
root.config(bg='black')
root.attributes('-alpha',0.9)

#FRAME1
frame1 = Frame(
    root,
    bg='black'
    )
frame1.pack(
    fill=BOTH,
    expand=True
    )

#FRAME2
frame2 = Frame(
    root,
    bg='black'
    )
frame2.pack(
    fill='x',
    expand=False
    )

#FRAME3
frame3 = Frame(
    root,
    bg='black',
    highlightbackground="gray",
    highlightthickness=1

    )
frame3.pack(
    fill=BOTH,
    expand=True, 
    padx=10,
    pady=10
    )

#IMAGENS DOS BOTÕES
imgPlay = PhotoImage(file = "assets/images/play_img.png")
imgPause = PhotoImage(file = "assets/images/pause_img.png")
imgNext = PhotoImage(file = "assets/images/next_img.png")
imgPreview = PhotoImage(file = "assets/images/prev_img.png")
imgAsk = PhotoImage(file = "assets/images/lupa2.png")

#FUNCOES DO PROGRAMA

def changeOnHover(button, colorOnHover): 

   button.bind("<Enter>", func=lambda e: button.config( 
       background = colorOnHover
        )) 
   button.bind("<Leave>", func=lambda e: button.config( 
       background = 'black' 
        )) 

def changeImgPlayButton(Evento = None):
    song = listbox.get(ANCHOR)
    if tocando != song:
        buttonPlay.config(image=imgPlay)
    else:
        buttonPlay.config(image=imgPause)

def defaultList():
    global song_list
    list = '.'
    try:
        list = str(Path.home() / "Music")
    except:
        pass

    os.chdir(list) 
    song_list = os.listdir() 

    addToList(song_list)
        
    labelTop['text'] = os.path.basename(list)

def startThreadProcess():
    myNewThread = threading.Thread(target=teste)
    threads.append(myNewThread)
    myNewThread.start()

def addToList(song_list):
    clearList()
    for song in song_list:
        if '.mp3' in song:
            if len(song) >= 30:
                songOut = song
                listbox.insert('end', songOut[:29]+' ... '+'.mp3')
            else:
                listbox.insert('end',song)
        else: 
            song_list.remove(song)

def clearList():
    listbox.delete(0,'end') 

def ask(Event = None):
    global song_list
    directory = askdirectory()
    os.chdir(directory) 
    song_list = os.listdir() 
    addToList(song_list)
    labelTop['text'] = os.path.basename(directory)

def play(Event = None):
    global song_list,parado,tocando,index
    song = listbox.get(ACTIVE)

    if tocando == song:
        if parado:
            music.unpause()
            buttonPlay.config(image= imgPause)
            parado = False 
        else:
            music.pause()
            buttonPlay.config(image= imgPlay)
            parado = True
    else:
        for i in song_list:
            if len(i) >= 30:
                if song[:29] in i:
                    init()
                    music.load(i)
                    music.play()
                    tocando = song
                    label['text'] = song 
                    buttonPlay.config(image= imgPause)
                    listbox.itemconfig(ACTIVE,{'bg':'light green'})
            else:
                if song in i:
                    init()
                    music.load(song)
                    music.play()
                    label['text'] = song 
                    tocando = song 
                    buttonPlay.config(image= imgPause)
                    listbox.itemconfig(ACTIVE,{'bg':'light green'})
def selection(signal):
    global index,song_list
    for item in listbox.curselection():
        listBoxIndex = item
    if signal == 'next':
        listBoxIndexSignal = listBoxIndex+1
    else:
        listBoxIndexSignal = listBoxIndex-1

    listbox.selection_clear(listBoxIndex)
    listbox.selection_set(listBoxIndexSignal)
    listbox.activate(listBoxIndexSignal)

def next(Event = None):
    selection('next')
    play()

def preview(Event = None):
    selection('prev')
    play()

#TKINTER PART OF PROGRAM
listbox = Listbox(
    frame1,
    bg='light blue',
    fg='blue',
    font=('Times','10'),
    justify=CENTER,
    selectmode="single"
    )

#LIST BOX
listbox.pack(
    side='bottom',
    expand=True,
    fill='both',
    padx=10,
    )

listbox.bind('<Double-Button-1>',play)
listbox.bind('<Return>',play)
listbox.bind('<<ListboxSelect>>',changeImgPlayButton)

#LABEL DA MÚSICA TOCANDO
label = Label(
    frame2,
    bg='black',
    fg='yellow',
    font='Times'
    )
label.pack(
    expand=True,
    fill='both'
    )

#BUTÃO ASK
buttonAsk = Button(
    frame1,
    text='. . .',
    fg='yellow',
    command=ask, 
    bg='black',
    borderwidth=0,
    font=('Times','15','bold'),
    cursor='plus'
    )
buttonAsk.pack(
    side='right',
    padx=10
    )

#LABEL DO DIRETÓRIO
labelTop = Label(
    frame1,
    bg='black',
    fg='yellow',
    font='Times'
)
labelTop.pack(
    side = 'top',
    fill='x',
    pady=10,
    )

#BUTAO NEXT
buttonNext = Button(
    frame3,
    width=50,
    height=50,
    text='Play',
    command=next,
    bg='black',
    image=imgNext,
    borderwidth=2,
    cursor = 'right_side'
    )
buttonNext.pack(
    expand=False,
    side='right',
    padx=20
    )

#BUTAO PLAY
buttonPlay = Button(
    frame3,
    width=50,
    height=50,
    text='Play',
    command=play,
    bg='black',
    image=imgPlay,
    borderwidth=2
    )
buttonPlay.pack(
    expand=False,
    side='right',
    )

#BUTAO PREVIEW
buttonPreview = Button(
    frame3,
    width=50,
    height=50,
    text='Play',
    command=preview,
    bg='black',
    image=imgPreview,
    borderwidth=2,
    cursor= 'left_side'
    )
buttonPreview.pack(
    expand=False,
    side='right',
    padx=20
    )

changeOnHover(buttonPlay,'#202020')
changeOnHover(buttonNext,"#202020")
changeOnHover(buttonPreview,"#202020")
changeOnHover(buttonAsk,"#202020")

defaultList()

root.mainloop()
  