import json
import time
import os

# Viser til bibliotekets JSON-fil i samme mappe som dette skriptet
FILE_PATH = os.path.join(os.path.dirname(__file__), 'bibliotek.json')

# Leser inn listen med bøker fra JSON-filen
def load_books():
    # Leser filen og laster JSON-innholdet
    with open(FILE_PATH, 'r', encoding='utf-8') as file:
        books = json.load(file)
    # Sørger for at alle bøker har feltet 'borrowed' (standard False)
    for b in books:
        if 'borrowed' not in b:
            b['borrowed'] = False
    # Returnerer listen med bøker til kallende funksjon
    return books

# Lagrer listen med bøker tilbake til JSON-filen
def save_books(books):
    with open(FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(books, file, indent=4, ensure_ascii=False)

# Viser hovedmenyen og valgene brukeren har
def menu():
    # synliggjør valgene for brukeren
    print("1. Legg til bok")
    print("2. Vis alle bøker")
    print("3. Lån en bok")
    print("4. Lever en bok")
    print("5. Avslutt")
    # Leser inn brukerens input som string
    choice = input("Velg et alternativ (1-5): ")
    # Returnerer valget til hovedløkken
    return choice 

# Funksjon for å legge til en ny bok i biblioteket
def legg_til_bok():
    # Leser det som blir skrivd i Titel, Forfatter og utgivelse år feltet, den fjerner også mellomrom rundt
    title = input("Skriv inn boktittel: ").strip()
    author = input("Skriv inn forfatter: ").strip()
    year = input("Skriv inn utgivelsesår: ").strip()
    
    # Henter eksisterende bøker for å sjekke duplikater
    books = load_books()
    # Sjekker om bok med samme tittel allerede finnes (Sensitivt på store/små bokstaver)
    for book in books:
        if book.get('title').lower() == title.lower():
            print(f"Boken '{title}' finnes allerede i biblioteket.")
            time.sleep(2)
            return

    # Oppretter en ny bok med standard 'borrowed' False
    books.append({
        "title": title,
        "author": author,
        "year": year,
        "borrowed": False
    })
    # Lagrer oppdatert liste tilbake til json filen
    save_books(books)
    
    print(f"Boken '{title}' er lagt til i biblioteket.")
    # Pause slik at brukeren rekker å se meldingen
    time.sleep(2)

# Viser alle bøker med status (tilgjengelig eller utlånt)
def vis_alle_boker():
    # Henter boklisten
    books = load_books()

    # Hvis ingen bøker finnes, sier ifra til brukeren
    if not books:
        print("Ingen bøker i biblioteket.")
    else:
        for book in books:
            title = book.get('title')
        # leter gjennom alle bøker og viser informasjon
            author = book.get('author')
            year = book.get('year')
            # Bestemmer status basert på feltet 'borrowed'
            status = "Utlånt" if book.get('borrowed', False) else "Tilgjengelig"
            print(f"Tittel: {title}, Forfatter: {author}, År: {year}, Status: {status}")
    # Venter på at brukeren trykker Enter før retur
    input("Trykk Enter for å fortsette...")

# Låner en bok: setter borrowed statusen til true hvis den er ledig
def lan_en_bok():
    # Leser input tittelen fra brukeren og leter om den finnes, (dette er ikke sensitivt på store/små bokstaver)
    title = input("Skriv inn boktittel du vil låne: ").strip().lower()
    
    books = load_books()
    # Søk gjennom boklisten etter matchende tittel
    for book in books:
        if book.get('title').lower() == title:
            # Hvis boka allerede er utlånt, informer brukeren at den er utilgjengelig
            if book.get('borrowed', False):
                print(f"Boken '{book['title']}' er allerede utlånt ;)")
            else:
                # Merk boka som utlånt og lagre endringene
                book['borrowed'] = True
                save_books(books)
                print(f"Du har lånt '{book['title']}!'.")
            # Pause før retur til meny, da kan brukeren lese meldingen
            time.sleep(2)
            return
    # Hvis ingen match funnet, sier ifra til brukeren
    print(f"Boken '{title}' finnes ikke i biblioteket ;)")
    time.sleep(2)

# Leverer en bok: setter 'borrowed' til False hvis den var utlånt
def lever_en_bok():
    # Leser inn tittel fra brukeren for innlevering
    title = input("Skriv inn boktittel du vil levere: ").strip().lower()
    
    books = load_books()
    # Finn boka i listen
    for book in books:
        if book.get('title').lower() == title:
            # Hvis boka var utlånt, merk den som levert og lagre
            if book.get('borrowed', False):
                book['borrowed'] = False
                save_books(books)
                print(f"Takk for at du leverte '{book['title']}'.")
            else:
                # Hvis boka ikke var utlånt, informer brukeren
                print(f"Boken '{book['title']}' var ikke utlånt, kanskje låne den først?")
            time.sleep(2)
            return
    
    # Hvis boka ikke finnes, gi beskjed
    print(f"Boken '{title}' finnes ikke i biblioteket vårt ;)")
    time.sleep(2)

# Sikrer at katalog og JSON-fil finnes før programmet starter
def ensure_bibliotek_file():
    # Opprett katalog og fil dersom de mangler
    if not os.path.exists(FILE_PATH):
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        with open(FILE_PATH, 'w', encoding='utf-8') as file:
            # Starter med en tom liste i JSON-filen
            json.dump([], file, ensure_ascii=False)

# Hovedfunksjon som styrer programmets flyt
def main():
    # Sørger for at nødvendig filstruktur er på plass
    ensure_bibliotek_file()
    # Hovedløkken som viser meny og håndterer valg
    while True:
        choice = menu()
        if choice == '1':
            legg_til_bok()
        elif choice == '2':
            vis_alle_boker()
        elif choice == '3':
            lan_en_bok()
        elif choice == '4':
            lever_en_bok()
        elif choice == '5':
            # Brukeren vil avslutte programmet
            print("Avslutter programmet...")
            break
        else:
            # Ugyldig valg, be brukeren prøve igjen
            print("Ugyldig valg, prøv igjen.")
            time.sleep(2)

# Starter programmet hvis filen kjøres direkte
if __name__ == "__main__":
    main()