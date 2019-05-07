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

![](F:\Dev\Git\Forward-Error-Correction\model.png)

Kanał transmisyjny jest zaburzany przez losowe zakłócenia.



#### BER (Bit Error Rate)

Elementowa stopa błędów, wskaźnik określający prawdopodobieństwo wystąpienia zafałszowania bitu informacji w czasie transmisji danych. Z matematycznego punktu widzenia jest to stosunek liczby bitów odebranych błędnie do całkowitej liczby przesłanych bitów. W dzisiejszych systemach BER jest zależny od szybkości transmisji i od rezerwy mocy sygnału. Dobre jakościowo połączenie charakteryzuje się BER poniżej 10<sup>-10</sup>. W typowych kanałach zawiera się w przedziale <10<sup>-2</sup>, 10<sup>-5</sup>>. Dla transmisji danych wymagane jest BER ~ (10<sup>-6</sup>, 10<sup>-9</sup>).

<<<<<<< Updated upstream


=======
>>>>>>> Stashed changes
#### Kod z powtórzeniem

Jeden z najprostszych kodów korekcyjnych polegający na powtórzeniu danego bitu kilkukrotnie. Elementowa stopa błędu jest relatywnie niska, nie jest to niezawodna metoda, jednak sporo zyskuje dzięki swojej łatwości implementacji. 

Przykład: 

> Transmisja kodu o długości 3 - 101. Po powieleniu kazdego z bitów trzykrotnie uzyskujemy 111 000 111 i taki sygnał wysyłamy. Załóżmy, że wystąpiły błędy i odbiorca otrzymał 111 010 100. Sygnał dekodujemy zgodnie z zasadą większości, więc ostatecznym rezultatem jest 100. W tym przypadku jeden bit jest zafałszowany, jednak wiekszość odebranych bitów jest poprawna.



#### Kod BCH (Bose-Chaudhuri-Hocquenghema)

Kody cykliczne, czyli wielomianowe o długości słowa kodowego n, których wielomian generujący g(x) jest dzielnikiem wielomianu x<sup>n</sup>+1, o zmiennej długości, służące do korekcji błędów losowych, w przybliżeniu do 25% całkowitej liczby cyfr.

Istnieje wielomian k(x) stopnia k, że

> g(x)k(x) = x<sup>n</sup> + 1

lub

> (x<sup>n</sup>+1)modg(x) = 0

Dla każdej liczby całkowitej m i t < 2<sup>m-1</sup> istnieje kod bch o długości n = 2<sup>m</sup> - 1. Może on korygować do t błędów i ma nie więcej niż m*t elementów kontrolnych.



> n = 2<sup>m</sup> - 1
>
> k >= n - m*t
>
> d<sub>min</sub> >= 2t + 1



gdzie: 
n - długość wektora kodowego,
k - długość ciągu informacyjnego,
d - odległość minimalna,
t - zdolność korekcji błędów.



Wykorzystana biblioteka:

> <https://github.com/jkent/python-bchlib>









#### Kod Hamminga

Koryguje błędy polegające na przekłamaniu jednego bitu poprzez użycie dodatkowych bitów parzystości. Odległość Hamminga (liczba pozycji, na których dane ciągi bitów się różnią) między słowami transmitowanymi i odbieranymi powinna wynosić 0 lub 1. Bity kontrolne znajdują się na pozycjach będących potęgami liczby 2 - 1, 2, 4, 8, 16...

Wykorzystana biblioteka:

> <https://pypi.org/project/libhamming/>



## Wyniki badań

Badania przeprowadziliśmy na kanale Gilberta. Kolejno przepuszczaliśmy przez kanał ciągi kodowane kodem potrojeniowym, Hamminga oraz BCH. Zmienialiśmy cztery różne parametry kanału:

* A - prawdopodobieństwo wystąpienia błędu jeśli kanał znajduje się w stanie dobrym,
* B - prawdopodobieństwo przejścia ze stanu dobrego do złego,
* C - prawdopodobieństwo wystąpienia błędu jeśli kanał znajduje się w stanie złym, 
* D - prawdopodobieństwo przejścia ze stanu złego do dobrego.

Wybraliśmy sześć różnych ustawień kanału pod względem jakościowym:

1. prawie idealny: `A = 0.000001`,  `B = 0.000101648`,  `C = 0.31`, `D = 0.914789`

   ![](<https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/gilbert_ber_err_prob%3D(1e-06%2C%200.000101648%2C%200.31%2C%200.914789).png>)

   

2. dobry: `A = 0.000053513`, `B = 0.000196854`, `C =0.65`, `D = 0.509547`

   ![](<https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/gilbert_ber_err_prob%3D(5.3513e-05%2C%200.000196854%2C%200.65%2C%200.509547).png>)

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

3. niezły: `A = 0.0003631513`, `B = 0.000396854`, `C = 0.9`, `D = 0.2768`

   ![](<https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/gilbert_ber_err_prob%3D(0.0003631513%2C%200.000396854%2C%200.9%2C%200.2768).png>)

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

4. średni: `A = 0.000053513`,  `B = 0.00496854`, `C = 0.9`, `D = 0.2768`

   ![](<https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/gilbert_ber_err_prob%3D(5.3513e-05%2C%200.00496854%2C%200.9%2C%200.2768).png>)

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

5. zły: `A = 0.0003631513`, `B = 0.00496854`, `C = 0.99999`, `D = 0.04`

   ![](<https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/gilbert_ber_err_prob%3D(0.0003631513%2C%200.00496854%2C%200.99999%2C%200.04).png>)

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

6. fatalny: `A = 0.0003631513`, `B = 0.00496854`, `C = 0.99999`, `D = 0.004`

   ![](<https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/gilbert_ber_err_prob%3D(0.0003631513%2C%200.00496854%2C%200.99999%2C%200.004).png>)





W każdym wykresie oś pionowa charakteryzuje BER - Bit Error Rate (im mniejszy tym lepszy), pozioma natomiast długość wiadomości - ilość bitów w wygenerowanym ciągu. W **kanale prawie idealnym** kod potrojeniowy oraz BCH dają podobne rezultaty, z przewagą kodowania BCH, które spisało się idealnie, współczynnik błędu wynosi 0. Kodowanie Hamminga wyraźnie od nich odstaje. W przypadku **kanału dobrego** kodowanie BCH zachowuje wynik, potrojeniowe staje się dużo gorsze, jednak nadal dwukrotnie lepsze od Hamminga. W **kanale niezłym** oraz **średnim** BER kodowania potrojeniowego coraz bardziej zbliża się do współczynnika błędu kodu Hamminga, przy czym próbka zakodowana kanałem BCH stale jest bezbłędnie odkodowywana. Dopiero w **kanale złym** kodowanie potrojeniowe i Hamminga dają podobne rezultaty, a w kodowaniu BCH pojawia się BER, nieznacznie mniejszy od konkurencyjnych kanałów. W **kanale fatalnym** kod Hamminga i potrojeniowy spisują się jednakowo, BCH nadal ma nad nimi przewagę.

Najlepsze wyniki pod względem występującego współczynnika błędu, niezależnie od dobranych parametrów, zwraca kodowanie BCH. Wiadomość zostaje bezbłędnie odkodowana dla prawie idealnego kanału, dobrego, niezłego oraz średniego. Bit Error Rate jest różny od 0 dopiero w gorszych kanałach, jednak nadal jest mniejszy od współczynnika błędu występującego przy kodowaniu potrojeniowym czy też Hamminga. 