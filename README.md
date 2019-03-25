# Niezawodność i Diagnostyka Układów Cyfrowych - Projekt



| Prowadzący  | dr hab. inż. Henryk Maciejewski                              |
| ----------- | ------------------------------------------------------------ |
| Temat       | System FEC (Forward Error Correction)                        |
| Skład grupy | Tymoteusz Frankiewicz, 241255<br />Filip Mykieta, 229900<br />Szymon Wiśniewski, 241269 |



## Problem

Znalezienie optymalnej liczby oraz sposobu dodawania nadmiarowych bitów w systemach FEC.



## Wstępne założenia

Celem projektu jest zbudowanie algorytmów korekcyjnych i oszacowanie parametrów modelu tak, aby stosunek kosztu do jakości był jak najbardziej optymalny.



## Wykorzystane narzędzia

- Język Python wraz z bibliotekami: 
  - numpy,
  - matplotlib,

- git (GitHub jako zdalne repozytorium).



## Teoria

#### Kody nadmiarowe

Służą do zabezpieczenia danych przed błędami transmisji poprzez dołączenie dodatkowych bitów do nadawanych informacji. Mają zastosowanie między innymi w technice FEC - Forward Error Correction.



W skład kodów nadmiarowych wchodzą:

* **kody blokowe** - informacje podzielone są na bloki k-elementowe. Do każdego z nich dołączana jest sekwencja kontrolna,
* **kody splotowe** - nie występuje podział na bloki. W przeciwieństwie do kodów blokowych przetwarzają dane w sposób ciągły, bezpośrednio w momencie otrzymania danej informacji. Ideą kodowania splotowego jest przekształcenie wejściowego k-bitowego ciągu informacyjnego na n-bitowy ciąg wyjściowy,
* **kody systematyczne** - ciąg informacyjny zawarty jest w pierwszych k-bitach słowa kodowego,
* **kody liniowe** - wektor kodowy jest sumą dwóch dowolnych wektorów kodowych,
* **kody cykliczne** - tworzone są przy wykorzystaniu ciągów wielomianów.



#### FEC

Technika służąca do korygowania błędów w tramisji danych kosztem zaopatrzenia danego ciągu w nadmiarową informację, którą uzyskuje się poprzez użycie kodów korekcyjnych.



###### Wady FEC:

- skomplikowane i czasochłonne metody korekcji błędów,
- brak gwarancji skorygowania wszystkich błędów,
- przy dużej liczbie błędów dekoder zamiast ją zmniejszać może spowodować jej powiększenie.



###### Zalety FEC:

- świetnie się sprawdza w korekcji błędów "na żywo", np. wideo, audio,
- charakteryzuje się jednakowym opóźnieniem dla całego zestawu danych,
- nie ma protokołu transmisyjnego.



#### Model

![](<https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/model.png>)

Kanał transmisyjny jest zaburzany przez losowe zakłócenia.



#### BER (Bit Error Rate)

Elementowa stopa błędów, wskaźnik określający prawdopodobieństwo wystąpienia zafałszowania bitu informacji w czasie transmisji danych. Z matematycznego punktu widzenia jest to stosunek liczby bitów odebranych błędnie do całkowitej liczby przesłanych bitów. W dzisiejszych systemach BER jest zależny od szybkości transmisji i od rezerwy mocy sygnału. Dobre jakościowo połączenie charakteryzuje się BER poniżej 10<sup>-10</sup>. W typowych kanałach zawiera się w przedziale <10<sup>-2</sup>, 10<sup>-5</sup>>. Dla transmisji danych wymagane jest BER ~ (10<sup>-6</sup>, 10<sup>-9</sup>).

Mamy przeprowadzić badania dla BER kanału 10<sup>-3</sup> oraz 10<sup>-8</sup>. (???)



#### Kod z powtórzeniem

Jeden z najprostszych kodów korekcyjnych polegający na powtórzeniu danego bitu kilkukrotnie. Elementowa stopa błędu jest relatywnie niska, nie jest to niezawodna metoda, jednak sporo zyskuje dzięki swojej łatwości implementacji. 

Przykład: 

> Transmisja kodu o długości 3 - 101. Po powieleniu kazdego z bitów trzykrotnie uzyskujemy 111 000 111 i taki sygnał wysyłamy. Załóżmy, że wystąpiły błędy i odbiorca otrzymał 111 010 100. Sygnał dekodujemy zgodnie z zasadą większości, więc ostatecznym rezultatem jest 100. W tym przypadku jeden bit jest zafałszowany, jednak wiekszość odebranych bitów jest poprawna.



#### Kod BCH (Bose-Chaudhuri-Hocquenghema)

Kody cykliczne, czyli wielomianowe o długości słowa kodowego n, których wielomian generujący g(x) jest dzielnikiem wielomianu x<sup>n</sup>+1.

Biblioteka

> <https://github.com/jkrauze/bch>



#### Kod Hamminga

Koryguje błędy polegające na przekłamaniu jednego bitu poprzez użycie dodatkowych bitów parzystości. Odległość Hamminga (liczba pozycji, na których dane ciągi bitów się różnią) między słowami transmitowanymi i odbieranymi powinna wynosić 0 lub 1. Bity kontrolne znajdują się na pozycjach będących potęgami liczby 2 - 1, 2, 4, 8, 16...



TODO zapoznać się z:

<https://www.geeksforgeeks.org/computer-network-hamming-code/>

<https://www.youtube.com/watch?v=373FUw-2U2k>



#### Kod Reed-Solomona

Biblioteka:

> <https://pypi.org/project/reedsolo/>>



#### Model Gilberta








## Notatki
#### 13 Marzec 2019

> - BCH - <https://github.com/jkrauze/bch> 
> - Reed-Solomon - <https://pypi.org/project/reedsolo/>
>   - biblioteki, kilka przykładów kodów nadmiarowych encode, decode
> - badania - eksperyment numeryczny zbudowanie modelu
> - potrajanie bitów - intuicyjny sposób - różne sposoby nadmiarowości
> - kanał - uszkadza bity, np. model Gilberta, model…
>   różne parametry kanału - mniej lub bardziej zaszumiony
>   kody są projektowane pod różne kanały
>   kanały różnią się parametrami - prawdopodobieństwem błędu oraz typem błędu
> - BER kanału: 10-3, 10-8 - stopień zaszumienia
> - wyjście: obserwowana jakość transmisji oraz obniżona prędkość transmisji, zyskujemy jedno, tracimy drugie
>
> 
>
> ##### Na kolejne zajęcia:
>
> - model - w sprawozdaniu
> - biblioteki kodowe - różne rodziny kodów, kodery i dekodery, różne nadmiarowości
> - próbki kodu

