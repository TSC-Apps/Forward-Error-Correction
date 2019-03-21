| Prowadzący  | dr hab. inż. Henryk Maciejewski                              |
| ----------- | ------------------------------------------------------------ |
| Temat       | System FEC (Forward Error Correction)                        |
| Skład grupy | Tymoteusz Frankiewicz, 241255<br /> Filip Mykieta, 229900<br />Szymon Wiśniewski, 241269 |

 

### Problem

Znalezienie optymalnej liczby oraz sposobu dodawania nadmiarowych bitów w systemach FEC.

### Wstępne założenia

Celem projektu jest zbudowanie algorytmów korekcyjnych i oszacowanie parametrów modelu tak, aby stosunek kosztu do jakości był jak najbardziej optymalny.

### Wykorzystane narzędzia

- Język Python wraz z bibliotekami: 
  - numpy,
  - matplotlib,

- git (GitHub jako zdalne repozytorium).

### Etapy realizacji projektu

- Koncepcja i przygotowanie teoretyczne
- Implementacja wybranych algorytmów
- Testowanie poprawności stworzonego programu i optymalizacja
- Analiza rezultatów

# Notatki z 13 III 2019

- BCH - <https://github.com/jkrauze/bch> 
-  Reed-Solomon - <https://pypi.org/project/reedsolo/>
  - biblioteki, kilka przykładów kodów nadmiarowych encode, decode
- badania - eksperyment numeryczny zbudowanie modelu
- potrajanie bitów - intuicyjny sposób - różne sposoby nadmiarowości
- kanał - uszkadza bity, np. model Gilberta, model…
  różne parametry kanału - mniej lub bardziej zaszumiony
  kody są projektowane pod różne kanały
  kanały różnią się parametrami - prawdopodobieństwem błędu oraz typem błędu
- BER kanału: 10-3, 10-8 - stopień zaszumienia
- wyjście: obserwowana jakość transmisji oraz obniżona prędkość transmisji, zyskujemy jedno, tracimy drugie



### Na kolejne zajęcia:

- model - w sprawozdaniu
- biblioteki kodowe - różne rodziny kodów, kodery i dekodery, różne nadmiarowości
- próbki kodu