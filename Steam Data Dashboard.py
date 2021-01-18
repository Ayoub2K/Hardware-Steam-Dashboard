from tkinter import *
import functies as fc
import API
import os
import RPi.GPIO as GPIO
import time
from PIL import ImageTk
from PIL import Image
from datetime import datetime
import matplotlib.pyplot as plt

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0\n')
    os.environ.__setitem__('DISPLAY', ':0.0')

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( 0 )

switch = 23
sr04_trig = 24
sr04_echo = 25
servo = 18
clock_pin = 20
data_pin = 21
shift_clock_pin = 5
latch_clock_pin = 6
data_pin_schuifregelaar = 13

rood = [0, 0, 255]
oranje = [0, 150, 255]
groen = [0, 255, 0]

GPIO.setup( switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
GPIO.setup( sr04_trig, GPIO.OUT )
GPIO.setup( sr04_echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
GPIO.setup(servo, GPIO.OUT)
GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(data_pin, GPIO.OUT)
GPIO.setup( shift_clock_pin, GPIO.OUT )
GPIO.setup( latch_clock_pin, GPIO.OUT )
GPIO.setup( data_pin_schuifregelaar, GPIO.OUT )


def hc595(aantal_online):
    for i in range(8):
        if aantal_online > 0:
            GPIO.output(data_pin_schuifregelaar, GPIO.HIGH)
            aantal_online = aantal_online - 1
        else:
            GPIO.output(data_pin_schuifregelaar, GPIO.LOW)
        GPIO.output(shift_clock_pin, GPIO.HIGH)
        GPIO.output(shift_clock_pin, GPIO.LOW)
    GPIO.output(latch_clock_pin, GPIO.HIGH)
    GPIO.output(latch_clock_pin, GPIO.LOW)
    time.sleep(0.1)


def led_strip_uit():
    for i in range(4):
        apa102_send_bytes([0, 0, 0, 0, 0, 0, 0, 0])
    for i in range(8):
        apa102_send_bytes([1, 1, 1, 1, 1, 1, 1, 1])
        for i in range(3):
            apa102_send_bytes([0, 0, 0, 0, 0, 0, 0, 0])
    for i in range(4):
        apa102_send_bytes([1, 1, 1, 1, 1, 1, 1, 1])


def apa102_send_bytes(bytes):
    for bit in bytes:
        if bit == 1:
            GPIO.output(data_pin, GPIO.HIGH)
        elif bit == 0:
            GPIO.output(data_pin, GPIO.LOW)
        GPIO.output(clock_pin, GPIO.HIGH)
        GPIO.output(clock_pin, GPIO.LOW)
    time.sleep(0.003)

            

def apa102(colors):
    for i in range(4):
        apa102_send_bytes([0, 0, 0, 0, 0, 0, 0, 0])
    for color in colors:
        apa102_send_bytes([1, 1, 1, 1, 1, 1, 1, 1])
        for kleur in color:
            bits = []
            for i in range(8):
                if kleur % 2 == 1:
                    bits.append(1)
                else:
                    bits.append(0)
                kleur = kleur // 2
            apa102_send_bytes(bits)
    for i in range(4):
        apa102_send_bytes([1, 1, 1, 1, 1, 1, 1, 1])

       


def kleuren(aantal_uren_gametijd):
    if aantal_uren_gametijd >= 1000:
        colors = []
        for i in range(8):
            colors.append(rood)
    else:
        colors = []
        aantal = aantal_uren_gametijd
        for i in range(8):
            if aantal == 0:
                colors.append(groen)
            elif aantal < 125:
                colors.append(oranje)
                aantal = 0
            elif aantal > 125:
                colors.append(rood)
                aantal = aantal - 125
    apa102(colors)



def pulse( pin, delay1, delay2 ):
   GPIO.output(pin, GPIO.HIGH)
   time.sleep(delay1)
   GPIO.output(pin, GPIO.LOW)
   time.sleep(delay2)

def servo_pulse( pin_nr, aantal_uren_gametijd ):
    position = aantal_uren_gametijd
    pos1 = 0.0005 + (0.002/100*position)
    pos2 = 0.02
    pulse(pin_nr, pos1, pos2)

def sr04( trig_pin, echo_pin ):
   GPIO.output(trig_pin, GPIO.HIGH)

   time.sleep(0.00001)
   GPIO.output(trig_pin, GPIO.LOW)

   starttime = time.time_ns()
   while GPIO.input(echo_pin) == False:
      starttime = time.time_ns()

   endtime = time.time_ns()
   while GPIO.input(echo_pin) == True:
      endtime = time.time_ns()

   heenenweer = (endtime - starttime) / 2
   afstand = (heenenweer * 343)
   afstandCentimeter = (afstand / 10000000)
   return afstandCentimeter



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


def punt_naar_komma(getal):
    getal = str(getal)
    getal = getal.replace('.', ',')
    return getal


def toon_required_age():
    destroy()
    display.delete(1.0, END)
    sortedlist = fc.mergeSort(fc.list_data('required_age'))
    for index in sortedlist:
        display.insert(END, f'''{index[0]} - {index[1]}\n''')
    if sr04(sr04_trig, sr04_echo) < 7.5:
        display.see('end')


def toonPrijs():
    destroy()
    display.delete(1.0, END)
    sortedlist = fc.mergeSort(fc.list_data('price'))
    for index in sortedlist:
        display.insert(END, f'''€{punt_naar_komma(index[0])} - {index[1]} \n''')
    if sr04(sr04_trig, sr04_echo) < 7.5:
        display.see('end')


def GemiddeldePrijs():
    destroy()
    display.delete(1.0, END)
    gemPrijs = fc.gemiddelde(fc.list_int('price'))
    afgerond = round(gemPrijs, 2)
    display.insert(END, f'''De gemiddelde prijs van games : €{punt_naar_komma(afgerond)} \n''')

def RangePrijs():
    destroy()
    display.delete(1.0, END)
    RangePrijs = fc.Rng(fc.list_int('price'))
    display.insert(END, f'''De Range van prijzen : {punt_naar_komma(RangePrijs)} \n''')

def MediaanPrijs():
    destroy()
    display.delete(1.0, END)
    MediaanPrijs = fc.mediaan(fc.list_int('price'))
    display.insert(END, f'''De Mediaan van prijzen : €{punt_naar_komma(MediaanPrijs)} \n''')

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
    led_strip_uit()
    totale_gametijd = API.totale_gametijd(steam_id[0])
    gametijd = round(totale_gametijd /10)
    for i in range(0, gametijd, 1):
        servo_pulse(servo, i)
    kleuren(totale_gametijd)
    destroy()
    display_2.delete(1.0, END)
    display_2.insert(END, f'''{API.naam(steam_id[0])} heeft totaal {punt_naar_komma(totale_gametijd)} uur gegamed!\n''')


def toon_owned_games():
    led_strip_uit()
    destroy()
    display_2.delete(1.0, END)
    display_2.insert(END, f'''{API.naam(steam_id[0])} heeft de volgende games:\n\n{API.owned_games(steam_id[0])}\n''')


def raise_frame(frame):
    display.delete(1.0, END)
    display_2.delete(1.0, END)
    led_strip_uit()
    frame.tkraise()
    frame_header.tkraise()


def get_steam_id():
    raise_frame(frame_1)
    hc595(0)
    steam_id.clear()
    steam_id.append(steam_id_entry.get())
    steam_id_entry.delete(0, 'end')
    if steam_id[0] == '':
        steam_id_info.config(text='Geen steam id ingevuld')
    else:
        steam_id_info.config(text=f'nu in gebruik:\n{steam_id[0]}\n{API.naam(steam_id[0])}')


def toon_vrienden_online():
    led_strip_uit()
    destroy()
    display_2.delete(1.0, END)
    vrienden_lijst = API.vrienden_online(steam_id[0])
    display_2.insert(END, f'''De volgende mensen zijn online:\n\n''')
    aantal_online = 0
    regel = 3
    for index in vrienden_lijst:
        if index[1] == 1:
            aantal_online = aantal_online + 1
            display_2.insert(END, f'''{index[0]} -> online\n''')
            begin = len(index[0]) + 4
            display_2.tag_add("online", f'{regel}.{begin}', f'{regel}.{begin + 6}')
            display_2.tag_config("online", foreground="green")
        if index[1] == 0:
            display_2.insert(END, f'''{index[0]} -> offline\n''')
            begin = len(index[0]) + 4
            display_2.tag_add("offline", f'{regel}.{begin}', f'{regel}.{begin + 7}')
            display_2.tag_config("offline", foreground="red")
        if index[1] == 3:
            display_2.insert(END, f'''{index[0]} -> afwezig\n''')
            begin = len(index[0]) + 4
            display_2.tag_add("afwezig", f'{regel}.{begin}', f'{regel}.{begin + 7}')
            display_2.tag_config("afwezig", foreground="orange")
        regel = regel + 1
    display_2.insert(END, f'''\nEr zijn {aantal_online} mensen online!\n''')
    if aantal_online <= 8:
        hc595(aantal_online)
    else:
        hc595(8)


def toon_recently_played():
    led_strip_uit()
    destroy()
    display_2.delete(1.0, END)
    info = API.recently_played(steam_id[0])
    display_2.insert(END, f'''{API.naam(steam_id[0])} heeft recent {info[0]} verschillende games gespeeld, Namelijk:\n\n''')
    for game in info[1]:
        display_2.insert(END, f'''{game}\n''')


def toon_account_aangemaakt():
    led_strip_uit()
    destroy()
    display_2.delete(1.0, END)
    tijd_aanmaak = API.account_aangemaakt(steam_id[0])
    tijd_nu = datetime.now()
    display_2.insert(END, f'''{API.naam(steam_id[0])} heeft zijn/haar account aangemaakt op: {tijd_aanmaak.tm_mday}-{tijd_aanmaak.tm_mon}-{tijd_aanmaak.tm_year}\n\n''')
    tijd = f'{tijd_aanmaak.tm_year}-{tijd_aanmaak.tm_mon}-{tijd_aanmaak.tm_mday} {tijd_aanmaak.tm_hour}:{tijd_aanmaak.tm_min}:{tijd_aanmaak.tm_sec}'
    tijd_aanmaak = datetime.strptime(tijd, '%Y-%m-%d %H:%M:%S')
    tijd_tussen = tijd_nu - tijd_aanmaak
    dagen = tijd_tussen.days
    jaar = int(dagen / 365)
    dagen = dagen - jaar * 365
    maand = int(dagen / 30)
    dagen = dagen - maand * 30
    sec = tijd_tussen.seconds
    uur = int(sec / 60 / 60)
    sec = sec - uur * 60 * 60
    min = int(sec / 60)
    sec = sec - min * 60
    display_2.insert(END, f'''Om precies te zijn: {jaar} jaar, {maand} maanden, {dagen} dagen, {uur} uren,\n{min} minuten, {sec} seconden geleden!''')


# hier wordt het ingevoerde steam id opgeslagen
steam_id = []  #steam id: 76561198169107517, 76561198099842424


# dit is voor de grafiek
Owners = fc.frequentieOwner(fc.list_int('owners'))
plt.barh(list(Owners.keys()), list(Owners.values()), color='#171a21', alpha=0.8)
plt.title('Hoeveel owners 1 game heeft')
plt.tight_layout()
plt.savefig('grafiekowner.png', dpi=100)


# Tkinter scherm
root = Tk()
root.title("Steam Dashboard")
root.geometry("950x600")

# de verschillende frames
frame_2 = Frame(master=root)
frame_2.place(x=0, y=0, width=950, height=600)

frame_1 = Frame(master=root)
frame_1.place(x=0, y=0, width=950, height=600)

steam_id_frame = Frame(master=root)
steam_id_frame.place(x=0, y=0, width=950, height=600)

frame_header = Frame(master=root)
frame_header.place(x=0, y=0, width=950, height=80)


# steam id scherm waar je steam id wordt gevraagd
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
insturcties.place(y=550, x=115)


# de display van scherm 1 waarin data wordt weer gegeven
display = Text(frame_1, background="#f0f0f0", height=21, width=50, font=("Helvetica", 14), pady=15)
display.place(x=350, y=85)

scroll_y = Scrollbar(frame_1, orient="vertical", command=display.yview)
scroll_y.place(x=930, y=85, height=475, anchor='ne')

display.configure(yscrollcommand=scroll_y.set)


# frame 1
Search = Entry(master=frame_1, width=50)
Search.place(x=50, y=100, width=150, height=25)

send = Button(master=frame_1, text=' > ',background='#171a21', foreground='#FFFFFF', command=search)
send.place(x=200, y=100, width=50)

buttonOwners = Button(master=frame_1, text='required age',background='#171a21', foreground='#FFFFFF', command=toon_required_age)
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
              background='#24282f',
              foreground='#969696',
              font=('Helvetica', 16, 'bold italic'),
              width=80,
              height=3)
header.place(x=0, y=0)

img2 = Image.open("Steam-Logo.png")
img2 = img2.resize((80, 50), Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(img2)

steam_logo = Label(master=frame_header, image=img2, background='#24282f')
steam_logo.image = img2
steam_logo.place(x=310, y=15)



# wisselen tussen schermen
button_switch = Button(master=frame_1, text='Volgend scherm', background='#171a21', foreground='#FFFFFF', command=lambda:raise_frame(frame_2))
button_switch.place(x=50, y=530, width=200)

button_terug = Button(master=frame_2, text='Terug', background='#171a21', foreground='#FFFFFF', command=lambda:raise_frame(frame_1))
button_terug.place(x=50, y=530, width=200)

button_veranderen = Button(master=frame_2, text='Verander',background='#171a21', foreground='#FFFFFF', command=lambda:raise_frame(steam_id_frame))
button_veranderen.place(x=50, y=145, width=200)


# de display van scherm 2 waarin data wordt weer gegeven
display_2 = Text(frame_2, background="#f0f0f0", height=21, width=50, font=("Helvetica", 14), pady=15)
display_2.place(x=350, y=85)

scroll_y = Scrollbar(frame_2, orient="vertical", command=display_2.yview)
scroll_y.place(x=930, y=85, height=475, anchor='ne')

display_2.configure(yscrollcommand=scroll_y.set)


# frame 2
steam_id_info = Label(master=frame_2, text='')
steam_id_info.place(x=50, y=90, width=200)

button_gametijd = Button(master=frame_2, text='Totale gametijd',background='#171a21', foreground='#FFFFFF', command=toon_gametijd)
button_gametijd.place(x=50, y=220, width=200)

button_recently_played = Button(master=frame_2, text='Recent gespeeld',background='#171a21', foreground='#FFFFFF', command=toon_recently_played)
button_recently_played.place(x=50, y=255, width=200)

button_owned_games = Button(master=frame_2, text='Owned games',background='#171a21', foreground='#FFFFFF', command=toon_owned_games)
button_owned_games.place(x=50, y=290, width=200)

button_online_vrienden = Button(master=frame_2, text='Online vrienden',background='#171a21', foreground='#FFFFFF', command=toon_vrienden_online)
button_online_vrienden.place(x=50, y=360, width=200)

button_datum_aanmaak = Button(master=frame_2, text='datum van aanmaak',background='#171a21', foreground='#FFFFFF', command=toon_account_aangemaakt)
button_datum_aanmaak.place(x=50, y=430, width=200)


# start knop
print('Ready to start Program')
while True:
    if (GPIO.input(switch)):
        print('program started!')
        break

# tkinter loop
root.mainloop()

# lampjes uit
led_strip_uit()
hc595(0)
