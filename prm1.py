from .aptmotor import AptMotor

class PRM1(AptMotor):
    """
    This class provides high level encapsulation of the AptMotor class for the
    PRM1 and the PRM1-Z8 controllers.
    """

    def __init__(self,serial_number=None):
        super(PRM1,self).__init__(hwser=serial_number,stageType='PRM1-Z8')

    def goto(self,abs_pos,channel=0,wait=True):
        self.MoveAbsoluteEnc(channel,abs_pos,wait=wait)

    def move(self,dist,channel=0,wait=True):
        curpos = self.getPosition(channel)
        newpos = curpos + dist
        self.goto(newpos)

    def home(self,channel=0):
        self.zero(channel)

    def position(self,channel=0):
        return self.getPosition(channel)
