from tkinter import *
import functies as fc
import API
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
    sortedlist = fc.mergeSort(fc.list_data('required_age'))
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


def toon_gametijd():
    destroy()
    display_2.delete(1.0, END)
    display_2.insert(END, f'''{API.naam(steam_id[0])} heeft totaal {API.totale_gametijd(steam_id[0])} uur gegamed!\n''')


def toon_owned_games():
    destroy()
    display_2.delete(1.0, END)
    display_2.insert(END, f'''{API.naam(steam_id[0])} heeft de volgende games:\n\n{API.owned_games(steam_id[0])}\n''')


def raise_frame(frame):
    display.delete(1.0, END)
    display_2.delete(1.0, END)
    frame.tkraise()
    frame_header.tkraise()


def get_steam_id():
    raise_frame(frame_1)
    steam_id.clear()
    steam_id.append(steam_id_entry.get())
    steam_id_entry.delete(0, 'end')
    steam_id_info.config(text=f'nu in gebruik:\n{steam_id[0]}\n{API.naam(steam_id[0])}')


steam_id = []  #steam id: 76561198169107517

root = Tk()
root.title("Steam Dashboard")
root.geometry("950x600")

frame_2 = Frame(master=root)
frame_2.place(x=0, y=0, width=950, height=600)

frame_1 = Frame(master=root)
frame_1.place(x=0, y=0, width=950, height=600)

steam_id_frame = Frame(master=root)
steam_id_frame.place(x=0, y=0, width=950, height=600)

frame_header = Frame(master=root)
frame_header.place(x=0, y=0, width=950, height=80)


#steam id scherm waar je steam id wordt gevraagd
uitleg = Label(master=steam_id_frame, text='Vul hier je Steam id in:')
uitleg.place(x=400, y=270, width=150, height=25)

steam_id_entry = Entry(master=steam_id_frame, width=50)
steam_id_entry.place(x=400, y=300, width=150, height=25)

ingevuld = Button(master=steam_id_frame, text='Volgende',background='#171a21', foreground='#FFFFFF', command=get_steam_id)
ingevuld.place(x=400, y=330, width=150, height=25)

insturcties = Label(master=steam_id_frame, text="Om je steam id te krijgen ga je vanaf je bibliotheek naar:\nBeeld"
                                                " (links boven) > instellingen > vink het vakje met 'Steam adresbalk "
                                                "weergeven indien beschikbaar' aan >\nOK > ga naar je profiel > links "
                                                "boven zie je een link en daar staat je steam id tussen")
insturcties.place(y=550, x=190)


# de display waarin data wordt weer gegeven
display = Text(frame_1, background="#f0f0f0", height=21, width=50, font=("Helvetica", 14), pady=15)
display.place(x=350, y=85)

scroll_y = Scrollbar(frame_1, orient="vertical", command=display.yview)
scroll_y.place(x=930, y=85, height=495, anchor='ne')

display.configure(yscrollcommand=scroll_y.set)


#knopen
Search = Entry(master=frame_1, width=50)
Search.place(x=50, y=100, width=150, height=25)

send = Button(master=frame_1, text=' > ',background='#171a21', foreground='#FFFFFF', command=search)
send.place(x=200, y=100, width=50)

buttonOwners = Button(master=frame_1, text='required age',background='#171a21', foreground='#FFFFFF', command=toonOwners)
buttonOwners.place(x=50, y=150, width=200)

buttonPrijs = Button(master=frame_1, text='Prijs',background='#171a21', foreground='#FFFFFF', command=toonPrijs)
buttonPrijs.place(x=50, y=180, width=200)

buttonGemPrijs = Button(master=frame_1, text='Gemidelde Prijs',background='#171a21', foreground='#FFFFFF', command=GemiddeldePrijs)
buttonGemPrijs.place(x=50, y=230, width=200)

buttonRange = Button(master=frame_1, text='Range Prijs',background='#171a21', foreground='#FFFFFF', command=RangePrijs)
buttonRange.place(x=50, y=260, width=200)

buttonMediaanPrijs = Button(master=frame_1, text='Mediaan Prijs',background='#171a21', foreground='#FFFFFF', command=MediaanPrijs)
buttonMediaanPrijs.place(x=50, y=290, width=200)

buttonOwnerFrequentie = Button(master=frame_1, text='Frequentie Owner',background='#171a21', foreground='#FFFFFF', command=FreqOwner)
buttonOwnerFrequentie.place(x=50, y=340, width=200)

buttonStaafdiagram = Button(master=frame_1, text='Owner Diagram',background='#171a21', foreground='#FFFFFF', command=open_imgowner)
buttonStaafdiagram.place(x=50, y=370, width=200)

buttonLeeftijdFrequentie = Button(master=frame_1, text='Frequentie minimum Leeftijd',background='#171a21', foreground='#FFFFFF', command=FreqLeeftijd)
buttonLeeftijdFrequentie.place(x=50, y=430, width=200)
buttonModusleeftijd = Button(master=frame_1, text='Modus minimum Leeftijd',background='#171a21', foreground='#FFFFFF', command=modusLeeftijd)
buttonModusleeftijd.place(x=50, y=460, width=200)
buttonVarleeftijd = Button(master=frame_1, text='Variatie minimum Leeftijd',background='#171a21', foreground='#FFFFFF', command=variatieLeeftijd)
buttonVarleeftijd.place(x=50, y=490, width=200)

img = Image.open("grafiekowner.png")
img = img.resize((650, 500), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
panel = Label(frame_1, image=img)
panel.image = img

#Dashboard header
header = Label(master=frame_header,
              text='Steam Dashboard',
              background='#171a21',
              foreground='#969696',
              font=('Helvetica', 16, 'bold italic'),
              width=74,
              height=3)
header.place(x=0, y=0)

button_switch = Button(master=frame_1, text='Volgend scherm', background='#171a21', foreground='#FFFFFF', command=lambda:raise_frame(frame_2))
button_switch.place(x=50, y=530, width=200)

button_terug = Button(master=frame_2, text='Terug', background='#171a21', foreground='#FFFFFF', command=lambda:raise_frame(frame_1))
button_terug.place(x=50, y=530, width=200)

# de display van frame 2
display_2 = Text(frame_2, background="#f0f0f0", height=21, width=50, font=("Helvetica", 14), pady=15)
display_2.place(x=350, y=85)

scroll_y = Scrollbar(frame_2, orient="vertical", command=display_2.yview)
scroll_y.place(x=930, y=85, height=495, anchor='ne')

display_2.configure(yscrollcommand=scroll_y.set)

steam_id_info = Label(master=frame_2, text='')
steam_id_info.place(x=50, y=90, width=200)

button_veranderen = Button(master=frame_2, text='Verander',background='#171a21', foreground='#FFFFFF', command=lambda:raise_frame(steam_id_frame))
button_veranderen.place(x=50, y=140, width=200)

button_gametijd = Button(master=frame_2, text='Totale gametijd',background='#171a21', foreground='#FFFFFF', command=toon_gametijd)
button_gametijd.place(x=50, y=190, width=200)

button_owned_games = Button(master=frame_2, text='Owned games',background='#171a21', foreground='#FFFFFF', command=toon_owned_games)
button_owned_games.place(x=50, y=220, width=200)

root.mainloop()
