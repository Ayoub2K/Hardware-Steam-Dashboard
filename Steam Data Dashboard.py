from tkinter import *
import functies

def search():
    zoekwoord = str(Search.get())
    display.delete(1.0, END)
    naamlijst = (functies.search_data(zoekwoord))
    print(naamlijst)
    if naamlijst == None:
        display.insert(END, f'Die Game konden wij niet vinden!')
    elif zoekwoord in naamlijst:
        data = functies.search_data(zoekwoord)
        display.insert(END, f'''
Game: {data[0]} \n
prijs: €{data[4]} \n
Platform : {data[8]} \n
Publicatiedatum: {data[1]} \n
Ontwikkelaar: {data[2]} \n
Genre: {data[3]} \n
vereiste leeftijd: {data[5]} \n
Postieve reviews: {data[6]} \n
Negatieve reviews: {data[7]} \n
''')
    Search.delete(0, END)


def toonOwners():
    display.delete(1.0, END)
    sortedlist = functies.insertionSort(functies.list_data('owners'))
    for index in sortedlist:
        display.insert(END, f'''{index[0]} - {index[1]}\n''')

def toonPrijs():
    display.delete(1.0, END)
    sortedlist = functies.insertionSort(functies.list_data('price'))
    for index in sortedlist:
        display.insert(END, f'''€{index[0]} - {index[1]} \n''')

def GemiddeldePrijs():
    display.delete(1.0, END)
    gemPrijs = functies.gemiddelde(functies.list_int('price'))
    afgerond = round(gemPrijs, 2)
    display.insert(END, f'''De gemiddelde prijs van games : €{afgerond} \n''')

def RangePrijs():
    display.delete(1.0, END)
    RangePrijs = functies.Rng(functies.list_int('price'))
    display.insert(END, f'''De Range van prijzen : {RangePrijs} \n''')

def MediaanPrijs():
    display.delete(1.0, END)
    MediaanPrijs = functies.mediaan(functies.list_int('price'))
    display.insert(END, f'''De Mediaan van prijzen : €{MediaanPrijs} \n''')

def FreqOwner():
    display.delete(1.0, END)
    Owners = functies.frequentieOwner(functies.list_int('owners'))
    for key, value in Owners.items():
        display.insert(END, f'''{key} -> {value} \n''')


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
Search = Entry(master=root, width=50)
Search.place(x=50, y=100, width=150)

send = Button(master=root, text=' > ',background='#171a21', foreground='#FFFFFF', command=search)
send.place(x=200, y=100, width=50)

buttonOwners = Button(master=root, text='Owners',background='#171a21', foreground='#FFFFFF', command=toonOwners)
buttonOwners.place(x=50, y=150, width=200)

buttonPrijs = Button(master=root, text='Prijs',background='#171a21', foreground='#FFFFFF', command=toonPrijs)
buttonPrijs.place(x=50, y=200, width=200)

buttonGemPrijs = Button(master=root, text='Gemidelde Prijs',background='#171a21', foreground='#FFFFFF', command=GemiddeldePrijs)
buttonGemPrijs.place(x=50, y=250, width=200)

buttonRange = Button(master=root, text='Range Prijs',background='#171a21', foreground='#FFFFFF', command=RangePrijs)
buttonRange.place(x=50, y=300, width=200)

buttonMediaanPrijs = Button(master=root, text='Mediaan Prijs',background='#171a21', foreground='#FFFFFF', command=MediaanPrijs)
buttonMediaanPrijs.place(x=50, y=350, width=200)

buttonOwnerFrequentie = Button(master=root, text='Frequentie Owner',background='#171a21', foreground='#FFFFFF', command=FreqOwner)
buttonOwnerFrequentie.place(x=50, y=400, width=200)

buttonStaafdiagram = Button(master=root, text='Frequentie Owner Diagram',background='#171a21', foreground='#FFFFFF', command=FreqOwner)
buttonStaafdiagram.place(x=50, y=450, width=200)

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
