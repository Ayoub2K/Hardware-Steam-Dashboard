from tkinter import *
import functies as fc
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

Owners = fc.frequentieOwner(fc.list_int('owners'))
plt.barh(list(Owners.keys()), Owners.values(), color='#171a21', alpha=0.8)
plt.title('Hoeveel owners 1 game heeft')
plt.tight_layout()
plt.savefig('grafiekowner.png', dpi=100)

def FreqOwner():
    destroy()
    display.delete(1.0, END)
    Owners = fc.frequentieOwner(fc.list_int('owners'))
    for key, value in Owners.items():
        display.insert(END, f'''   {key} -> {value} \n''')

def FreqLeeftijd():
    destroy()
    display.delete(1.0, END)
    Leeftijd = fc.frequentieLeeftijd(fc.list_int('required_age'))
    for key, value in Leeftijd.items():
        display.insert(END, f'''  {key} -> {value} \n''')

def open_imgowner():
    panel.place(x=250, y=85)

def destroy():
    panel.place_forget()


def search():
    destroy()
    display.delete(1.0, END)
    zoekwoord = str(Search.get())
    naamlijst = (fc.search_data(zoekwoord))

    if naamlijst == None:
        display.insert(END, f'Die Game konden wij niet vinden!')
    elif zoekwoord in naamlijst:
        data = fc.search_data(zoekwoord)
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
    destroy()
    display.delete(1.0, END)
    sortedlist = fc.mergeSort(fc.list_data('owners'))
    for index in sortedlist:
        display.insert(END, f'''{index[0]} - {index[1]}\n''')

def toonPrijs():
    destroy()
    display.delete(1.0, END)
    sortedlist = fc.mergeSort(fc.list_data('price'))
    for index in sortedlist:
        display.insert(END, f'''€{index[0]} - {index[1]} \n''')

def GemiddeldePrijs():
    destroy()
    display.delete(1.0, END)
    gemPrijs = fc.gemiddelde(fc.list_int('price'))
    afgerond = round(gemPrijs, 2)
    display.insert(END, f'''De gemiddelde prijs van games : €{afgerond} \n''')

def RangePrijs():
    destroy()
    display.delete(1.0, END)
    RangePrijs = fc.Rng(fc.list_int('price'))
    display.insert(END, f'''De Range van prijzen : {RangePrijs} \n''')

def MediaanPrijs():
    destroy()
    display.delete(1.0, END)
    MediaanPrijs = fc.mediaan(fc.list_int('price'))
    display.insert(END, f'''De Mediaan van prijzen : €{MediaanPrijs} \n''')

def modusLeeftijd():
    destroy()
    display.delete(1.0, END)
    values = list(fc.frequentieLeeftijd(fc.list_int('required_age')).values())
    hoogsteValue = max(values)
    modi = []
    for key, value in fc.frequentieLeeftijd(fc.list_int('required_age')).items():
        if value >= hoogsteValue:
            modi.append(key)
    display.insert(END, f'''De Mediaan van het minimum leeftijd = {modi} \n''')

def variatieLeeftijd():
    destroy()
    display.delete(1.0, END)
    gemideld = fc.gemiddelde(fc.list_int('required_age'))
    samen = []
    for i in fc.list_int('required_age'):
        i -= gemideld
        samen.append(i ** 2)
    variatie = sum(samen) / len(samen)
    display.insert(END, f'''De Variatie van het minimum leeftijd = {variatie} \n''')


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
buttonPrijs.place(x=50, y=180, width=200)

buttonGemPrijs = Button(master=root, text='Gemidelde Prijs',background='#171a21', foreground='#FFFFFF', command=GemiddeldePrijs)
buttonGemPrijs.place(x=50, y=230, width=200)

buttonRange = Button(master=root, text='Range Prijs',background='#171a21', foreground='#FFFFFF', command=RangePrijs)
buttonRange.place(x=50, y=260, width=200)

buttonMediaanPrijs = Button(master=root, text='Mediaan Prijs',background='#171a21', foreground='#FFFFFF', command=MediaanPrijs)
buttonMediaanPrijs.place(x=50, y=290, width=200)

buttonOwnerFrequentie = Button(master=root, text='Frequentie Owner',background='#171a21', foreground='#FFFFFF', command=FreqOwner)
buttonOwnerFrequentie.place(x=50, y=340, width=200)

buttonStaafdiagram = Button(master=root, text='Owner Diagram',background='#171a21', foreground='#FFFFFF', command=open_imgowner)
buttonStaafdiagram.place(x=50, y=370, width=200)

buttonLeeftijdFrequentie = Button(master=root, text='Frequentie minimum Leeftijd',background='#171a21', foreground='#FFFFFF', command=FreqLeeftijd)
buttonLeeftijdFrequentie.place(x=50, y=430, width=200)
buttonModusleeftijd = Button(master=root, text='Modus minimum Leeftijd',background='#171a21', foreground='#FFFFFF', command=modusLeeftijd)
buttonModusleeftijd.place(x=50, y=460, width=200)
buttonVarleeftijd = Button(master=root, text='Variatie minimum Leeftijd',background='#171a21', foreground='#FFFFFF', command=variatieLeeftijd)
buttonVarleeftijd.place(x=50, y=490, width=200)

img = Image.open("grafiekowner.png")
img = img.resize((650, 500), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
panel = Label(root, image=img)
panel.image = img

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
