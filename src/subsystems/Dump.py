class Dump:
    def __init__(self, BP, port):
        self.BP = BP
        self.dumpPort = port
        self.setEncoder(0)

    def getEncoder(self):
        return self.BP.get_motor_encoder(self.dumpPort)
    def setEncoder(self, newPos):
        # lego motors only support offset for some reason.
        self.BP.offset_motor_encoder(self.dumpPort, newPos + self.getEncoder())

    def idle(self):
        self.BP.set_motor_position(self.dumpPort, 5)
    
    def dump(self):
        if(self.BP.get_motor_encoder(self.dumpPort) > -45):
            self.BP.set_motor_power(self.dumpPort, -0.2)
        else:
            self.BP.set_motor_position(self.dumpPort, -45)
