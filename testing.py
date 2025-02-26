import random, copy, tkinter, tkinter.ttk, tkinter.font, os, gtts
from pygame import mixer

FileDirPath = os.path.dirname(os.path.abspath(__file__))
testFiles:list[str] = []
with open(os.path.join(FileDirPath, "option.txt"), "r", encoding="UTF8") as file:
    while (line:=file.readline()):
        testFiles.append(line.rstrip())
print(testFiles)

def getAnswers(words:list[str]) -> list[str]:
    answers = []
    for word in words:
        if word[0] == "(":
            index = word.find(")")
            answers.append(word[index+1:])
        else:
            answers.append(word)
    return answers

window = tkinter.Tk()

window.title(", ".join(map(lambda x: x[x.rfind("/")+1:-4], testFiles)))
WINDOWWIDTH = 1200
WINDOWHEIGHT = 600
WINDOWXPOS = (window.winfo_screenwidth()-WINDOWWIDTH)//2
WINDOWYPOS = (window.winfo_screenheight()-WINDOWHEIGHT)//2-40
window.geometry("{}x{}+{}+{}".format(WINDOWWIDTH,WINDOWHEIGHT,WINDOWXPOS,WINDOWYPOS))
window.resizable(False, False)

paperlogy9 = tkinter.font.Font(family="Paperlogy 9 Black", size=24)
paperlogy7 = tkinter.font.Font(family="Paperlogy 7 Bold", size=20)
paperlogy6 = tkinter.font.Font(family="Paperlogy 6 SemiBold", size=16)
paperlogy5 = tkinter.font.Font(family="Paperlogy 5 Medium", size=12)

# style = tkinter.ttk.Style()
# style.theme_use("default")
# style.configure(".greenProgress.BarHorizontal.TProgressbar", background="green")
# style.layout("redProgressBar.Horizontal.TProgressbar",
#              [('Horizontal.Progressbar.trough',
#                {'children': [('Horizontal.Progressbar.pbar',
#                               {'side': 'right', 'sticky': 'e'})],
#                               'sticky': 'nswe'})])
# style.configure("redProgressBar.Horizontal.TProgressbar", background="red")

# greenProgressbar = tkinter.ttk.Progressbar(window, style="greenProgressBar.Horizontal.TProgressbar", orient="horizontal")
# redProgressbar = tkinter.ttk.Progressbar(window, style="redProgressBar.Horizontal.TProgressbar", orient="horizontal")
canvas = tkinter.Canvas(window, width=WINDOWWIDTH, height=20, bg="black")
greenRect = canvas.create_rectangle(0, 0, 0, 20, fill="#21FA90", width=0)
redRect = canvas.create_rectangle(WINDOWWIDTH, 0, WINDOWWIDTH, 20, fill="#FF0000", width=0)
def setGreenRect(maximum, value):
    canvas.coords(greenRect, 0, 0, (value*WINDOWWIDTH)/maximum, 20)
def setRedRect(maximum, value):
    canvas.coords(redRect, WINDOWWIDTH-((value*WINDOWWIDTH)/maximum), 0, WINDOWWIDTH, 20)
countLabel = tkinter.Label(window, font=paperlogy6, anchor="e", padx=10)
announceLabel = tkinter.Label(window, text="", font=paperlogy9, wraplength=WINDOWWIDTH-50)
wordLabel = tkinter.Label(window, text="", font=paperlogy7, anchor="e", padx=20)
wordEntry = tkinter.Entry(window, font=paperlogy7)
wordListFrame = tkinter.Frame(window)
wordListScrollBar = tkinter.Scrollbar(wordListFrame)
wordListText = tkinter.Text(wordListFrame, font=paperlogy5, yscrollcommand=wordListScrollBar.set, state="disabled")
wordListScrollBar.config(command=wordListText.yview)
wordOriginLabel = tkinter.Label(window, font=paperlogy5, anchor="w")
wordPageLabel = tkinter.Label(window, font=paperlogy5, anchor="e")

AudioFileDirPath = os.path.join(FileDirPath, "audio")
def makeFileName(name:str):
    return "{}.mp3".format(name.replace("/","+"))
mixer.init()
mixer.music.set_volume(1)

volumeLabel = tkinter.Label(window, font=paperlogy6, anchor="w")
volume = tkinter.IntVar()
volumeBar = tkinter.Scale(window, variable=volume, orient="horizontal", showvalue=False, width=10)
def setVolume(event):
    mixer.music.set_volume(volumeBar.get()/100)
    volumeLabel.config(text="volume:{}%".format(volumeBar.get()))
volumeBar.config(command=setVolume)
volumeBar.set(100)

AudioFiles = os.listdir(AudioFileDirPath)
wordSets:dict[str,list[str]] = dict()
wordOrigin:dict[str,str] = dict()
wordPage:dict[str,str] = dict()
thisPage = ""
for filename in testFiles:
    with open(filename, "r", encoding="UTF8") as file:
        while (line:=file.readline()):
            word = line.rstrip().split("|")
            if len(word) == 2:
                word[1] = word[1].split(",")
                wordSets[word[0]] = word[1]
                wordOrigin[word[0]] = filename
                wordPage[word[0]] = thisPage
                audioName = makeFileName(word[0])
                if not audioName in AudioFiles:
                    tts = gtts.gTTS(text=word[0])
                    tts.save(os.path.join(AudioFileDirPath, audioName))
                    print(audioName, "is made")
            elif line[0] == "p":
                thisPage = line.rstrip()
wordNumber = len(wordSets)
print("loaded {} words completely".format(wordNumber))
countLabel.config(text="0/{}/0".format(wordNumber))

def playWordAudio():
    audioName = makeFileName(wordKeys[wordIndex])
    try:
        mixer.music.load(os.path.join(AudioFileDirPath, audioName))
    except:
        print("Catching The Error\nTrying recovery")
        tts = gtts.gTTS(text=wordKeys[wordIndex])
        tts.save(os.path.join(AudioFileDirPath, audioName))
        print(audioName, "is made")
        mixer.music.load(os.path.join(AudioFileDirPath, audioName))
    mixer.music.play()

wordKeys = list(wordSets.keys())
random.shuffle(wordKeys)
gettingWord = True
totalMemoryCount = 0
newMemoryCount = 0
wordIndex = 0
wrongWords = []
wordLabel.config(text=wordKeys[wordIndex])
wordOriginLabel.config(text=wordOrigin[wordKeys[wordIndex]])
wordPageLabel.config(text=wordPage[wordKeys[wordIndex]])
playWordAudio()
passing = True

def inputWord(event):
    global totalMemoryCount, newMemoryCount, gettingWord, wordKeys, wordIndex, wrongWords, passing
    if passing or wordEntry.get() in getAnswers(wordSets[wordKeys[wordIndex-1]]):
        if wordIndex != len(wordKeys):
            if gettingWord and wordEntry.get() != "":
                if wordEntry.get() in getAnswers(wordSets[wordKeys[wordIndex]]):
                    announceLabel.config(text="correct -> {}".format(", ".join(wordSets[wordKeys[wordIndex]])))
                    totalMemoryCount += 1
                    newMemoryCount += 1
                    setGreenRect(wordNumber, totalMemoryCount)
                else:
                    announceLabel.config(text="wrong, answer is " + ", ".join(wordSets[wordKeys[wordIndex]]))
                    wrongWords.append(wordKeys[wordIndex])
                    wordListText.config(state="normal")
                    wordListText.insert("1.0", "{} | {}\n".format(wordKeys[wordIndex], ", ".join(wordSets[wordKeys[wordIndex]])))
                    wordListText.config(state="disabled")
                    setRedRect(wordNumber, len(wrongWords))
                    passing = False
                countLabel.config(text="{}/{}/{}".format(totalMemoryCount, wordNumber-totalMemoryCount-len(wrongWords), len(wrongWords)))
                gettingWord = False
                wordIndex += 1
            else:
                wordLabel.config(text=wordKeys[wordIndex])
                wordEntry.delete(0,len(wordEntry.get()))
                announceLabel.config(text="")
                gettingWord = True
                wordOriginLabel.config(text=wordOrigin[wordKeys[wordIndex]])
                wordPageLabel.config(text=wordPage[wordKeys[wordIndex]])
                passing = True
                playWordAudio()
        else:
            passing = True
            wordEntry.delete(0,len(wordEntry.get()))
            if gettingWord:
                wordIndex = 0
                newMemoryCount = 0
                if totalMemoryCount == wordNumber:
                    wordKeys = list(wordSets.keys())
                    totalMemoryCount = 0
                    setGreenRect(wordNumber,0)
                else:
                    wordKeys = copy.deepcopy(wrongWords)
                setRedRect(wordNumber,0)
                random.shuffle(wordKeys)
                wrongWords = []
                wordLabel.config(text=wordKeys[wordIndex])
                announceLabel.config(text="")
                wordListText.config(state="normal")
                wordListText.delete("1.0",tkinter.END)
                wordListText.config(state="disabled")
                wordOriginLabel.config(text=wordOrigin[wordKeys[wordIndex]])
                wordPageLabel.config(text=wordPage[wordKeys[wordIndex]])
                countLabel.config(text="{}/{}/{}".format(totalMemoryCount, wordNumber-totalMemoryCount-len(wrongWords), len(wrongWords)))
                playWordAudio()
            else:
                announceLabel.config(text="You memorized {} words in {} words.(+{}/{}) {} words left".format(totalMemoryCount, wordNumber, newMemoryCount, len(wordKeys), len(wrongWords)))
                gettingWord = True
                if totalMemoryCount == wordNumber:
                    wordEntry.insert(0, "restart")
                else:
                    wordEntry.insert(0, "continue")
                wordLabel.config(text="")
                wordOriginLabel.config(text="")
                wordPageLabel.config(text="")
wordEntry.bind("<Return>", inputWord)

canvas.place(x=0,y=0,width=WINDOWWIDTH,height=20)
volumeBar.place(x=0,y=30,width=200,height=20)
volumeLabel.place(x=200,y=20,width=300,height=40)
countLabel.place(x=0,y=20,width=WINDOWWIDTH,height=40)
announceLabel.place(x=0,y=60,width=WINDOWWIDTH,height=100)
wordLabel.place(x=0,y=160,width=WINDOWWIDTH//2,height=100)
wordEntry.place(x=WINDOWWIDTH//2+20,y=190,width=WINDOWWIDTH//2-40,height=40)
wordListText.place(x=0,y=0,width=1080,height=250)
wordListScrollBar.place(x=1080,y=0,width=20,height=250)
wordListFrame.place(x=50,y=300,width=1100,height=250)
wordOriginLabel.place(x=50,y=550,width=950,height=50)
wordPageLabel.place(x=1000,y=550,width=150,height=50)

window.mainloop()