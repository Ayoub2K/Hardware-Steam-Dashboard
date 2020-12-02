from tkinter import *
import json

with open('steam.json') as jsonFile:
    data = json.load(jsonFile)

def list_data(key):
    list = []
    for i in data:
        list.append([i[key], i['name']])
    return list

def selectionSort(list):
    n = len(list)
    for i in range(n):
        minimum = i

        for j in range(i + 1, n):
            if (list[j] < list[minimum]):
                minimum = j

        list[i], list[minimum] = list[minimum], list[i]
        #temp = list[i]
        #list[i] = list[minimum]
        #list[minimum] = temp
    return list

def toonNaam():
    display.delete(1.0, END)
    sortedlist = selectionSort(list_data('name'))
    for i in sortedlist:
        display.insert(END, f'''{i[0]}\n''')

def toonPrijs():
    display.delete(1.0, END)
    sortedlist = selectionSort(list_data('price'))
    for i in sortedlist:
        display.insert(END, f'''€{i[0]} - {i[1]} \n''')

def toonDatum():
    display.delete(1.0, END)
    sortedlist = selectionSort(list_data('release_date'))
    for i in sortedlist:
        display.insert(END, f'''{i[0]} - {i[1]} \n''')

def toonPlaytime():
    display.delete(1.0, END)
    sortedlist = selectionSort(list_data('median_playtime'))
    for i in sortedlist:
        display.insert(END, f'''{i[0]} - {i[1]}\n''')



root = Tk()
root.title("Steam Dashboard")
root.geometry("950x600")

#de  display waarin data wordt weer gegeven
display = Text(root, background="#f0f0f0", height=21, width=50, font=("Helvetica", 14), pady=15)
display.place(x=350, y=85)

scroll_y = Scrollbar(root, orient="vertical", command=display.yview)
scroll_y.place(x=930, y=85, height=495, anchor='ne')

display.configure(yscrollcommand=scroll_y.set)


#knopen
buttonNaam = Button(master=root, text='Naam',background='#171a21', foreground='#FFFFFF', command=toonNaam)
buttonNaam.place(x=200, y=150, width=100)

buttonPrijs = Button(master=root, text='Prijs',background='#171a21', foreground='#FFFFFF', command=toonPrijs)
buttonPrijs.place(x=200, y=200, width=100)

buttonDatum = Button(master=root, text='Uitkomstdatum',background='#171a21', foreground='#FFFFFF', command=toonDatum)
buttonDatum.place(x=200, y=250, width=100)

buttonPlaytime = Button(master=root, text='gemidelde speeltijd',background='#171a21', foreground='#FFFFFF', command=toonPlaytime)
buttonPlaytime.place(x=200, y=300, width=100)

#Dashboard header
header = Label(master=root,
              text='Steam Dashboard',
              background='#171a21',
              foreground='#969696',
              font=('Helvetica', 16, 'bold italic'),
              width=74,
              height=3)
header.place(x=0, y=0)

root.mainloop()
