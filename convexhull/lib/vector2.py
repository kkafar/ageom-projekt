""" Implementacja wektora dwuwymiarowego """

import numpy as np

class Vector2: 
    def __init__(self, x: float = 0, y: float = 0):
        """ Klasa reprezentująca dwuwymiarowy wektor """
        self.coord = np.array([x, y], dtype='float64')


    @classmethod   
    def from_vec(cls, other):
        """ Tworzy wektor jednakowy z wektorem przekazanym w parametrze """
        return cls(Vector2[0], Vector2[1])

    @classmethod
    def from_subscriptable(cls, other):
        """ Tworzy wektor [ other[0], other[1] ] """
        return cls(other[0], other[1])

    
    def as_array(self) -> np.array:
        """ Zwraca dwu elementową tablicę współrzednych wektora """
        return self.coord


    def x(self) -> float:
        """ Zwraca współrzędną x (odciętą) wektora """
        return self.coord[0]


    def y(self) -> float:
        """ Zwraca współrzędną y (rzędną) wektora """
        return self.coord[1]


    def length(self) -> float:
        """ Zwraca długość wektora """
        return np.sqrt(self.coord[0] * self.coord[0] + self.coord[1] * self.coord[1])


    def lenght_sq(self) -> float:
        """ Zwraca kwadrat długości wektora """
        return (self.coord[0] * self.coord[0] + self.coord[1] * self.coord[1])


    def __add__(self, other):
        """ Zwraca wektor będący sumą wektorową składników """
        return Vector2(self.coord[0] + other[0], self.coord[1] + other[1])


    def __sub__(self, other):
        """ Zwraca wektor będący różnicą wektorowa argumentów. V - U -> [Vx - Ux, Vy - Uy] """
        return Vector2(self.coord[0] - other[0], self.coord[1] - other[1])
    

    def __str__(self):
        return "[" +  str(self.coord[0]) + "," + str(self.coord[1]) + "]"

    
    def __getitem__(self, index: int) -> float:
        """ Zwraca podaną współrzędną wektora """
        return self.coord[index]


    def __mul__(self, other):
        """ Jeżeli argument to wektor: mnożenie skalarne wektorów\n
        Jeżeli argument nie jest wektorem (nie jest sprawdzana poprawnośc typu) to jest traktowany jako liczba i mamy mnożenie przez skalar"""
        if isinstance(other, Vector2):
            return (self.coord[0] * other[0] + self.coord[1] * other[1])
        else:
            return Vector2(other * self.coord[0], other * self.coord[1])


    def __rmul__(self, other):
        """ Jeżeli argument jest liczbą: skalowanie wektora\n
        Jeżeli argument jest wektorem - niezdefiniowane """
        return Vector2(other * self.coord[0], other * self.coord[1])

# ALIAS
Point2 = Vector2