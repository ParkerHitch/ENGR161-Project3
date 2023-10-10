import grovepi

class groveLightSensor:

    port = 0

    # Initialize a llight sensor on port "A" + analogPort
    def __init__(self, analogPort):
        self.port = analogPort
        grovepi.pinMode(self.port, "INPUT")
    
    # returns a value in the range: [0,1024)
    # higher is brighter reading
    def getRawVal(self):
        return grovepi.analogRead(self.port)
    
    # returns brightness as a percentage [0,1.00]
    # higher percentage = brighter environment
    def getBrightness(self):
        return self.getVal() / 1023.0