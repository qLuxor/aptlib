from __future__ import absolute_import,division,print_function
from .aptdevice import AptDevice
from . import aptconsts as c

class _AptMotor(AptDevice):
    """ Wrapper around the messages of the APT protocol specified for motor controller. The method names (and case) are set the same as in the Thor Labs ActiveX control for compatibility

    !!!! TODO: These are no longer directly compatible with ActiveX control due to the mapping of channel onto destId via self.channelAddresses, therefore it makes more sense to use a cleaner syntax here without
    worrying about compatibility, and if needed make a AptMotorWrapper(AptMotor) class which gives versions with identical names. This will prevent cluttering of the namespace as well"""   
    def __init__(self,stageType=c.DEFAULT_STAGE_TYPE,*args,**kwargs):
        super(_AptMotor,self).__init__(*args,**kwargs)
        """ 
        ThorLabs APT ActiveX control does the following on initialization of PRM1-Z8 stage with TDC001 controller
        MGMSG_MOD_SET_CHANENABLESTATE -> 10,02,01,01,50,01 -> in AptDevice init function -> in AptDevice init function
        MGMSG_MOT_SET_VELPARAMS -> 13,04,0E,00,D0,01,01,00,00,00,00,00,93,00,00,00,5F,8D,06,00
        MGMSG_MOT_SET_JOGPARAMS -> 16,04,16,00,D0,01,01,00,02,00,7E,25,00,00,BD,08,00,00,DC,00,00,00,25,D4,09,00,02,00
        MGMSG_MOT_SET_LIMSWITCHPARAMS -> 23,04,10,00,D0,01,01,00,04,00,01,00,80,07,00,00,80,07,00,00,01,00
        MGMSG_MOT_SET_GENMOVEPARAMS -> 3A,04,06,00,D0,01,01,00,80,07,00,00
        MGMSG_MOT_SET_HOMEPARAMS -> 40,04,0E,00,D0,01,01,00,02,00,01,00,5F,8D,06,00,FF,1D,00,00
        MGMSG_MOT_SET_MOVERELPARAMS -> 45,04,06,00,D0,01,01,00,00,0A,00,00
        MGMSG_MOT_SET_MOVEABSPARAMS -> 50,04,06,00,D0,01,01,00,00,00,00,00
        MGMSG_MOT_SET_DCPIDPARAMS -> A0,04,14,00,D0,01,01,00,52,03,00,00,96,00,00,00,A0,0A,00,00,32,00,00,00,0F,00
        MGMSG_MOT_SET_AVMODES -> B3,04,04,00,D0,01,01,00,0F,00
        MGMSG_MOT_SET_BUTTONPARAMS -> B6,04,10,00,D0,01,01,00,01,00,FC,4A,00,00,F9,95,00,00,D0,07,D0,07
        MGMSG_MOT_SET_POTPARAMS -> B0,04,1A,00,D0,01,01,00,14,00,BE,A7,00,00,32,00,B4,46,03,00,50,00,69,8D,06,00,64,00,D1,1A,0D,00
        """
        self.stageType=stageType

        # Initialization procedure for the different stages (only PRM1-Z8 implemented)
        if self.stageType == 'PRM1-Z8':
            # MGMSG_MOT_SET_VELPARAMS
            self.writeMessage(c.MGMSG_MOT_SET_VELPARAMS,dataPacket=(c.CHANNEL_1,0,0x93,0x68d5f))
            # MGMSG_MOT_SET_JOGPARAMS
            self.writeMessage(c.MGMSG_MOT_SET_JOGPARAMS,dataPacket=(c.CHANNEL_1,0x2,0x257e,0x08bd,0xdc,0x9d425,0x2))
            # MGMSG_MOT_SET_LIMSWITCHPARAMS
            self.writeMessage(c.MGMSG_MOT_SET_LIMSWITCHPARAMS,dataPacket=(c.CHANNEL_1,0x4,0x1,0x780,0x780,0x1))
            # MGMSG_MOT_SET_GENMOVEPARAMS
            self.writeMessage(c.MGMSG_MOT_SET_GENMOVEPARAMS,dataPacket=(c.CHANNEL_1,0x780))
            # MGMSG_MOT_SET_HOMEPARAMS
            self.writeMessage(c.MGMSG_MOT_SET_HOMEPARAMS,dataPacket=(c.CHANNEL_1,0x2,0x1,0x68d5f,0x1dff))
            # MGMSG_MOT_SET_MOVERELPARAMS
            self.writeMessage(c.MGMSG_MOT_SET_MOVERELPARAMS,dataPacket=(c.CHANNEL_1,0xa00))
            # MGMSG_MOT_SET_MOVEABSPARAMS
            self.writeMessage(c.MGMSG_MOT_SET_MOVEABSPARAMS,dataPacket=(c.CHANNEL_1,0x0))
            # MGMSG_MOT_SET_DCPIDPARAMS
            self.writeMessage(c.MGMSG_MOT_SET_DCPIDPARAMS,dataPacket=(c.CHANNEL_1,0x352,0x96,0xaa0,0x32,0xf))
            # MGMSG_MOT_SET_AVMODES
            self.writeMessage(c.MGMSG_MOT_SET_AVMODES,dataPacket=(c.CHANNEL_1,0xf))
            # MGMSG_MOT_SET_BUTTONPARAMS
            self.writeMessage(c.MGMSG_MOT_SET_BUTTONPARAMS,dataPacket=(c.CHANNEL_1,0x1,0x4afc,0x95f9,0x7d0,0x7d0))
            # MGMSG_MOT_SET_POTPARAMS
            self.writeMessage(c.MGMSG_MOT_SET_POTPARAMS,dataPacket=(c.CHANNEL_1,0x14,0xa7be,0x32,0x346b4,0x50,0x68d69,0x64,0xd1ad1))
            

    def close(self):
        # Do not stop the movement when closing the device (newer controllers crash)
        #for ch in range(len(self.channelAddresses)):
        #    self.LLMoveStop(ch)
        return super(_AptMotor, self).close()

    def MoveHome(self,channel=0,wait=True):
        """ Home the specified channel and wait for the homed return message to be returned """
        channelID,destAddress=self.channelAddresses[channel]
        waitTime=c.QUERY_TIMEOUT if wait else None
        response=self.query(c.MGMSG_MOT_MOVE_HOME,c.MGMSG_MOT_MOVE_HOMED,channelID,destID=destAddress,waitTime=waitTime)

    def MoveJog(self,channel=0,direction=c.MOTOR_JOG_FORWARD):
        """ Jog the specified channel in the specified direction and wait for the move completed message to be returned """
        channelID,destAddress=self.channelAddresses[channel]
        response=self.query(c.MGMSG_MOT_MOVE_JOG,c.MGMSG_MOT_MOVE_COMPLETED,channelID,direction,destID=destAddress)
    
    def GetPosition(self,channel=0):
        """ Get the position in mm """
        channelID,destAddress=self.channelAddresses[channel]
        response=self.query(c.MGMSG_MOT_REQ_POSCOUNTER,c.MGMSG_MOT_GET_POSCOUNTER,channelID,destID=destAddress)
        posParam=response[-1][-1]
        return self._encToPosition(posParam)

    def MoveAbsoluteEnc(self,channel=0,positionCh1=0.0,positionCh2=0,waitTime=c.QUERY_TIMEOUT,wait=True):
        """ Move the specified channel to the specified absolute position and wait for the move completed message to be returned """
        channelID,destAddress=self.channelAddresses[channel]
        position=positionCh1
        waitTimeParam=waitTime if wait else None
        posParam=self._positionToEnc(position)
        response=self.query(c.MGMSG_MOT_MOVE_ABSOLUTE,c.MGMSG_MOT_MOVE_COMPLETED,0x06,destID=destAddress,dataPacket=(channelID,posParam),waitTime=waitTimeParam)

    def MoveAbsoluteEx(self,channel=0,positionCh1=0.0,positionCh2=0,wait=True):
        """ Wrapper for MoveAbsoluteEx """
        self.MoveAbsoluteEnc(channel,positionCh1,positionCh2,wait=wait)

    def GetStageAxisInfo(self,channel=0):
        """ Get the stage axis info... doesn't seem to be working right now """
        channelID,destAddress=self.channelAddresses[channel]
        response=self.query(c.MGMSG_MOT_REQ_PMDSTAGEAXISPARAMS,c.MGMSG_MOT_GET_PMDSTAGEAXISPARAMS,channelID,destID=destAddress)
        dataPacket=response[-1]
        return dataPacket

    def LLMoveStop(self,channel=0):
        """ Send the stop signal... c.MGMSG_MOT_MOVE_COMPLETED may be returned here if the stage was moving """
        # TODO: deal with the return message
        channelID,destAddress=self.channelAddresses[channel]
        self.writeMessage(c.MGMSG_MOT_MOVE_STOP,channelID,destID=destAddress)
        pass

    def _positionToEnc(self,position):
        """ convert between position in mm (or angle in degrees where applicable) and appropriate encoder units"""
        return round(position*c.getMotorScalingFactors(self.controllerType,self.stageType)["position"])

    def _encToPosition(self,enc):
        """ convert between position in mm (or angle in degrees where applicable) and appropriate encoder units"""
        return enc/c.getMotorScalingFactors(self.controllerType,self.stageType)["position"]
    
    def _velocityToEnc(self,velocity):
        """ convert between velocity in mm/s (angular in degrees/s where applicable) and appropriate encoder units"""
        return round(velocity*c.getMotorScalingFactors(self.controllerType,self.stageType)["velocity"])
    
    def _accelerationToEnc(self,acceleration):
        """ convert between acceleration in mm/s/s (angular in degrees/s/s where applicable) and appropriate encoder units"""
        return round(acceleration*c.getMotorScalingFactors(self.controllerType,self.stageType)["acceleration"])



class AptMotor(_AptMotor):
    """ This class contains higher level methods not provided in the Thor Labs ActiveX control, but are very useful nonetheless """
    def __init__(self,*args,**kwargs):
      super(AptMotor,self).__init__(*args,**kwargs)

    def deviceDescriptionStrings(self):
        # Mapping dictionary between class names and the description string given by the device
        return ['APT DC Motor Controller']
    
    def setPosition(self,position,channel=0):
        self.MoveAbsoluteEnc(channel,position)
    def getPosition(self, channel = 0):
        return self.GetPosition(channel)
    def zero(self,channel=0):
        self.MoveHome(channel)
 
