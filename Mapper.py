import folium


def formatGPSData(data):
    dataArray = []
    for point in data:
        dataArray.append(point[1:])
    return dataArray


class Mapper:
    def __init__(self, title, data):
        self.title = title
        self.gpsData = data
        self.timelessGPSData = formatGPSData(data)

    def createMap(self):
        mapCenter = self.timelessGPSData[0]
        myMap = folium.Map(location=mapCenter, zoom_start=12)

        # Add a Polyline to represent the path
        path_line = folium.PolyLine(locations=self.timelessGPSData, color='blue', weight=5, opacity=0.7)
        path_line.add_to(myMap)

        # Add markers for each GPS point
        for point in self.gpsData:
            time, lat, lon = point
            folium.Marker(
                location=(lat, lon),
                popup=f"{time} seconds in: @ {(lat, lon)}",
                icon=folium.Icon(color='red')
            ).add_to(myMap)

        # Save the map as an HTML file
        myMap.save(f"{self.title}.html")

    def openMapInBrowser(self):
        # Open the HTML file in a web browser
        import webbrowser
        webbrowser.open(f"{self.title}.html")
