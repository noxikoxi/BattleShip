# BattleShips 

### A game made in pygame, playable on LAN for two players

---

## How to start the game:
- Run Server.py (python Server.py).
- Run Client.py twice (for each player).
- If you want to play on one PC you may leave IP filed as blank, it will take your PC IP, otherwise type IP of the computer running Server.py

---

## Zasady gry
- Celem gry jest zatopienie wszystkich statków przeciwnika; wygrywa gracz, któremu uda się to zrobić pierwszemu.
- Statki nie mogą być ustawione w swoim sąsiedztwie (pomiędzy statkami musi występować co najmniej 1 blok przerwy,
  wliczając w to ruch na skos).
- Położenie statków ustalane jest losowo.
- Statki mogą być ustawione w pionie lub poziomie.
- Każdy gracz posiada:
    - 4 statki o długości 1.
    - 3 statki o długości 2.
    - 2 statki o długości 3.
    - 1 statek o długości 4.
- Gracze wykonują ruch wedle ustalonej kolejności:
  - Na początku zaczyna losowy gracz (jest wybierany przez serwer).
  - Następnie wybiera współrzędne na mapie przeciwnika, w które chce strzelić.
  - Po wykonaniu strzału, jeżeli trafił w statek, wykonuje swój ruch ponownie.
  - Jeżeli trafił w wodę, następny ruch wykonuje przeciwnik.
  - Gra kończy się, kiedy jeden z graczy zatopi wszystkie statki przeciwnika.

---

## Jak grać?
- Po uruchomieniu gry należy wpisać swoją nazwę oraz adres ip serwera.
- Jeżeli klient jest uruchomiony na tym samym komputerze co serwer, można zostawić pole z adresem ip puste, zostanie pobrany z systemu.
- Okno gry zawiera dwie plansze: gracza oraz przeciwnika
- Na planszy gracza widoczne są wszystkie jego statki.
- Na planszy przeciwnika na początku są same nieznane bloki, 
w trakcie gry po strzale będą one sygnalizowały zawartość planszy przeciwnika:
    - Pomarańczowe koło oznacza, że trafiliśmy w wodę.
    - Czerwony kolor bloku oznacza, że trafiliśmy w statek.
    - Czarny kolor bloku oznacza, że statek przeciwnika został na nim zatopiony.
- W celu wykonania swojego ruchy należy wybrać blok z planszy przeciwnika po prawej stronie.
- Blok wybieramy klikając lewym przyciskiem myszy, zaznaczony blok jest sygnalizowany poprzez pomarańczowy kolor.
Następnie, aby wykonać ruch, należy nacisnąć przycisk "Shoot" na dole okna.
- Pomarańczowe koło na naszej planszy oznacza, że przeciwnik strzelił w wodę.
- Zaczerwieniony blok zawierający statek na planszy gracza oznacza strzał przeciwnika w statek.
- Po zakończeniu gry serwer automatycznie się zamyka, gracz może zamknąć okienko poprzez klawisz *q*.


---

## Zawartość Katalogu
- plik Settings.py zawierający ustawienia dla Okna i mapy gry oraz zdefiniowane kolory.
- plik Server.py zawierający implementację Serwera i Klienta.
- plik Client.py zawierający implementację gry oraz połączenie się z serwerem (Gracz).
- katalog Classes zawierający implementacje klas potrzebnych do obsługi gry.
- katalog Assets zawierający grafiki statków.

---

## Implementacja

### Klasy

Implementacja zawiera klasy: Block, Button, Player, Popup, Ship, SpriteGroup, Server, Client, Game
- Block jest klasą implementująca jeden kwadrat na planszy, posiada metody umożliwiające w łatwy sposób oznaczenie strzałów.
- Button jest klasą, wykorzystaną do stworzenia przycisku "Shoot", umożliwia jednoznaczne wykonanie ruchu.
- Player jest klasą reprezentująca gracza, zawiera wszystkie statki oraz metodę losowo je umieszczająca.
- Popup to klasa, której zadaniem jest pobranie nazwy i adresu ip serwera od gracza.
- Ship to klasa reprezentująca statek.
- SpriteGroup dziedziczy po *pygame.sprite.Group*, posiada nadpisaną metodę Draw, która pobiera dodatkowo ekran do rysowania.
- Server jest implementacją serwera gry, służy do przesyłania informacji pomiędzy graczami.
- Client jest klasą, która obsługuje komunikację z serwerem.
- Game jest klasą gry.

### Istotne informacje
- Ship przechowuje licznik trafień, umożliwiający ocenienie, czy jest już zatopiony.
- Player przechowuje licznik zatopionych statków przeciwnika, pozwala to ocenić czy już wygrał.
- Server służy tylko jako pośrednik wymiany informacji pomiędzy graczami oraz rozdziela tury.
- Cała logika gry jest po stronie klienta.
- Indeksowanie planszy gracza i przeciwnika odbywa się w kolejności [wiersz] [kolumna].
- O końcu gry decyduje klient (gracz), jeżeli licznik zatopionych statków gracza jest równy całkowitej liczbie statków,
    wysyła on komunikat *GAME_OVER* do serwera, który przesyła go do drugiego gracza. Gracz, który otrzymał *GAME_OVER* z serwera, przegrywa.
- W konsoli serwera wyświetlane są komunikaty o otrzymanych wiadomościach od graczy oraz wysłanych komunikatów *TURN*.
- W konsoli klienta pokazywane są komunikaty jakie odebrał od serwera.

### Komunikacja Klient-Serwer
- Odbywa się poprzez określoną pulę wiadomości:
    - *SHOOT*
    - *SHIP*
    - *WATER*
    - *SHIP_SUNK*
    - *GAME_OVER*
    - *TURN*
    - *READY*
    - *ERROR*
- **SHOOT** oznacza strzał, jego składnia: *SHOOT [wiersz]:[kolumna]*
- **SHIP** oznacza trafienie w statek: *SHIP [wiersz]:[kolumna]*
- **WATER** oznacza trafieni w wodę: *WATER [wiersz]:[kolumna]*
- **SHIP_SUNK** oznacza, że trafiony jest statek i został zatopiony: 
*SHIP_SUNK [wiersz początku statku],[kolumna początku statku]:[kierunek statki]:[długość statku]*
- **GAME_OVER** oznacza koniec gry, gracz, który otrzymał ten komunikat od serwera, przegrywa. Składnia: *GAME_OVER*
- **TURN** oznacza przekazanie tury, gracz, który go otrzymał, może wykonać ruch, Składnia: *TURN*
- **READY** sygnalizuje, że gracz otrzymał i przetworzył nazwę przeciwnika oraz jest gotowy do rozpoczęcia gry
- **ERROR** sygnalizuje, że serwer napotkał błąd i zamyka połączenie, jednocześnie zamyka gry klientów

#### Uwagi
- wiersz w komunikatach jest realnym indeksem mapy, dlatego jest zawsze mniejszy o 1. (mapa jest indeksowana od 0, ale wyświetlane etykiety zaczynają się od 1).

