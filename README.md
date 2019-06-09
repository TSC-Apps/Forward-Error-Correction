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

###### Zalety FEC:

- świetnie się sprawdza w korekcji błędów "na żywo", np. wideo, audio,
- charakteryzuje się jednakowym opóźnieniem dla całego zestawu danych,
- nie ma protokołu transmisyjnego.

###### Wady FEC:

- skomplikowane i czasochłonne metody korekcji błędów,

- brak gwarancji skorygowania wszystkich błędów,

- przy dużej liczbie błędów dekoder zamiast ją zmniejszać, może spowodować jej powiększenie.

  

#### Model

![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/270a9ac5fbb9681e9648337f29b94021fad8f48f/model.png?raw=true)

Kanał transmisyjny jest zaburzany przez losowe zakłócenia.



#### BER (Bit Error Rate)

Elementowa stopa błędów, wskaźnik określający prawdopodobieństwo wystąpienia zafałszowania bitu informacji w czasie transmisji danych. Z matematycznego punktu widzenia jest to stosunek liczby bitów odebranych błędnie do całkowitej liczby przesłanych bitów. W dzisiejszych systemach BER jest zależny od szybkości transmisji i od rezerwy mocy sygnału. Dobre jakościowo połączenie charakteryzuje się BER poniżej 10<sup>-10</sup>. W typowych kanałach zawiera się w przedziale <10<sup>-2</sup>, 10<sup>-5</sup>>. Dla transmisji danych wymagane jest BER ~ (10<sup>-6</sup>, 10<sup>-9</sup>).

Zaimplementowane uniwersalne narzędzie do liczenia BER wykonuje logiczny XOR bitów na kolejnych pozycjach w oryginalnej wiadomości 
i w wiadomości zdekodowanej po przejściu przez kanał, sprawdzając w ten sposób ich zgodność.

```python
def ber_triple(input, output):
    wrong_bits = 0

    for i in range(len(input)):
        wrong_bits += (input[i] ^ output[i])

    return wrong_bits / len(input)
```



#### Kod z powtórzeniem

Jeden z najprostszych kodów korekcyjnych, polegający na powtórzeniu danego bitu kilkukrotnie - w projekcie testujemy kod potrajający bity. 
Elementowa stopa błędu jest relatywnie niska, nie jest to niezawodna metoda, jednak sporo zyskuje dzięki swojej łatwości implementacji. 

Przykład: 

> Transmisja kodu o długości 3: 101. Po powieleniu kazdego z bitów trzykrotnie uzyskujemy 111 000 111 i taki sygnał wysyłamy. Załóżmy, że wystąpiły błędy i odbiorca otrzymał 111 010 100. Sygnał dekodujemy zgodnie z zasadą większości, więc ostatecznym rezultatem jest 100. W tym przypadku jeden bit jest zafałszowany, jednak wiekszość odebranych bitów jest poprawna.



W projekcie koder to `python comprehension` (nie ma odpowiednika w języku polskim), które potraja kazdy bit w danej liście bitów. Na potrzeby kanału zwracana jest `numpy array`.

```python
def code_triple(lst):
    return array([[i for i in lst for j in range(0, 3)]])
```



Dekoder jest bardziej skomplikowany. Zewnętrzna pętla posiada krok równy 3. Za każdym obiegiem pętli tworzy nowy `Counter`, który zlicza wystąpienia 0 i 1. Kiedy już wewnętrzna pętla obróci się 3 razy, wybierana jest popularniejsza wartość wśród badanych trzech bitów. Owa wartość dodawana jest do wynikowej, zdekodowanej listy, zachowujemy w ten sposób oryginalny rozmiar wiadomości.



```python
def decode_triple(arr):
    dec_lst = []
    lst = arr[0]
    for i in range(0, len(lst), 3):
        counter = Counter()
        for j in range(0, 3):
            counter[lst[i + j]] += 1

        # zabieg konieczny ze wzgledu na zwracanie przez most_commot listy krotek
        val, times = zip(*counter.most_common())
        dec_lst.append(val[0])
        counter.clear()

    return dec_lst
```



#### Kod BCH (Bose-Chaudhuri-Hocquenghema)

###### Krótka teoria

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



###### Wykorzystana biblioteka:

> <https://github.com/jkent/python-bchlib>



###### Badania, parametry

Przy badaniu skuteczności BCH sterowaliśmy parametrami kanału, długością informacji, którą chcemy zakodować, oraz zdolnością korekcji błędów - ilością bitów, które maksymalnie kodowanie BCH jest w stanie naprawić. Ze względu na ograniczenia wykorzystanej implementacji danego kodowania korekcyjnego, przy dużej informacji do przetworzenia biblioteka odmawiała współpracy, ciąg wejściowy został podzielony na pakiety. Każdy z nich z osobna został przepuszczony przez wybrany kanał, zakodowany i następnie odkodowany. Ostatecznie wszystkie złączono w jeden ciąg wyjściowy, na którego podstawie obliczono współczynnik błędu (BER) dla danych parametrów kodowania i kanału. 

Ilość pozycji kontrolnych (nadmiarowość) w zakodowanej informacji została zbadana eksperymentalnie poprzez dobieranie parametru `t` - zdolności korekcyjnej błędów. Od tego samego parametru zależała również ilość bitów w pojedynczym pakiecie - im większe `t`, tym mniejsze pakiety. Co istotne, wraz ze wzrostem skuteczności kodowania, czyli zwiększeniem zdolności korekcyjnej `t`, rosła długość zakodowanej informacji - ilość pozycji kontrolnych. Innymi słowy, przy zwiększaniu parametru t wystąpił zauważalny wzrost efektywności kodowania kosztem nadmiarowości.

Tabela powstała w trakcie przeprowadzania eksperymentów na wykorzystanej implementacji bibliotekii kodowania BCH:

```
+--------------+-----------------+-------------------------+-----------------------------+
| BCH_BITS - t | MAX_DATA_LENGTH | ENCODED_BITS            | n - k                       |
| zdolność     | w pojedynczym   | ilosc bitow             | liczba pozycji kontrolnych  |
| korekcyjna   | pakiecie        | zakodowanej informacji  |                             |
+--------------+-----------------+-------------------------+-----------------------------+
| 10           | 1007            | 1120                    | 113                         |
| 50           | 942             | 1510                    | 568                         |
| 100          | 864             | 1980                    | 1116                        |
| 200          | 718             | 2870                    | 2006                        |
| 500          | 362             | 5150                    | 4788                        |
| 630          | 297             | 5680                    | 5383                        |
+--------------+-----------------+-------------------------+-----------------------------+
```

* `BCH_BITS` - `t`, zdolność korekcji błędów, maksymalna liczba bitów, które można naprawić,
* `MAX_DATA_LENGTH` - maksymalna ilość bitów w pojedynczym pakiecie,
* `ENCODED_BITS` - ilość bitów całej zakodowanej informacji (informacja początkowa + pozycje kontrolne),
* `n - k` - liczba pozycji kontrolnych, `n-k` = `ENCODED_BITS` - `MAX_DATA_LENGTH`.



###### Aspekty techniczne

Wszelkie operacje, które wybrana biblioteka pozwala wykonać na ciągu danych zostały zebrane w klasie BCH celem zachowania porządku oraz spójności struktur. Są to kolejno: 

* zakodowanie informacji (encode), 
* odkodowanie informacji (decode).

Metody konwertują ciągi na struktury, które przyjmuje biblioteka i wtedy dopiero wykonywane są konkretne operacje.

Obiekty klasy są tworzone przy pomocy konstruktora, który jako argumenty przyjmuje wielomian, na podstawie którego automatycznie wyznaczanie jest ciało Galois, oraz parametr t symbolizujący zdolność korekcyjną. Podanie parametru p - polynomial z punktu widzenia implementacji biblioteki jest nieobligatoryjne. Próby jego zmiany kończyły się fiaskiem, więc zawsze ostatecznie zawsze jest taki sam i wynosi 8219 (propozycja autora biblioteki).

```python
class BCH:
    def __init__(self, p, t):
        self.bch_polynomial = p
        self.bch_bits = t
        self.bitflips = 0

        # utworzenie obiektu klasy z biblioteki bchlib
        self.obj = bchlib.BCH(self.bch_polynomial, self.bch_bits)
        # self.boj = bchlib.BCH.__init__()

    def encode(self, data):
        # konwersja listy do bytearray (na potrzeby biblioteki bchlib)
        data = bytearray(data)

        # zakodowanie ciagu danych
        data_enc = self.obj.encode(data)

        # utworzenie pakietu
        packet = data + data_enc

        lst = dec_to_bin(list(packet))

        return lst

    def decode(self, packet):
        # konwersja binary -> dec
        packet = bin_to_dec(packet)

        # konwersja listy do bytearray (na potrzeby biblioteki bchlib)
        packet = bytearray(packet)

        # rozpakowanie pakietu
        data, data_enc = packet[:-self.obj.ecc_bytes], packet[-self.obj.ecc_bytes:]

        # odkodowanie
        try:
            decoded = self.obj.decode(data, data_enc)

            self.bitflips = decoded[0]
            data_dec = decoded[1]
            # data_enc = decoded[2]

            return list(data_dec)
        except:
            print('Nie udalo sie odkodowac ciagu danych.')
```



#### Kod Hamminga

Koryguje błędy polegające na przekłamaniu jednego bitu poprzez użycie dodatkowych bitów parzystości. Odległość Hamminga (liczba pozycji, na których dane ciągi bitów się różnią) między słowami  transmitowanymi i odbieranymi powinna wynosić 0 lub 1. Bity kontrolne znajdują się na pozycjach będących potęgami liczby 2: 1, 2, 4, 8, 16...

W projekcie użyto gotowej implementacji kodu Hamminga (8,4): https://github.com/DakotaNelson/hamming-stego. Jako argument wejściowy przyjmuje listę bitów, zaś zwraca `numpy array` z zakodowanym ciągiem. W przypadku podania ciągu o długości, która nie jest wielokrotnością liczby 4, dopełenia go zerami, np:

```python
>>> encode([1,1,1])
array([[1, 1, 1, 0, 0, 0, 0, 1]])
```



Jego nadmiarowość wynosi 100%.



### Modele kanałów

W projekcie zaimplementowaliśmy dwa modele kanałów, za pośrecnictwem których przesyłany jest ciąg bitów powstały w wyniku zakodowania wiadomości. Podczas transmisji na sygnał wpływają zakłócenia, co prowadzi do tego, że niektóre bity mogą zostać błędnie odebrane po transmisji, a co za tym idzie, wiadomość zostanie niepoprawnie zdekodowana. Dobierając eksperymentalnie właściwe dla danego modelu prawdopodobieństwa przekłamań, zasymulowaliśmy kanały różnej jakości i sprawdziliśmy, w jakim stopniu uszkadzają one sygnał.



##### Binary Symmetric Channel (BSC) 

W tym kanale podejmujemy decyzję, czy dany bit zostanie przekłamany, czy nie, na podstawie prostego losowania z rozkładu jedostajnego na przedziale *[0,1)* z zadanym progowym prawdopodobieństwem błędu *p*, które dzieli przedział na dwie części. Jeśli wylosowana liczba znajdzie się poniżej progu, bit zostanie przekłamany, jeśli powyżej - przesłany poprawnie.

Losowanie wartości `float` z przedziału *[0.0, 1.0)* zgodnie z rozkładem jednostajnym umożliwia funkcja
`random()` z biblioteki `random`. Poniżej przedstawiony jest proces decyzyjny, czy dana wartość bitu z otrzymanej wejściowej (zakodowanej) `numpy array` zostanie w naszej symulacji kanału przesłana poprawnie, czy przekłamana (dołączamy ją do wyjściowej `numpy array`).


```python
if random() < p_of_error:
    if input_array[i][j] == 0:
        output_array[i][j] = 1
    else:
        output_array[i][j] = 0
else:
    output_array[i][j] = input_array[i][j]
```

Przy użyciu tego kanału wykonaliśmy testy jedynie w początkowej fazie projektu i nie zawarliśmy ich analizy w sprawozdaniu ze względu na fakt, że przedstawiony poniżej model Gilberta-Elliotta jest przy pewnych wartościach parametrów niemal równoważny z BSC.



##### Model Gilberta-Elliotta

Bardziej złożoną symulacją jest model GIlberta-Elliotta. Jest oparty o łańcuch Markowa z dwoma stanami *G* (*good*) i B (*bad*). W dobrym stanie *G* prawdopodobieństwo błędu jest mniejsze i wynosi *1-k*, w złym stanie jest większe i wynosi *1-h* (*k* i *h* to odpowiednie prawdopodobieństwa poprawnej transmisji bitu), w danym stanie decyzja o błędzie jest podejmowana jak w *BSC*. Poza tym ustalamy prawdopodobieństwo 
przejścia ze stanu dobrego do złego (*p*) i ze stanu złego do dobrego (*r*). Ten model pozwala dość dobrze symulować błędy grupowe.

 ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/270a9ac5fbb9681e9648337f29b94021fad8f48f/gilbert.png?raw=true)

Procedura pamięta, w którym aktualnie stanie znajduje się kanał, i na postawie prawdopodobieństwa błędu dla obecnego stanu przeprowadza proces decyzyjny dokładnie taki sam jak w kanale BSC - bit zostanie wysłany poprawnie lub niepoprawnie.
Następnie funkcja `random()` ponownie losuje wartość, która jest porównana z prawdopodobieństem przejścia do stanu przeciwnego - na tej podstawie aktualny stan zostanie zachowany lub zmieniony, po czym przejdziemy do kolejnego obiegu pętli i przesłania następnego bitu na takiej samej zasadzie.

```python
if good_state: # jestesmy w dobrym stanie
    if random() < p_of_error_when_good:
        if input_array[i][j] == 0:
            output_array[i][j] = 1
        else:
            output_array[i][j] = 0
    else:
        output_array[i][j] = input_array[i][j]
    good_state = random() > p_of_good_to_bad
else: # jestesmy w zlym stanie
    if random() < p_of_error_when_bad:
        if input_array[i][j] == 0:
            output_array[i][j] = 1
        else:
            output_array[i][j] = 0
    else:
        output_array[i][j] = input_array[i][j]
    good_state = random() > (1 - p_of_bad_to_good)
```





### Narzędzia do analizy danych

W projekcie skorzystano z biblioteki `matplotlib`.  Działa w sposób bardzo podobny do matlaba: należy ustalić zawartość osi x i y, ich etykietę, tytuł wykresu, etc np:

```python
	plt.plot([sum6/10], [2870 / 718], label='Kodowanie BCH(2870, 718)', marker='o')

    plt.title('Zestawienie nadmiarowości z BER różnych kodowań')
    plt.xlabel('BER')
    plt.ylabel('Nadmiarowość')
    plt.grid(linestyle='-', linewidth=0.5)	# tworzy siatke
    plt.legend() # tworzy legende na wykresie
    plt.savefig('gilbert_ber_err_prob=' + str(parameter_list) + '.png')

```



## Wyniki badań

Badania przeprowadziliśmy na kanale Gilberta. Kolejno przepuszczaliśmy przez kanał ciągi kodowane kodem potrojeniowym, Hamminga oraz BCH.
Zmienialiśmy cztery różne parametry kanału:

* *1-k* - prawdopodobieństwo wystąpienia błędu, jeśli kanał znajduje się w stanie dobrym,
* *p* - prawdopodobieństwo przejścia ze stanu dobrego do złego,
* *1-h* - prawdopodobieństwo wystąpienia błędu, jeśli kanał znajduje się w stanie złym, >
* *r* - prawdopodobieństwo przejścia ze stanu złego do dobrego.

Wybraliśmy sześć różnych ustawień kanału pod względem jakościowym. Dla każdego z tych ustawień wykonaliśmy dwa wykresy ilustrujące zależności, które chcieliśmy zbadać.

Pierwszy wykres z pary to zależność BER w danym kanale od długości przesyłanej wiadomości. Testowaliśmy tutaj kodowanie potrojeniowe, kodowanie Hamminga(8,4) oraz kodowanie BCH(,). Badanych długości wiadomości było dziesięć (co 100 000 bitów, od 100 000 bitów  do 1 000 000 bitów). Dla każdej długości zostało wygenerowane dziesięć losowych wiadomości, które zostały następnie zakodowane, przesłane i odkodowane. Wartość BER przyporządkowana na wykresie danej długości wiadomości
to średnia arytmetyczna dziesięciu wartości BER dla owych losowych ciągów wejściowych.

Drugi wykres z pary to ilustracja zależności pomiędzy BER a nadmiarowością danego kodowania. Przez nadmiarowość rozumiemy liczbę rzeczywistą, która mówi, ile razy dłuższa od informacyjnej wiadomości jest wiadomość zakodowana (gotowa już do przesłania
przez kanał), jak duży jest narzut dodatkowych bitów. Testowaliśmy tutaj kodowanie potrojeniowe, kodowanie Hamminga(8,4) oraz kodowanie BCH w czterech wersjach: (1120,1007), (1510,1024), (1980,864), (2870,718). W każdej parze *(n,k)* *n* oznacza długość całkowitą słowa po zakodowaniu, a *k* to liczba bitów informacyjnych - nadmiarowość liczymy jako iloraz *n/k*, jest to oczywiście stała wartość dla danego kodowania. Badaliśmy wiadomości o długości 1 000 000 bitów, znów generując po dziesięć
losowych ciągów i uśredniając BER widoczny na wykresach.










1. prawie idealny: `1-k = 0.000001`,  `p = 0.000101648`,  `1-h = 0.31`, `r = 0.914789`

   ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/gilbert_ber_err_prob%3D(1e-06%2C%200.000101648%2C%200.31%2C%200.914789).png?raw=true)

   ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/dots/gilbert_ber_err_prob=(1e-06,%200.000101648,%200.31,%200.914789).png?raw=true)

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

2. dobry: `1-k = 0.000053513`, `p = 0.000196854`, `1-h =0.65`, `r = 0.509547`

   ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/gilbert_ber_err_prob%3D(5.3513e-05%2C%200.000196854%2C%200.65%2C%200.509547).png?raw=true)

   ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/dots/gilbert_ber_err_prob=(5.3513e-05,%200.000196854,%200.65,%200.509547).png?raw=true)

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

3. niezły: `1-k = 0.0003631513`, `p = 0.000396854`, `1-h = 0.9`, `r = 0.2768`

   ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/gilbert_ber_err_prob%3D(0.0003631513%2C%200.000396854%2C%200.9%2C%200.2768).png?raw=true)

   ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/dots/gilbert_ber_err_prob=(0.0003631513,%200.000396854,%200.9,%200.2768).png?raw=true)

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

4. średni: `1-k = 0.000053513`,  `p = 0.00496854`, `1-h = 0.9`, `r = 0.2768`

   ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/gilbert_ber_err_prob%3D(5.3513e-05%2C%200.00496854%2C%200.9%2C%200.2768).png?raw=true)

   ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/dots/gilbert_ber_err_prob=(5.3513e-05,%200.00496854,%200.9,%200.2768).png?raw=true)

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

5. zły: `1-k = 0.0003631513`, `p = 0.00496854`, `1-h = 0.99999`, `r = 0.04`

   ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/gilbert_ber_err_prob%3D(0.0003631513%2C%200.00496854%2C%200.99999%2C%200.04).png?raw=true)

   ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/dots/gilbert_ber_err_prob=(0.0003631513,%200.00496854,%200.99999,%200.04).png?raw=true)

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

6. fatalny: `1-k = 0.0003631513`, `p = 0.00496854`, `1-h = 0.99999`, `r = 0.004`

   ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/gilbert_ber_err_prob%3D(0.0003631513%2C%200.00496854%2C%200.99999%2C%200.004).png?raw=true)

   ![](https://github.com/TSC-Apps/Forward-Error-Correction/blob/master/plots/dots/gilbert_ber_err_prob=(0.0003631513,%200.00496854,%200.99999,%200.004).png?raw=true)



### Wnioski

##### Zależność BER od długości wiadomości

W każdym wykresie oś pionowa charakteryzuje BER - Bit Error Rate (im mniejszy, tym lepszy), pozioma natomiast oznacza długość wiadomości - liczbę bitów w wygenerowanym ciągu. W **kanale prawie idealnym** kod potrojeniowy oraz BCH dają podobne rezultaty, z przewagą kodowania BCH, które spisało się idealnie, współczynnik błędu wynosi 0. Kodowanie Hamminga wyraźnie od nich odstaje. W przypadku **kanału dobrego** kodowanie BCH zachowuje wynik, potrojeniowe staje się dużo gorsze, jednak nadal dwukrotnie lepsze od Hamminga. W **kanale niezłym** oraz **średnim** BER kodowania potrojeniowego coraz bardziej zbliża się do współczynnika błędu kodu Hamminga, przy czym próbka zakodowana kanałem BCH stale jest bezbłędnie odkodowywana. Dopiero w **kanale złym** kodowanie potrojeniowe i Hamminga dają podobne rezultaty, a w kodowaniu BCH pojawia się BER nieznacznie mniejszy od konkurencyjnych kanałów. W **kanale fatalnym** kod Hamminga i potrojeniowy spisują się jednakowo, BCH nadal ma nad nimi przewagę.

Najlepsze wyniki pod względem występującego współczynnika błędu, niezależnie od dobranych parametrów, zwraca kodowanie BCH. Wiadomość zostaje bezbłędnie odkodowana dla prawie idealnego kanału, dobrego, niezłego oraz średniego. Bit Error Rate jest różny od 0 dopiero w gorszych kanałach, jednak nadal jest mniejszy od współczynnika błędu występującego przy kodowaniu potrojeniowym czy też Hamminga.

Warto też zauważyć, że rosnąca długość wiadomości nie wiązała się ze znaczącym wzrostem BER - niewielkich fluktuacji nie bierzemy pod uwagę. Pozwala to wnioskować, że dla danych parametrów kanału i danego kodowania BER jest funkcją w przybliżeniu stałą.

##### Zestawienie nadmiarowości 
W kanale prawie idealnym:

- wszystkie kodowania BCH dają BER = 0. Jeżeli przyjmiemy próg BER rzędu 10^{-6}​, wymagania spełnia także kod potrojeniowy,
- kodowanie Hamminga jest gorsze o rząd wielkości

BER nie jest tutaj czynnikiem różnicującym wśród kodowań BCH. Najoptymalniejszym wyborem okazuje się najmniej nadmiarowe kodowanie BCH czyli (1120, 1007) z nadmiarowością około 1,1.

W kanale dobrym:

- wszystkie kodowania BCH są niezawodne z BER = 0,
- kodowanie potrojeniowe i Hamminga oferują BER tego samego rzędu 10^-4 przy trzykrotnej nadmiarowości potrojeniowego i dwukrotnej Hamminga. Matematyczne zasady rządzące kodowaniem Hamminga zaczynają przeważać nad prostotą działania kodowania potrojeniowego.

BER nie jest tutaj czynnikiem różnicującym, ponieważ wszystkie kodowania BCH są bezbłędne. Najoptymalniejszym wyborem okazuje się najmniej nadmiarowe kodowanie BCH czyli (1120, 1007). 

W kanale niezłym:

- w BCH pojawiają się pierwsze błędy (w wersji z najmniejszą nadmiarowością (1120, 1007) mamy BER rzędu 10^-4,
- kodowanie Hamminga zbliża się do kodowania potrojeniowego (są rzędu 10^-3), dzieli je już minimalna różnica)

Wybór najoptymalniejszego kodowania jest już mniej oczywisty. Jeśli jest potrzeba przeprowadzenia bezbłędnej transmisji to najlepiej będzie zastosować kodowanie BCH(1510, 1024) o nadmiarowości ok. 1,5. W przypadku braku możliwości zastosowania tak nadmiarowego kodu lub kiedy, kluczowym czynnikiem jest szybkość transmisji, dobrym rozwiązaniem jest zastosowanie kodu BCH(1120, 1007) z nadmiarowością ok. 1,1, który przekłamuje mniej więcej 6 bitów na 10 000.

W kanale średnim:

- kodowania BCH układają się w przybliżeniu w łukowaty kształt hiperboliczny,
- kodowanie Hamminga jest coraz bliższe kodowaniu potrojeniowemu,
- najmniej nadmiarowe kodowanie BCH(1120, 1007), które wybieraliśmy jako najoptymalniejsze w dwóch pierwszych kanałach, zaczęło mieć gorszy BER od kodowania potrojeniowego i Hamminga (rzędu 10^-2),

Przyjęcie maksymalnego BER = 10^-2 prowadzi do odrzucenia trzech kodowań i pozwala wybierać między pozostałymi trzema kodowaniami BCH. Jeśli najważniejszym czynnikiem jest szybkość transmisji, to dobrym wyborem okazuje się BCH(1510, 1024) z BER rzędu 10^-3 - 10^-4, zaś jeśli istnieje konieczność bezbłędnej transmisji, to należy wybrać BCH(1980, 864).

W kanale złym:

- żaden z badanych kodów nie jest w stanie skorygować wszystkich błędów, minimalny BER wynosi 0,1, wszystkie kodowania mają bardzo wysoki BER rzędu 10^-1,
- kodowanie Hamminga ma praktycznie identyczną zdolność korekcyjną co kodowanie potrojeniowe,
- rodzina kodów BCH znów układa się w hiperboliczny kształt - większa nadmiarowość oznacza mniejszy BER, mniejsza nadmiarowość - większy,.
- niewielkie różnice w BER oznaczają tutaj już spore różnice w bezwzględnej ilości przekłamanych bitów. Dla testowanego ciągu (1 000 000 bitów) 0,01 to 10 000 bitów.

W tak słabym kanale zdolność korekcyjna wszystkich kodowań jest tego samego rzędu. Zatem rozsądnym rozwiązaniem jest wybrać najmniej nadmiarowe kodowanie (BCH(1120, 1007) - jest on ok. 4 razy mniej nadmiarowy od najlepszego kodowania, zaś ma jedynie ok. 10% wyższy BER.

W kanale fatalnym:

- rząd wielkości BER jest bardzo wysoki i wynosi 10^-1 - wartości oscylują wokół 50% błędnych bitów,
- kodowania potrojeniowe i Hamminga w stosunku do BCH radzą sobie gorzej niż w dwóch poprzednich kanałach.

W fatalnym kanale kodowanie jest praktycznie bez znaczenia. W żadnym wypadku nie można uzyskać wiadomości nawet podobnej do oryginalnej. Zatem najlepiej wybrać najszybsze kodowanie - BCH(1120, 1007).
