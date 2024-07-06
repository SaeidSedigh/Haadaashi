_signs = [1,2,3,4,5,6,7,8,9,10,11,12]

class M_Planet:
    def __init__(self, name, degree, speed, nakshatra=None, navamsa=None):
        self.Name = name
        self.Degree = degree
        self.Sign = _signs[int(self.Degree // 30)]
        self.SignDegree = self.Degree % 30
        self.PlanetSpeed = speed
        self.Nakshatra = nakshatra
        self.NavamsaZvuk = None
    def __repr__(self):
        return f"{self.Name}: {self.SignDegree:.2f}° {self.Sign} {self.Nakshatra if self.Nakshatra else ''}"
