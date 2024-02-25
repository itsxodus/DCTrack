class CamData:
    def __init__(self, time, lon, lat, lonDir="", latDir=""):
        self.time = time
        self.lon = lon[1:]
        self.lat = lat[1:]
        self.lonDir = lon[0]
        self.latDir = lat[0]

    def getTime(self):
        return self.time

    def getLon(self):
        return self.lon

    def getLat(self):
        return self.lat

    def getLoc(self):
        negativeLon = False
        negativeLat = False
        if self.lonDir == "S":
            negativeLon = True
        if self.latDir == "W":
            negativeLat = True
        try:
            formattedLon = float(("-" if negativeLon else "") + self.lon)
            formattedLat = float(("-" if negativeLat else "") + self.lat)
            return (self.getTime(), formattedLon, formattedLat)
        except ValueError:
            return None

    def printData(self):
        return f"At second {self.time}, vehicle is at {self.lon} degrees {self.lonDir} latitude, and {self.lat} degrees {self.latDir} longitude"
