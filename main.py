import requests
from bs4 import BeautifulSoup

elhunytak = []


def banya(lap: int, utolsoHalott: int):
    """Kibányássza az adott sorszámú oldalról 'elhunytak' 2D-s listába

    lap: 'https://koronavirus.gov.hu/elhunytak?page={lap}' //'0' az utolsó 50 halottat tartalmazó oldal
    """

    Q = f"https://koronavirus.gov.hu/elhunytak?page={lap}"
    r = requests.get(Q)
    elhunytakB = []
    site = BeautifulSoup(r.text, 'html.parser')

    for sor in site.find_all('tr'):
        elhunyt = []

        for oszlop in sor.find_all('td'):
            elhunyt.append(oszlop.text.replace("  ", "").replace("\n", "").replace("\r", ""))

        if elhunyt != []:
            elhunytakB.append(elhunyt)

    elhunytakB.reverse()
    for eh in elhunytakB:
        if int(eh[0]) > utolsoHalott:
            elhunytak.append(eh)


def lastPage():
    """Az utolsó oldal számának kibányászása"""

    o = "https://koronavirus.gov.hu/elhunytak"
    lap = BeautifulSoup(requests.get(o).text, 'html.parser')
    return str(lap.find('li', class_='pager-last').find('a').get('href')).rsplit("=")[1]  # Érted?! :D


def lastRecord():
    """A legutóbbi elhunyt sorszámának kibányászása
        és újabb elhunytak számának meghatározása.
        !!!beolvas()-t meghívja!!!
        return: új elhunytak száma"""
    o = "https://koronavirus.gov.hu/elhunytak"
    utsoH = BeautifulSoup(requests.get(o).text, 'html.parser')
    uh = int(utsoH.find('tr', class_='views-row-first').find('td').text)
    print("Az utolsó elhunyt sorszáma a 'koronavirus.gov.hu'-n:", uh)
    beolvas()
    print("Az utolsó tárolt elhunyt sorszáma", elhunytak[-1][0])
    print("Ez", int(uh) - int(elhunytak[-1][0]), "újabb elhunytat jelent")
    return int(uh) - int(elhunytak[-1][0])


def kiirMonitorra():
    """Kiírja az elhunytak listáját soronként
    Minden sor egy lista [sorszám, nem, életkor, alapbetegségek]"""

    for na in elhunytak:
        print(na)


def korSzerint(min: int, max: int):
    """Kiírja a minimum és maximum életkor közötti elhunytakat"""

    for le in elhunytak:
        if len(le) > 3 and int(le[2]) >= min and int(le[2]) <= max:
            print(le[0], le[1], le[2], le[3], sep=";")


def beolvas():
    """Beolvassa a tárolt 'elhunytak.csv' listát"""
    try:
        with open("elhunytak.csv", "r") as lista:
            for sor in lista:
                elhunytak.append(sor.strip().split(";"))

    except FileNotFoundError as fnfe:
        print("\033[6m\033[91mHIBA:\033[0m", "Az elhunytak.cvs fájl nem létzeik!")


def kiirCsvbe():
    """kiírja az 'elhunytak' listát, az 'elhunytak.csv'-be"""

    with open("elhunytak.csv", "w") as lista:
        for sor in elhunytak:
            lista.write(f"{sor[0]};{sor[1]};{sor[2]};{sor[3]}\n")


def interface():
    print("""Üdvözlet!
    Ez a script a 'https://koronavirus.gov.hu/elhunytak' weblapról próbálja kibányászni az elhunytak listáját életkor szerint.
    Az utoljára regisztráltaktól kezdve lapnként 50 sorban vannak felsorolva az elhunytak.
    Minnél több oldalt vizsgál annál  több ideig tarthat az adatok lekérése""")

    utso = int(input(
        f"\nKérem adja meg, melyik oldaltól vizsgálná! (0 - a legutolsó 50 regisztrált elhunyt) (max: {lastPage()}):"))
    elso = int(input(f"Kérem adja meg, melyik oldalig kíváncsi az adatokra! (max: {lastPage()}):")) + 1
    if elso <= utso:
        return print("A második adat nem lehet kisebb!")
    min = int(input("\nMinimális életkor: "))
    max = int(input("Maximális életkor: "))
    if max < min: print("???")
    for l in range(utso, elso):
        banya(l)
    korSzerint(min, max)


def csvAppend():
    ujhalott = lastRecord()  # lastRecord() meghívja a beolvas()-t, tehát az 'elhunytak' listához hozzáadódik ami a csv-ben van
    if ujhalott > 3000: print("Ez elég sok! (Lehet nem kéne egyszerre frissíteni)")
    print("Ez", ujhalott / 50, "oldalnyi új elhunyt")
    enyitFrissit = int(input("Hány oldal új elhunytat szeretne hozzáfűzni a helyi listához?"))
    utolsoOldal = int(lastPage()) - len(elhunytak) // 50 - 1
    for old in range(utolsoOldal, utolsoOldal - enyitFrissit,
                     -1):
        print(old, "-as számú oldal bányászása... cél:", utolsoOldal - enyitFrissit + 1)
        banya(old, int(elhunytak[-1][0]))


# interface()
# beolvas()
# korSzerint(35,65)
# banya(1)
csvAppend()

# lastRecord()
# kiirCsvbe()
# beolvas()
# banya(728)
kiirCsvbe()
