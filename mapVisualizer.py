import matplotlib.pyplot as plot
from mpl_toolkits.basemap import Basemap



class DataVis:

    @staticmethod
    def highlight_countries(country_list):
        fig = plot.figure(figsize=(12, 6))
        map = Basemap()

        map.drawcoastlines()
        map.drawcountries()

        for each in country_list:
            map.drawcountries(linewidth=2, color='r')

        plot.title('Album Availability Map')
        plot.show()

