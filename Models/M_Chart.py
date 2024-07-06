_months = ['January',"February","March","April","May","June","July","August","September","October","November","December"]
_signs = [1,2,3,4,5,6,7,8,9,10,11,12]
from Models.M_Planet import M_Planet
import copy
class M_Chart:
    #zodiac degree ascmc[0] % 30
    #ZODIAC_SIGNS int(AscendantDegree // 30)
    Ascendant = None
    Moon = None
    Mercury = None
    Venus = None
    Sun = None
    Mars = None
    Jupiter = None
    Saturn = None
    Rahu = None
    Uranus = None
    Neptune = None
    Pluto = None
    def clone(self):
        return copy.deepcopy(self)
    DrawingManifest = {
        'CalculationMethod' : None,
        'CountryCity' : None,
        'Date' : None,
        'FormattedDateTime' : None
    }
    def __repr__(self):
        return f"{self.DrawingManifest['CountryCity']}: {self.DrawingManifest['FormattedDateTime']}° {self.DrawingManifest['CalculationMethod']['name']}"
    def __init__(self,**info):
        for key in info:
            self.DrawingManifest[key] = info[key]
        self.DrawingManifest['FormattedDateTime'] = f"{self.DrawingManifest['Date'].day} {_months[self.DrawingManifest['Date'].month-1]} {self.DrawingManifest['Date'].year} - {self.DrawingManifest['Date'].hour}:{self.DrawingManifest['Date'].minute}"

    def append(self,planetOBJ):
        if (planetOBJ.Name == "MO"):
            self.Moon = planetOBJ
        if (planetOBJ.Name == "ME"):
            self.Mercury = planetOBJ
        if (planetOBJ.Name == "VE"):
            self.Venus = planetOBJ
        if(planetOBJ.Name == "SU"):
            self.Sun = planetOBJ
        if (planetOBJ.Name == "MA"):
            self.Mars = planetOBJ
        if (planetOBJ.Name == "JU"):
            self.Jupiter = planetOBJ
        if (planetOBJ.Name == "SA"):
            self.Saturn = planetOBJ
        if (planetOBJ.Name == "RA"):
            self.Rahu = planetOBJ
            self.Ketu = M_Planet("KE",(self.Rahu.Degree + 180) % 360 , self.Rahu.PlanetSpeed)
        if (planetOBJ.Name == "UR"):
            self.Uranus = planetOBJ
        if (planetOBJ.Name == "NE"):
            self.Neptune = planetOBJ
        if (planetOBJ.Name == "PL"):
            self.Pluto = planetOBJ
        if (planetOBJ.Name == "ASC"):
            self.Ascendant = planetOBJ

    def BhavasWholeSign(self,countFrom=0,offWestern=False):
        if not countFrom:
            return self.BhavasWholeSign(self.Ascendant.Sign)
        resultBhava = []
        rashis = {}
        karkas = [self.Moon,self.Mercury,self.Venus,self.Sun,self.Mars,self.Jupiter,self.Saturn,self.Rahu,self.Ketu,self.Uranus,self.Neptune,self.Pluto]
        if offWestern:
            karkas = karkas[0:9]
        for i in _signs:
            rashis[i] = []
            for karka in karkas:
                if karka:
                    if karka.Sign == i:
                        rashis[i].append(karka)
                        rashis[i].sort(key=lambda obj: obj.SignDegree)
        _toHouse = list(rashis.keys())[countFrom-1:]
        _beforeHouse = list(rashis.keys())[:countFrom-1]
        
        for r in _toHouse:
            resultBhava.append({
                'rashi' : r,
                'karkas' : rashis[r]
            })
        for r in _beforeHouse:
            resultBhava.append({
                'rashi' : r,
                'karkas' : rashis[r]
            })
        return resultBhava
    
    