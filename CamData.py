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
        negativeLat = False
        negativeLon = False
        if self.lonDir == "S":
            negativeLon = True
        if self.latDir == "W":
            negativeLat = True
        return str(("-" if negativeLon else "") + self.lon + "," + ("-" if negativeLat else "") + self.lat)

    def printData(self):
        return f"At second {self.time}, vehicle is at {self.lon} degrees {self.lonDir} latitude, and {self.lat} degrees {self.latDir} longitude"
