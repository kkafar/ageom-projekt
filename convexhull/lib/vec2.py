import numpy as np

#############################################################################################
class Vec2: 
    """ Klasa reprezentująca wektor 2D """
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y


    @classmethod
    def from_vec(cls, other):
        """ Inicjalizuje wektor identyczny do przekazanego """
        return cls(other.x, other.y)


    @classmethod
    def from_list(cls, list):
        """ Inicjalizuje wektor z pierwszych dwóch elementów listy """
        return cls(list[0], list[1])

    
    def copy(self):
        """ Zwraca kopię wektora """
        return Vec2(self.x, self.y)
    

    def as_tuple(self):
        """ Zwraca wektor jako krotkę (x, y) """
        return (self.x, self.y)

  
    def as_list(self):
        """ Zwraca wektor jako listę [x, y] """
        return [self.x, self.y]


    def as_array(self):
        """ Zwraca wektor jaka 2 elementową tablicę np.array """
        return np.array([self.x, self.y])


    def length(self):
        return np.sqrt(x**2 + y**2)

    
    def length_sq(self):
        return x * x + y * y


    def __neg__(self):
        """ Zwraca wektor przeciwny """
        return Vec2(self.x, self.y)

    
    def __add__(self, other):
        """ Operator dodawania wektorów. Zwraca nowy wektor. """
        return Vec2(self.x + other.x, self.y + other.y)    

    
    def __sub__(self, other):
        """ Operator odejmowania wektorow. Zwraca nowy wektor. """
        return Vec2(self.x - other.x, self.y - other.y)

    
    def __mul__(self, other): 
        """ Mnożenie skalarne wektorów."""
        return (self.x * other.x + self.y * other.y)

    
    def det(self, other):
        """ Zwraca wyznacznik 2 wektorów"""    
        return (self.x * other.y - self.y * other.x)
#############################################################################################
# Alias dla klasy Vec2
Pnt2 = Vec2
#############################################################################################