## TODO

### W przypadku algorytmu przyrostowego, skonsultować analizę złożoności obliczeniowej!!


1. [x] górna-dolna otoczka
2. [x] górna-dolna otoczka - wizualizacja -- jest jakiś bug, przy pokazywaniu dolnej otoczki, od razu pokazuje wszsytkie jej punkty - a nie powienien
3. [x] przyrostowy
4. [x] przyrostowy -- wizualizacja
5. [x] dziel i rządź 
6. [x] dziel i rządź -- wizualizacja

## Issues

1. [x] Naprawa importów
2. [x] Poprawić obsługę przpadku podstawowego w dziel i rządź (obsługiwać jakimś algorytmem, a nie przy k <= 2)
3. [ ] Dziel i zwyciężaj (małe k w stosunku do N -- błąd)
4. [ ] Chan przy dużych zbiorach punktów się sypie
5. [ ] Przyrostowy przy dużych zbiorach się sypie
6. [ ] Wyczyśić kod z zbędnych funkcji (tych które są już nie używane)
7. [ ] Na końcu zaktualizować kody w sprawozdaniu (dokumentacji)
8. [ ] Zaktaualizować opisy w dokumentacji
9. [ ] Dodać pomiary czasu do prezentacji i sprawozdania
10. [ ] Tabelki z pomiarami czasu do sprawozdania 
11. [ ] Bibliografie (koniecznie mają być, odniesień nie robimy)


# Sprawozdanie / dokumentacja

1. [ ] Część techniczna
    1. [ ] Opis programu ( z jakich modułów jest złożony, wymagania techniczne)
    2. [ ] Sposób obsługi programu (jak korzystać)
2. [ ] Sprawozdanie
    1. [ ] Opis problemu (wyznaczanie otoczki wypukłej)
    2. [ ] Definicje problemu, dowód na dolne ograniczenie złożonośći obliczeniowe, porównanie z sortowaniem
    3. [ ] Opis każdego z algorytmów
        1. [ ] Schemat działania (w punktach, polecenia w jezyku naturalnym)
        2. [ ] Wyjaśnienie szczegółów (np. w jaki sposób jest znajdywana styczna itd.)
        2. [ ] Analiza złożoności obliczeniowej
        4. [ ] Kod (ewentualnie z komentarzami zawierającymi odnośniki do punktów schematu)
        5. [ ] Opis wizualizacji (ewentualny)
    4. [ ] Podsumowanie (tabelka z złożonościami)
    5. [ ] Porównanie czasów wykonania i złożonośći, wykresy (statystyki)
        1. [ ] Dla każdego typu zbioru osobno\


### Typy zbiorów

Testujemy dla n: 1000 - 20000, co 100

1. [ ] Chmura punktów 
2. [ ] Okrąg (R = 500) 
3. [ ] Prostokąt 
4. [ ] Śmieszny kwadrat (bez dwóch boków, z przekątnymi)

# Prezentacja

1. Przedstawienie problemu (opis problemu, definicje, dowód na dolne ograniczenie złożoności obliczeniowej, porównanie z sortowaniem)
2. Opisy kolejnych algorytmów (slajdy powinny zaiwerać pełny opis)

W trakcie prezentacji należy przedstawić sposób działania programu


1. [ ] Slajd tytułowy (podpis, co to za projekt, w ramach czego itd.)
2. [ ] Przedstawienie problemu 
3. [ ] Dowód na dolne ograniczenie czasowe problemu 


3. [ ] Odnoście każdego algorytmu:
    1. [ ] ma być pełen opis
    2. [ ] po opisie, slajdy z animacją (na każdym slajdzie jedna klatka z działania algorytmu na jakimś małym zbiorze punktów)
4. [ ] Bibliografia

## Wszędzie dodać bibliografię i się podpisać 

# Program

1. [ ] Zrobimy jednego jupytera, w którym:
    1. [ ] Instrukcja
    2. [ ] Na początku wygenerujemy punkty
    3. [ ] Będzie można przetestować kolejne algorytmy (zobaczyć jak działają) 
    4. [ ] Do każdego algorytmu krótki opis działania.


