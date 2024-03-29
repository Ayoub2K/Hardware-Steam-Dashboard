import json

with open('steam.json') as jsonFile:
    data = json.load(jsonFile)

def list_data(key):
    list = []
    for index in data:
        list.append([index[key], index['name']])
    return list

def search_data(naam):
    list = []
    for index in data:
        list.append([index['name'], index['release_date'], index['developer'], index['genres'], index['price'], index['required_age'], index['positive_ratings'], index['negative_ratings'], index['platforms']])
    for i in list:
        if naam == i[0]:
            return i

def list_int(key):
    list = []
    for index in data:
        getal = index[key]
        list.append(getal)
    return list

# def insertionSort(list):
#     for index in range(1, len(list)):
#         key = list[index]
#         j = index - 1
#         while j >= 0 and key < list[j]:
#             list[j + 1] = list[j]
#             j -= 1
#         list[j + 1] = key
#     return list

def mergeSort(list):
    if len(list) > 1:
        #sorteer lijst in 2 helften
        mid = len(list) // 2
        links = list[:mid]
        rechts = list[mid:]
        #sorteer linker helft
        mergeSort(links)
        #sorteer rechter helft
        mergeSort(rechts)

        #variabelen bepalen
        lenLinks = len(links)
        lenRechts = len(rechts)
        linksIter = 0
        rechtsIter= 0
        mainlistIterator= 0
        
        #kopiert data van Linker en Rechter list
        while linksIter < lenLinks and rechtsIter < lenRechts:
            if links[linksIter] < rechts[rechtsIter]:
                list[mainlistIterator] = links[linksIter]
                linksIter += 1
            else:
                list[mainlistIterator] = rechts[rechtsIter]
                rechtsIter += 1
            mainlistIterator += 1

        #checkt of er variabnele over zijn
        while linksIter < lenLinks:
            list[mainlistIterator] = links[linksIter]
            linksIter += 1
            mainlistIterator += 1

        while rechtsIter < lenRechts:
            list[mainlistIterator] = rechts[rechtsIter]
            rechtsIter += 1
            mainlistIterator += 1
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

def frequentieLeeftijd(lst):

    freqDict = {
        '0': 0,
        '3': 0,
        '7': 0,
        '12': 0,
        '16': 0,
        '18': 0,
    }
    for i in lst:
        if i == 18:
            freqDict['18'] += 1
        elif i == 16:
            freqDict['16'] += 1
        elif i == 12:
            freqDict['12'] += 1
        elif i == 7:
            freqDict['7'] += 1
        elif i == 3:
            freqDict['3'] += 1
        elif i == 0:
            freqDict['0'] += 1
    return freqDict