import swisseph as swe
from datetime import datetime , timedelta
from Models.M_Planet import M_Planet
from Models.M_Chart import M_Chart
from Models.M_Nakshatra import M_Nakshatra

swe.set_ephe_path('ephe')

CalcMethods = {
    'Lahiri' : {
        'name' : "Lahiri Ayanamsha",
        'swe_method' : swe.SIDM_LAHIRI
    },
    'UshaShashi' : {
        'name' : "UshaShashi Ayanamsha",
        'swe_method' : swe.SIDM_USHASHASHI
    },
    'SuryaSiddhanta' : {
        'name' : 'Suryasiddhanta Ayanamsha',
        'swe_method' : swe.SIDM_SURYASIDDHANTA
    },
    'JNBhasin' : {
        'name' : 'J. N. Bhasin Ayanamsha',
        'swe_method' : swe.SIDM_JN_BHASIN
    }
}

class AstrologyCalculator:
    def __init__(self, datetime_utc:datetime , 
                TimeZoneOffset:tuple,
                latitude, 
                longitude, 
                sid_method=CalcMethods['Lahiri'],
                countryName = None):
        self.datetime_utc = datetime_utc
        self.latitude = latitude
        self.longitude = longitude
        self.sid_method = sid_method
        self.TimeZoneOffset = TimeZoneOffset
        self.CountryName = countryName or f'{latitude},{longitude}'
        #swe.set_ephe_path('./ephe')
        swe.set_sid_mode(self.sid_method['swe_method'])

    def _calculate_julian_day(self):
        timezone_offset = timedelta(hours=self.TimeZoneOffset[0], minutes=self.TimeZoneOffset[1])
        datetime_utc = self.datetime_utc - timezone_offset
        return swe.julday(datetime_utc.year, datetime_utc.month, datetime_utc.day, 
                          datetime_utc.hour + datetime_utc.minute / 60.0)
    
    def _calculate_position(self, jd, planet, flags):
        position, _ = swe.calc_ut(jd, planet, flags)
        position2, _ = swe.calc_ut(jd + 1, planet, flags) 
        return (position[0],position2[0] - position[0])

    def calculate_chart(self):
        jd = self._calculate_julian_day()
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

        planets = [
            (swe.SUN, "SU"), (swe.MOON, "MO"), (swe.MERCURY, "ME"), 
            (swe.VENUS, "VE"), (swe.MARS, "MA"), (swe.JUPITER, "JU"), 
            (swe.SATURN, "SA"), (swe.URANUS, "UR"), (swe.NEPTUNE, "NE"), 
            (swe.PLUTO, "PL")
        ]
        chart = M_Chart(
            CalculationMethod = self.sid_method,
            CountryCity = self.CountryName,
            Date = self.datetime_utc
        )
        for planet, name in planets:
            degree,speed = self._calculate_position(jd, planet, flags)
            chart.append(M_Planet(name,degree,speed))

        rahuPosition, _ = swe.calc_ut(jd, 10, flags)
        degree,speed = self._calculate_position(jd, 10, flags)
        chart.append(M_Planet('RA', degree,0))
        
        # Calculate Ascendant
        h_sys = b'P'  # Whole sign house system
        cusps, ascmc = swe.houses_ex(jd, self.latitude, self.longitude, h_sys,flags)
        chart.append(M_Planet('ASC', ascmc[0],0))
        return chart

class NakshatraTableCalculator:
    nakshatras = {
        'Aswini': [0, 13.2],
        'Bharani': [13.2, 26.4],
        'Krittika': [26.4, 39.6],
        'Rohini': [39.6, 52.8],
        'Mrigashirsha': [52.8, 66.0],
        'Ardra': [66.0, 79.2],
        'Punarvasu': [79.2, 92.4],
        'Pushya': [92.4, 105.6],
        'Ashlesha': [105.6, 118.8],
        'Magha': [118.8, 132.0],
        'Purva Phalguni': [132.0, 145.2],
        'Uttara Phalguni': [145.2, 158.4],
        'Hasta': [158.4, 171.6],
        'Chitra': [171.6, 184.8],
        'Swati': [184.8, 198.0],
        'Vishakha': [198.0, 211.2],
        'Anuradha': [211.2, 224.4],
        'Jyeshtha': [224.4, 237.6],
        'Mula': [237.6, 250.8],
        'Purva Ashadha': [250.8, 264.0],
        'Uttara Ashadha': [264.0, 277.2],
        'Shravana': [277.2, 290.4],
        'Dhanishtha': [290.4, 303.6],
        'Shatabhisha': [303.6, 316.8],
        'Purva Bhadrapada': [316.8, 330.0],
        'Uttara Bhadrapada': [330.0, 343.2],
        'Revati': [343.2, 360],
    }
    planetaryRuler = {
        'Aswini': 'KE',
        'Bharani': 'VE',
        'Krittika': 'SU',
        'Rohini': 'MO',
        'Mrigashirsha': 'MA',
        'Ardra': 'RA',
        'Punarvasu': 'JU',
        'Pushya': 'SA',
        'Ashlesha': 'ME',
        'Magha': 'KE',
        'Purva Phalguni': 'VE',
        'Uttara Phalguni': 'SU',
        'Hasta': 'MO',
        'Chitra': 'MA',
        'Swati': 'RA',
        'Vishakha': 'JU',
        'Anuradha': 'SA',
        'Jyeshtha': 'ME',
        'Mula': 'KE',
        'Purva Ashadha': 'VE',
        'Uttara Ashadha': 'SU',
        'Shravana': 'MO',
        'Dhanishtha': 'MA',
        'Shatabhisha': 'RA',
        'Purva Bhadrapada': 'JU',
        'Uttara Bhadrapada': 'SA',
        'Revati': 'ME'
    }
    def __init__(self, chart):
        self.chart = chart

    def _getNakshatra(self, planet):
        total_degree = planet.Degree
        IndexPada = 1
        IndexNakshatra = 0

        for nakshatra, (start, end) in self.nakshatras.items():
            if start <= total_degree < end:
                _deg = 0
                while _deg < planet.Degree:
                    IndexPada += 1
                    if planet.Degree <= _deg:
                        break
                    if IndexPada%3:
                        _deg += 3.2
                    else:
                        _deg += 3.6
                    if IndexPada % 4 == 0:
                        IndexNakshatra += 1
                        IndexPada = 0
                break

        planet.Nakshatra = M_Nakshatra(
            name = list(self.nakshatras.keys())[IndexNakshatra-1]
            ,pada = IndexPada or 4
        )
        return planet

    def GetChart(self):
        NakshatraChart = self.Chart.clone()
        NakshatraChart.Moon = self._getNakshatra(self.Chart.Moon)
        NakshatraChart.Mercury = self._getNakshatra(self.Chart.Mercury)
        NakshatraChart.Venus = self._getNakshatra(self.Chart.Venus)
        NakshatraChart.Venus = self._getNakshatra(self.Chart.Venus)
        NakshatraChart.Sun = self._getNakshatra(self.Chart.Sun)
        NakshatraChart.Mars = self._getNakshatra(self.Chart.Mars)
        NakshatraChart.Jupiter = self._getNakshatra(self.Chart.Jupiter)
        NakshatraChart.Saturn = self._getNakshatra(self.Chart.Saturn)
        NakshatraChart.Rahu = self._getNakshatra(self.Chart.Rahu)
        NakshatraChart.Ketu = self._getNakshatra(self.Chart.Ketu)

class NavamshaD9Calculator:
    NavamshaSounds =['Chu','Che','Cho','La',  
    'Lee','Lu','Lay','Lo', #bharani
    'A','Ee', 'Oo', 'Ay', #kritikka
    'O - omega','Va - value','Vi - victor' , 'Vu - wood', #Rohini
    'Ve - Vela','Vo - vocal','Ka - katherine' , 'Kee - Keanu', #mrigrashira
    'Ku - kubrick','Kha - khalsa','Nga - nancy' , 'Chha - chhatri (umberela)', #ardra
    'Kay - katie' , 'Ko - Kodak' , 'Ha - Hart' , 'Hee - Hinano', #purvansu
    'Hoo - hootchie' , 'He - helen' , 'Dah - Darwin', 'Ka - kam', #pushya
    'Dee - Deena' , 'Doo - Dude' , 'Day - David' , 'Doh - Dorothy/Doctor', #ashlesha
    'Ma - magic' , 'Mi - Mia' , 'Mu - Mukti' , 'Me - Meryl', #Magha
    'Mo - Mohicans', 'Ta - Taina' , 'Tee - tina' , 'Too - tooth', #purvaphalguni
    'Tay - taylor', 'To - Tohnamah', 'Pa - pascal' , 'Pee - peter', #uttarphalguni
    'Pu - putin' , 'Sha - shah' , 'Nu - nun' , 'Tu - Turtle', #Hasta
    'Pe - page' , 'Po - police' , 'Ra - rama' , 'Re - ray', #Chitra
    'Ru - Ruth' , 'Re - rex' , 'Ro - robin' , 'Ta - tanya', #swati
    'Ti - teehan' , 'Tu - tuesday' , 'Te - taylor' , 'To - tommy', #vishakha
    'Na - nassau' , 'Ni - nilofer' , 'Nu - nutan' , 'Ne - neha', #anuradha
    'No - nora' , 'Ya - yani', 'Yi - yeast' , 'Yu - yul', #jyetsha
    'Ye - yale' , 'Yo - yoga' , 'Bha - bhang', 'Bhe - bhesh', #mula
    'Bu - bootis', 'Dah - dahl' , 'Bha - bhatt' , 'Dha - dharma', #purvashadha
    'Be - beth', 'Bo - bohemian', 'Ja - jardine' , 'Ji - jimmy',#uttarashadha
    'Ju - jupiter justin','Je - Jennifer jet','Jo - joe','Gha - ghana gastly', #shravama
    'Ga - galileo' , 'Gi - Gibson' , 'Gu - gustav guitar', 'Ge - george gertha', #dhanishta
    'Go - godwin' , 'Sa - sally' , 'Si - Simon' , 'Su - Sun', #shatabhishiba
    'Se - seth',  'So - somalia' , 'The - then' , 'Di - divali', #purvabhadrapada
    'Du - durga' , 'Tha - thatcher' , 'Jha - Jhanci' , 'Na - Natasha', #uttarabhadrapada
    'The - the' , 'Tho - though' , 'Cha - charlie' , 'Chi - chile' #revati
    ]
    _s = list(range(1,13))
    _d = [3.2,4.6,10,13.2,16.4,20,23.2,26.4,30] #harja sign degree azin bozorgtar shod!
    def get_key(self,x):
        if x in [1, 5, 9]:
            return 1
        elif x in [2, 6, 10]:
            return 2
        elif x in [3, 7, 11]:
            return 3
        elif x in [4, 8, 12]:
            return 4
        else:
            return 1

    NavamshaDegree = lambda self,x: {
        1: dict(zip(self._d, self._s[:9])),
        2: dict(zip(self._d, self._s[9:] + self._s[:6])),
        3: dict(zip(self._d, self._s[6:] + self._s[:3])),
        4: dict(zip(self._d, self._s[6:] + self._s[3:]))
    }[self.get_key(x)]

    def __init__(self, chart):
        self.Chart = chart

    def _CalcD9(self,planet):
        _deg = 0
        IndexZvuk = 0
        while _deg < planet.Degree:
            IndexZvuk += 1
            if planet.Degree <= _deg:
                break
            if IndexZvuk%3:
                _deg += 3.2
            else:
                _deg += 3.6
        IndexNav = 0
        _deg = 0
        while _deg < planet.SignDegree:
            IndexNav += 1
            if planet.SignDegree <= _deg:
                break
            if IndexNav%3:
                _deg += 3.2
            else:
                _deg += 3.6
        PlanetD9Sign = self.NavamshaDegree(planet.Sign)
        d9sign = None
        for k in PlanetD9Sign.keys():
            if planet.SignDegree <= k:
                d9sign = PlanetD9Sign[k]
                break
        planet.Sign = d9sign 
        planet.NavamsaZvuk = self.NavamshaSounds[IndexZvuk]
        return planet

    def D9Chart(self) -> M_Chart:
        D9Chart = self.Chart.clone()
        D9Chart.Moon = self._CalcD9(self.Chart.Moon)
        D9Chart.Mercury = self._CalcD9(self.Chart.Mercury)
        D9Chart.Venus = self._CalcD9(self.Chart.Venus)
        D9Chart.Sun = self._CalcD9(self.Chart.Sun)
        D9Chart.Mars = self._CalcD9(self.Chart.Mars)
        D9Chart.Jupiter = self._CalcD9(self.Chart.Jupiter)
        D9Chart.Saturn = self._CalcD9(self.Chart.Saturn)
        D9Chart.Rahu = self._CalcD9(self.Chart.Rahu)
        D9Chart.Ketu = self._CalcD9(self.Chart.Ketu)
        return D9Chart