import os
from PIL import Image, ImageDraw, ImageFont

base_path = os.path.dirname(os.path.abspath(__file__))
_white = (255,255,255)
_whiteP = os.path.join(base_path, 'planets', '1_2_9_8_10')
_blueP = os.path.join(base_path, 'planets', '11_12')
NorthIndianGraphics = {
    1: {
        "dirPlanet" : _whiteP,
        'bgColor' : (255,69,0),
        'txtColor': _white
    },
    2 : {
        "dirPlanet" : _whiteP,
        'bgColor' : (34,139,34),
        'txtColor': (0,200,0)
    },
    3 : {
        "dirPlanet" : os.path.join(base_path, 'planets', '3'),
        'bgColor' : (255,250,205),
        'txtColor': (139,69,19)
    },
    4 : {
        "dirPlanet" : os.path.join(base_path, 'planets', '4'),
        'bgColor' : (192,192,192),
        'txtColor': (0,0,139)
    },
    5 : {
        "dirPlanet" : os.path.join(base_path, 'planets', '5'),
        'bgColor' : (255,215,0),
        'txtColor': (139,0,0)
    },
    6 : {
        "dirPlanet" : os.path.join(base_path, 'planets', '6'),
        'bgColor' : (144,238,144),
        'txtColor': (0,100,0)
    },
    7 : {
        "dirPlanet" : os.path.join(base_path, 'planets', '7'),
        'bgColor' : (255,182,193),
        'txtColor': (128,0,128)
    },
    8 : {
        "dirPlanet" : _whiteP,
        'bgColor' : (139,0,0),
        'txtColor': _white
    },
    9 : {
        "dirPlanet" : _whiteP,
        'bgColor' : (139,0,0),
        'txtColor': _white
    },
    10 : {
        "dirPlanet" : _whiteP,
        'bgColor' : (169,169,169),
        'txtColor': _white
    },
    11 : {
        "dirPlanet" : os.path.join(base_path, 'planets', _blueP),
        'bgColor' : (30,144,255),
        'txtColor': (0,0,139)
    },
    12 : {
        "dirPlanet" : os.path.join(base_path, 'planets', _blueP),
        'bgColor' : (173,216,230),
        'txtColor': (0,0,139)
    },
}

class ChartDrawer:
    def __init__(self, template_path, font_path):
        self.template = Image.open(template_path).convert("RGBA")
        self.draw = ImageDraw.Draw(self.template)
        self.font = ImageFont.truetype(font_path, 20)
    
    def add_text(self, text, position,size, color):
        """
        Adds text to an image at the specified coordinates with the desired font and color.

        Parameters:
        - text (str): The text to add.
        - position (tuple): The coordinates to place the text (x, y).
        - color (tuple): The color of the text (R, G, B).

        """
        self.draw.text(position, text, font=self.font, fill=color)
    
    def save_chart(self, output_path):
        self.template.save(output_path)
        self.template.show()

class NorthIndianProfiledChart(ChartDrawer):
    def __init__(self,chart : "M_Chart",FirstHouse = None , offWestern = 0, font_name = 'arialbd.ttf',**info):
        isAscChart = False
        if not FirstHouse:
            isAscChart = True
            FirstHouse = chart.Ascendant.Sign
        self.templateGraphics = NorthIndianGraphics[FirstHouse]
        path = os.path.join(base_path, 'NIP_charts', f'{FirstHouse}.png')
        super().__init__(path, 
            os.path.join(base_path,'assets',font_name))
        if(isAscChart):
            self.add_text("ASC",(520,296),20,self.templateGraphics["txtColor"])
            self.add_text(self.format_degree(chart.Ascendant.SignDegree),(516,320),20,self.templateGraphics["txtColor"])
        self.chart_rashis = chart.BhavasWholeSign(FirstHouse,offWestern)
        self.bhava_positions = { # x = planet count
            1: lambda x: [
                [(478, 383)],  # 1 planet
                [(331, 450), (624, 450)],  # 2 planets
                [(478, 383), (331, 450), (624, 450)],  # 3 planets
                [(395, 383),(560, 383)],  # 6 planets (same coordinates for simplification)
            ][x-1 if x <= 4 else 3],  # Corrected index to prevent out of range
            2: lambda x: [
                [(203, 325)],  # 1 planet
                [(203, 293), (203, 355)],  # 2 planets
                [(124, 293), (299, 293), (209, 353)],  # 3 planets
                [(150, 281),(280, 281)]
            ][x-1 if x <= 4 else 3],  # Corrected index to prevent out of range
            3: lambda x: [
                [(10, 458)],  # 1 planet
                [(10, 423), (10, 493)],  # 2 planets
                [(10, 423)],  # 3 planets
                [(10, 378)]
            ][x-1 if x <= 4 else 3],  # Corrected index to prevent out of range
            4: lambda x: [
                [(207, 659)],  # 1 planet
                [(207, 625), (207, 695)],  # 2 planets
                [(207, 625)],  # 3 planets
                [(207, 540)]
            ][x-1 if x <= 4 else 3],  # Corrected index to prevent out of range
            5: lambda x: [
                [(10, 861)],  # 1 planet
                [(10, 827), (10, 897)],  # 2 planets
                [(10, 827)], # 3 planets
                [(10, 790)]
            ][x-1 if x <= 4 else 3],  # Corrected index to prevent out of range
            6: lambda x: [
                [(203, 994)],  # 1 planet
                [(203, 960), (203, 1022)],  # 2 planets
                [(208, 960),(124, 1010), (299, 1010)],  # 3 planets
                [(136, 975), (280, 975)]
            ][x-1 if x <= 4 else 3],  # Corrected index to prevent out of range
            7: lambda x: [
                [(478, 881)],  # 1 planet
                [(331, 881), (624, 881)],  # 2 planets
                [(331, 881), (624, 881), (478, 948)],  # 3 planets
                [(395, 881), (560, 881)],  # 6 planets (same coordinates for simplification)
            ][x-1 if x <= 4 else 3],  # Corrected index to prevent out of range
            8: lambda x: [
                [(752, 994)],  # 1 planet
                [(752, 960), (752, 1022)],  # 2 planets
                [(831, 1010), (656, 1010), (747, 960)],  # 3 planets
                [(819, 975), (675, 975)]
            ][x-1 if x <= 4 else 3],  # Corrected index to prevent out of range
            9: lambda x: [
                [(945, 861)],  # 1 planet
                [(945, 827), (945, 897)],  # 2 planets
                [(945, 827)],  # 3 planets
                [(945, 790)]
            ][x-1 if x <= 4 else 3],  # Corrected index to prevent out of range
            10: lambda x: [
                [(748, 659)],  # 1 planet
                [(748, 625), (748, 695)],  # 2 planets
                [(748, 625)],
                [(748, 540)]
            ][x-1 if x <= 4 else 3],  # Corrected index to prevent out of range
            11: lambda x: [
                [(945, 458)],  # 1 planet
                [(945, 423), (945, 493)],  # 2 planets
                [(945, 423)],
                [(945, 378)]
            ][x-1 if x <= 4 else 3],  # Corrected index to prevent out of range
            12: lambda x: [
                [(752, 325)],  # 1 planet
                [(752, 293), (752, 355)],  # 2 planets
                [(825, 293), (656, 293), (746, 353)],  # 3 planets
                [(675, 281), (805, 281)]
            ][x-1 if x <= 4 else 3],  # Corrected index to prevent out of range
        }
        
        if(info):
            ChartName = info['PersonName'] #y :18 #x:277
            ChartType = "Lagna chart" if not info['ChartType'] else info['ChartType'] #y :58 #x:775
            ChartCity = chart.DrawingManifest['CountryCity'] #y :100 #x:775
            ChartCalculation = chart.DrawingManifest['CalculationMethod'] #y :140 #x:775
            ChartHouseSystem = info['HouseSystem'] #y :160 #x:775
    
    def format_degree(self,number):
        # Split the number into integer and decimal parts
        integer_part = int(number)
        decimal_part = f"{number:.2f}".split('.')[1]
        
        # Format the string
        formatted_string = f'{integer_part}"{decimal_part}°'
        return formatted_string

    def place_positions(self,coordinate,planets):
        #x, y = coordinate
        #planet_x, planet_y = x + position[0], y + position[1]
        planet_x, planet_y = coordinate
        for planet in planets:
            path = os.path.join(self.templateGraphics["dirPlanet"], f'{planet.Name}.png')
            planetimage = Image.open(path).convert("RGBA")
            self.template.paste(planetimage, (planet_x, planet_y),planetimage)
            degree_x, degree_y = planet_x + planetimage.width + 5, planet_y
            
            if planet.PlanetSpeed < 0:
                self.add_text('R', 
            (planet_x - 10, planet_y),20
            , self.templateGraphics['txtColor'])

            self.add_text(self.format_degree(planet.SignDegree), 
            (degree_x, degree_y+10),20
            , '#333')
            planet_y += 45

    def place_planets(self):
        bhavaCounter = 1
        for bhava in self.chart_rashis:
            planets = bhava['karkas']
            coordinates = self.bhava_positions[bhavaCounter](len(planets))
            if len(planets) > 4:
                if len(coordinates) == 2:
                    self.place_positions(coordinates[0],planets[0:3])
                    self.place_positions(coordinates[1],planets[3:])
                else:
                    self.place_positions(coordinates[0],planets)
            if len(planets) == 4:
                if len(coordinates) == 2:
                    self.place_positions(coordinates[0],planets[0:2])
                    self.place_positions(coordinates[1],planets[2:])
                else:
                    self.place_positions(coordinates[0],planets)
            if len(planets) == 3:
                if len(coordinates) == 1:
                    self.place_positions(coordinates[0],planets)
                if len(coordinates) == 3:
                    self.place_positions(coordinates[0],planets[0:1])
                    self.place_positions(coordinates[1],planets[1:2])
                    self.place_positions(coordinates[2],planets[2:3])
            if len(planets) == 2:
                self.place_positions(coordinates[0],planets[0:1])
                self.place_positions(coordinates[1],planets[1:2])
            if len(planets) == 1:
                self.place_positions(coordinates[0],planets[0:1])
            bhavaCounter+=1
    def profileGotov(self,image_path, output_size=(230, 230), position=(20, 18)):
        """
        Resizes and pads an image to make it a square of the specified size, then places it on a new canvas
        at the specified coordinates.

        Parameters:
        - image_path (str): Path to the input image.
        - output_size (tuple): The desired size of the output image (width, height).
        - background_color (tuple): The background color (R, G, B).
        - position (tuple): The coordinates to place the resized image on the new canvas (x, y).

        Returns:
        - Image object with the resized and padded image placed at the specified coordinates.
        """
        background_color = self.templateGraphics['bgColor']
        img = Image.open(image_path).convert("RGBA")
        img.thumbnail(output_size)

        width, height = img.size
        new_img = Image.new('RGBA', output_size, background_color)
        paste_position = ((output_size[0] - width) // 2, (output_size[1] - height) // 2)
        new_img.paste(img, paste_position)

        self.template.paste(new_img, position, new_img)

class NakshatraTable(ChartDrawer):
    def __init__(self,chart : "M_Chart" , font_name = 'arialbd.ttf',**info):
        path = os.path.join(base_path, 'NIP_charts', f'Nakshatra.png')
        super().__init__(path, 
            os.path.join(base_path,'assets',font_name))
    def drawNakshatra(self):
        chart.Moon.Nakshatra