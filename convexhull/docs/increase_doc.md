# Algorytm przyrostowy z sortowaniem 

## Sposób działania

1. Wybieramy pierwsze 3 punkty zbioru, które tworzą obecną otoczkę CH. 
2. Jeżeli weźmiemy jakikolwiek inny punkt wyjściowego zbioru to: 
   1. punkt ten należy do wnętrzna figury wyznaczonej przez CH, wtedy: 
      1. punkt ten na pewno nie należy do otoczki wypukłej wyjściowego zbioru punktów (oczywiste)
   2. punkt ten nie należy do wnętrza figury wyznaczonej przez CH, wtedy:
      1. punkt ten może należeć to otoczki wypukłej wyjściowego zbioru punktów, a zatem powiększamy obecnie znaną otoczkę o nowy punkt, jednocześnie usuwając z niej punkty które po dodaniu nowego znalazły się we wnętrzu nowej, aktualnej otoczki wypukłej. 



## Problemy

1. Algorytmy wyszukujące odpowiednie styczne jako argumenty muszą dostać wielokąty podane w formie listy wierzchołków w **KOLEJNOŚCI ODWROTNEJ DO RUCHU WSKAZÓWEK ZEGARA**.
   1. W takim razie w przypadku pierwszych trzech punktów (pierwsza wzięta otoczka) trzeba zadbać o to, by były podane w odpowiedniej kolejności.
   2. Dokładając każdy kolejny punkt do otoczki (w odpowiedni sposób) ich odpowiednia kolejność zostanie zachowana.
2. W jaki sposób poprawnie powiększać otoczkę? 
   1. W wyniku działania algorytmów znajdujących styczne otrzymujemy 2 indeksy punktów na otoczce.
   2. Wszystkie punkty znajdujące się **pomiędzy** punktami styczności muszą zostać usunięte, a na ich miejsce wstawiamy nowy.
   3. Potrzebujemy w tym celu rozpoznać odpowiedni łańcuch:
      $$ v_{left}, \ldots, v_{right} $$
      lub
      $$ v_{right}, \ldots, v_{left} $$
   4. W jaki sposób to zrobić?
      1. Sprawdzamy poprzednika i następnika jednego z punktów (po której stronie odcinka łączącego punkty styczności leżą), a następnie poruszamy się po odpowiednim łańcuchu 