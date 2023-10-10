
class TwoWheel:

    def __init__(self, BP, portL, portR):
        self.BP = BP
        self.leftP = portL
        self.rightP = portR
        self.setLEncoder(0)
        self.setREncoder(0)

    def setPowers(self, leftPower, rightPower):
        self.BP.setMotorPower(self.leftP, leftPower)
        self.BP.setMotorPower(self.rightP, rightPower)
    
    def getLEncoder(self):
        return self.BP.get_motor_encoder(self.leftP)
    def setLEncoder(self, newPos):
        # lego motors only support offset for some reason.
        self.BP.offset_motor_encoder(self.leftP, newPos + self.getLEncoder())

    def getREncoder(self):
        return self.BP.get_motor_encoder(self.rightP)
    def setREncoder(self, newPos):
        # lego motors only support offset for some reason.
        self.BP.offset_motor_encoder(self.rightP, newPos + self.getREncoder())