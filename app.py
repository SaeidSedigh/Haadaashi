from ChartCalculator import AstrologyCalculator , CalcMethods , NakshatraTableCalculator , NavamshaD9Calculator
from datetime import datetime
from Models.M_Chart import M_Chart
from Models.M_Planet import M_Planet
from ChartDrawer.chartDrawer import NorthIndianProfiledChart
# Example usage

datetime_utc = datetime(2002,7,1 , 9, 15)  # UTC time
latitude = 35.7219  # TEHRAN , IR
longitude = 51.3347  # TEHRAN , IR
#latitude = 56.1036
#longitude = 47.5065
sid_method = CalcMethods['Lahiri']  # Example sidereal method
#'SIDM_LAHIRI', 'SIDM_LAHIRI_1940', 'SIDM_LAHIRI_ICRC', 'SIDM_LAHIRI_VP285'
astrology_calculator = AstrologyCalculator(datetime_utc,(3,30), latitude, longitude, sid_method)
chart = astrology_calculator.calculate_chart()

#graphchart = NorthIndianProfiledChart(chart,chart.Moon.Sign,offWestern=1)
#graphchart.place_planets()
#a = NavamshaD9Calculator(chart).D9Chart()
#print(a.Moon.NavamsaZvuk)
print(NakshatraTableCalculator(chart)._getNakshatra(chart.Venus).Nakshatra.Pada)
#graphchart.profileGotov('ss.jpg')
#graphchart.save_chart('test.png')