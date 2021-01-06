from tkinter import *
import json

with open('steam.json') as jsonFile:
    data = json.load(jsonFile)

def list_data(key):
    list = []
    for index in data:
        list.append([index[key], index['name']])
    return list

def search_data(zoekwoord):
    list = []
    for index in data:
        list.append([index['name'], index['release_date'], index['developer'], index['genres'], index['price'], index['required_age'], index['positive_ratings'], index['negative_ratings'], index['platforms']])
    for i in list:
        if zoekwoord == i[0]:
            return i
        else:
            return '0'

def search():
    zoekwoord = str(Search.get())
    display.delete(1.0, END)
    if zoekwoord in (search_data(zoekwoord)):
        data = search_data(zoekwoord)
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
    else:
        display.insert(END, f'Die game konden wij niet vinden!')
    Search.delete(0, END)

def list_int(key):
    list = []
    for index in data:
        getal = index[key]
        list.append(getal)
    return list

def insertionSort(list):
    for index in range(1, len(list)):
        key = list[index]
        j = index - 1
        while j >= 0 and key < list[j]:
            list[j + 1] = list[j]
            j -= 1
        list[j + 1] = key
    return list


def gemiddelde(lst):
    som = 0
    for num in lst:
        som += num

    gem = som / len(lst)
    return gem

def Rng(lst):
    laagte = lst[0]
    hoogste = lst[0]

    for getal in lst:
        if getal < laagte:
            laagte = getal

    for getal in lst:
        if getal > hoogste:
            hoogste = getal

    verschil = hoogste - laagte
    return verschil

def mediaan(lst):
    lst.sort()
    index = (len(lst) - 1) // 2

    if (len(lst) % 2):
        return lst[index]
    else:
        return (lst[index] + lst[index + 1]) / 2.0

def frequentieOwner(lst):
    freqDict = {
        '0-20000': 0,
        '20000-50000': 0,
        '50000-100000': 0,
        '100000-200000': 0,
        '200000-500000': 0,
        '500000-1000000': 0,
        '1000000-2000000': 0,
        '2000000-5000000': 0,
        '5000000-10000000': 0,
        '10000000-20000000': 0,
        '20000000-50000000': 0,
        '50000000-100000000': 0,
        '100000000-200000000': 0,
    }
    for i in lst:
        if i == '100000000-200000000':
            freqDict['100000000-200000000'] += 1
        elif i == '50000000-100000000':
            freqDict['50000000-100000000'] += 1
        elif i == '20000000-50000000':
            freqDict['20000000-50000000'] += 1
        elif i == '10000000-20000000':
            freqDict['10000000-20000000'] += 1
        elif i == '5000000-10000000':
            freqDict['5000000-10000000'] += 1
        elif i == "2000000-5000000":
            freqDict['2000000-5000000'] += 1
        elif i == '1000000-2000000':
            freqDict['1000000-2000000'] += 1
        elif i == "500000-1000000":
            freqDict['500000-1000000'] += 1
        elif i == "200000-500000":
            freqDict['200000-500000'] += 1
        elif i == '100000-200000':
            freqDict['100000-200000'] += 1
        elif i == '50000-100000':
            freqDict['50000-100000'] += 1
        elif i == '20000-50000':
            freqDict['20000-50000'] += 1
        elif i == '0-20000':
            freqDict['0-20000'] += 1
    return freqDict


def toonOwners():
    display.delete(1.0, END)
    sortedlist = insertionSort(list_data('owners'))
    for index in sortedlist:
        display.insert(END, f'''{index[0]} - {index[1]}\n''')

def toonPrijs():
    display.delete(1.0, END)
    sortedlist = insertionSort(list_data('price'))
    for index in sortedlist:
        display.insert(END, f'''€{index[0]} - {index[1]} \n''')

def GemiddeldePrijs():
    display.delete(1.0, END)
    gemPrijs = gemiddelde(list_int('price'))
    afgerond = round(gemPrijs, 2)
    display.insert(END, f'''De gemiddelde prijs van games : €{afgerond} \n''')

def RangePrijs():
    display.delete(1.0, END)
    RangePrijs = Rng(list_int('price'))
    display.insert(END, f'''De Range van prijzen : {RangePrijs} \n''')

def MediaanPrijs():
    display.delete(1.0, END)
    MediaanPrijs = mediaan(list_int('price'))
    display.insert(END, f'''De Mediaan van prijzen : €{MediaanPrijs} \n''')

def FreqOwner():
    display.delete(1.0, END)
    Owners = frequentieOwner(list_int('owners'))
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
Search.place(x=50, y=100, width=150, height=25)

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
