import tkinter, tkinter.font, os, subprocess
from tkinter import filedialog
window = tkinter.Tk()

window.title("MainMenu")
window.geometry("640x400+50+50")
window.resizable(False, False)
PLAYPATH = os.path.dirname(os.path.abspath(__file__))
audioDirPath = os.path.join(PLAYPATH, "audio")
if not os.path.exists(audioDirPath):
    os.makedirs(audioDirPath)

paperlogy6 = tkinter.font.Font(family="Paperlogy 6 SemiBold", size=16)
paperlogy5 = tkinter.font.Font(family="Paperlogy 5 Medium", size=12)

fileFrame = tkinter.Frame(window)
fileScrollBar = tkinter.Scrollbar(fileFrame)
fileText = tkinter.Text(fileFrame, font=paperlogy5, yscrollcommand=fileScrollBar.set, state="disabled")
fileScrollBar.config(command=fileText.yview)
fileFrame.place(x=20,y=80,width=600,height=300)
fileText.place(x=0,y=0,width=580,height=300)
fileScrollBar.place(x=580,y=0,width=20,height=300)

fileChooseButton = tkinter.Button(window, text="file choose", font=paperlogy6)
fileNames = []
def choosingButton():
    global fileNames
    if os.path.exists(os.path.join(PLAYPATH, "data")):
        fileNames = list(filedialog.askopenfilenames(initialdir=os.path.join(PLAYPATH, "data"), filetypes=(("text file","*.txt*"),)))
    else:
        fileNames = list(filedialog.askopenfilenames(initialdir=PLAYPATH, filetypes=(("text file","*.txt*"),)))
    fileText.config(state="normal")
    fileText.delete("1.0",tkinter.END)
    fileText.insert("1.0", "\n".join(fileNames))
    fileText.config(state="disabled")
fileChooseButton.config(command=choosingButton)
fileChooseButton.place(x=20,y=20,height=40,width=200)

startButton = tkinter.Button(window, text="START", font=paperlogy6)
def start():
    if len(fileNames) != 0:
        with open("option.txt", "w+", encoding="UTF8") as file:
            file.writelines("\n".join(fileNames))
        subprocess.Popen(["python", "testing.py"])
startButton.config(command=start)
startButton.place(x=420,y=20,height=40,width=200)

window.mainloop()