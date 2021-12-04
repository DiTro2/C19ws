import requests
from bs4 import BeautifulSoup

elhunytak = []


def banya(lap):
    """Kibányássza az adott sorszámú oldalról 'elhunytak' 2D-s listába

    lap: 'https://koronavirus.gov.hu/elhunytak?page={lap}' //'0' az utolsó 50 halottat tartalmazó oldal
    """

    Q = f"https://koronavirus.gov.hu/elhunytak?page={lap}"
    r = requests.get(Q)
    # print(r.status_code, r.headers['content-type'],r.encoding)
    site = BeautifulSoup(r.text, 'html.parser')

    for adat, sor in enumerate(site.find_all('tr')):
        elhunyt = []

        for oszlop in sor.find_all('td'):
            elhunyt.append(oszlop.text.replace("  ", "").replace("\n", ""))

        elhunytak.append(elhunyt)


def lastPage():
    """Az utolsó oldal számának kibányászása"""

    o = "https://koronavirus.gov.hu/elhunytak"
    lap = BeautifulSoup(requests.get(o).text, 'html.parser')
    return str(lap.find('li', class_='pager-last').find('a').get('href')).rsplit("=")[1] #Érted?! :D


def kiir():
    """Kiírja az elhunytak listáját soronként
    Minden sor egy lista [sorszám, nem, életkor, alapbetegségek]"""

    for na in elhunytak:
        print(na)


def korSzerint(min: int, max: int):
    """Kiírja a minimum és maximum életkor közötti elhunytakat"""
    for le in elhunytak:
        if len(le) > 3 and int(le[2]) >= min and int(le[2]) <= max:
<<<<<<< HEAD
            print(le[0],le[1],le[2],le[3], sep=";")
=======
            print(le)
>>>>>>> 6270d8adf49f57fce082df79b43881b9ec0a0596


#korSzerint(90, 95)


def interface():
    print("""Üdvözlet!
    Ez a script a 'https://koronavirus.gov.hu/elhunytak' weblapról próbálja kibányászni az elhunytak listáját életkor szerint.
    Az utoljára regisztráltaktól kezdve lapnként 50 sorban vannak felsorolva az elhunytak.
    Minnél több oldalt vizsgál annál  több ideig tarthat az adatok lekérése""")


    utso = int(input("\nKérem adja meg, melyik oldaltól vizsgálná! (0 - a legutolsó 50 regisztrált elhunyt) :"))
    elso = int(input(f"Kérem adja meg, melyik oldalig kíváncsi az adatokra! (max: {lastPage()}):"))+1
    if elso <= utso:
        return print("A második adat nem lehet kisebb!")
    min=int(input("\nMinimális életkor: "))
    max=int(input("Maximális életkor: "))
    for l in range(utso, elso):
        banya(l)
    korSzerint(min,max)


interface()

