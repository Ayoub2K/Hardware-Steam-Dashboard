from tkinter import *
import json

with open('steam.json') as jsonFile:
    data = json.load(jsonFile)

    sortedList = sorted(data, key=lambda x: x['release_date'])
    EersteItem = data[0]['name']

print(sortedList[-1])


root = Tk()
root.title("Steam Dashboard")
root.geometry("950x600")

#de  display waarin data wordt weer gegeven
display = Text(root, background="#f0f0f0", height=18, font=("Helvetica", 16), pady=20)
display.grid(row=1, column=0)
display.insert(END, f'''Naam van eerste item in .Json bestand: {EersteItem} \n\n''')
display.insert(END, f'''Nieuwste game op Steam: {sortedList[-1]['name']}\nRelease: {sortedList[-1]['release_date']}\n\n''')
display.insert(END, f'''Oudste game op Steam: {sortedList[0]['name']}\nRelease: {sortedList[0]['release_date']}\n\n''')
#Dashboard header
header = Label(master=root,
              text='Steam Dashboard',
              background='#171a21',
              foreground='#969696',
              font=('Helvetica', 16, 'bold italic'),
              width=74,
              height=3)
header.grid(row=0, column=0)

root.mainloop()