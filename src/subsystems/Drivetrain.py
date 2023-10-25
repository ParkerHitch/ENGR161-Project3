import math
import config

class TwoWheel:

    def __init__(self, BP, portL, portR):
        self.BP = BP
        self.leftP = portL
        self.rightP = portR
        self.setLEncoder(0)
        self.setREncoder(0)

    def setPowers(self, leftPower, rightPower):
        self.BP.set_motor_power(self.leftP , -int(leftPower * 100))
        self.BP.set_motor_power(self.rightP, -int(rightPower * 100))
    
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


class RearWheelDriveFrontWheelSteer(TwoWheel):

    maxDegMot = 130 # degrees from straight of the steering motor for maximum right
    maxAngWheel = 52.5 # maximum angle wheels can turn to

    # steer offset is value of steering motor when straight
    def __init__(self, BP, portBackLeft, portBackRight, portFront, steerOffset):
        self.BP = BP
        self.leftP = portBackLeft
        self.rightP = portBackRight
        self.portSteer = portFront
        self.motorCenter = steerOffset
        self.setLEncoder(0)
        self.setREncoder(0)

    def setFrontAngle(self, angle):
        self.setFrontPercent(angle/self.maxAngWheel)

    def getFrontPercent(self):
        return (self.BP.get_motor_encoder(self.portSteer)-self.motorCenter) / self.maxDegMot

    # sets percent of steering motors [-1, 1]
    def setFrontPercent(self, percent):
        self.BP.set_motor_position(self.portSteer, self.motorCenter + percent * self.maxDegMot)
    
    # frontAng = angle of front wheels (deg), forward is 0, left is +, right is -
    # speed = deg/s of the faster back wheel
    def drive(self, frontAng, speed):
        self.setFrontAngle(frontAng)
        ang = 90 - math.fabs(frontAng)
        if ang == 90:
            self.setSpeeds(speed, speed)
        else:
            radius = math.tan(math.radians(ang)) * config.Y_SEPARATION + config.BACK_SEPARATION/2
            tanSpeedO = radius * math.radians(speed)
            tanSpeedI = (radius - config.BACK_SEPARATION) * math.radians(speed)
            coefficient = speed / tanSpeedO
            omegaO = coefficient * tanSpeedO
            omegaI = coefficient * tanSpeedI
            
            if frontAng > 0:
                self.setSpeeds(omegaI, omegaO)
            else:
                self.setSpeeds(omegaO, omegaI)

    def setSpeeds(self, speedL, speedR):
        self.BP.set_motor_dps(self.leftP, -speedL)
        self.BP.set_motor_dps(self.rightP, -speedR)
