from __future__ import absolute_import,print_function,division
from .aptdevice import AptDevice
from . import aptconsts as c

class _AptPiezo(AptDevice):
    """ Wrapper around the messages of the APT protocol specified for piezo controller. The method names (and case) are set the same as in the Thor Labs ActiveX control for compatibility

    !!!! TODO: These are no longer directly compatible with ActiveX control due to the mapping of channel onto destId via self.channelAddresses, therefore it makes more sense to use a cleaner syntax here without
    worrying about compatibility, and if needed make a AptPiezoWrapper(AptPiezo) class which gives versions with identical names. This will prevent cluttering of the namespace as well"""   
    def __init__(self,hwser=None):
        super(_AptPiezo, self).__init__(hwser)
        self.maxVoltage=75.0                # for some unknown reason our device isn't responding to self.GetMaxOPVoltage()
        self.maxExtension=self.GetMaxTravel()
        for ch in range(len(self.channelAddresses)):
            self.SetControlMode(ch)
            self.SetVoltOutput(ch)
            self.initializeConstants(ch)
            # If we wanna receive status update messages then we need to send MGMSG_HW_START_UPDATEMSGS
            # We would additionally need to send server alive messages every 1s, e.g. MGMSG_PZ_ACK_PZSTATUSUPDATE for Piezo
            # However if we don't need broadcasting of the position etc we can just fetch the status via GET_STATUTSUPDATES
        
    def initializeConstants(self,channel=0):
        """ Hack to initialize the pieze controller with constants defined explicitly in aptconsts.
        # TO DO : Make the constants model specific """
        channelID,destAddress=self.channelAddresses[channel]
        #self.writeMessage(c.MGMSG_MOD_SET_DIGOUTPUTS , 0, 0x59,destAddress) # Thor Labs are doing this, but I have no idea if it's necessary, or what 0x59 is since this is supposed to be 0
        self.writeMessage(c.MGMSG_PZ_SET_NTMODE,0x01)
        self.writeMessage(c.MGMSG_PZ_SET_INPUTVOLTSSRC,0x04,destID=destAddress,dataPacket=(channelID,c.PIEZO_INPUT_VOLTS_SRC_SW))
        self.writeMessage(c.MGMSG_PZ_SET_PICONSTS,0x06,destID=destAddress,dataPacket=(channelID,c.PIEZO_PID_PROP_CONST,c.PIEZO_PID_INT_CONST))
        self.writeMessage(c.MGMSG_PZ_SET_IOSETTINGS,0x0A,destID=destAddress,dataPacket=(channelID,c.PIEZO_AMP_CURRENT_LIM,c.PIEZO_AMP_LP_FILTER,c.PIEZO_AMP_FEEDBACK_SIGNAL,c.PIEZO_AMP_BNCMODE_LVOUT))
            
    def SetControlMode(self,channel=0,controlMode=c.PIEZO_OPEN_LOOP_MODE):
        """ When in closed-loop mode, position is maintained by a feedback signal from the piezo actuator. 
        This is only possible when using actuators equipped with position sensing.
        This method sets the control loop status The Control Mode is specified in the Mode parameter as per the main documentation """
        channelID,destAddress=self.channelAddresses[channel]
        self.writeMessage(c.MGMSG_PZ_SET_POSCONTROLMODE,channelID,controlMode,destID=destAddress)

    def GetControlMode(self,channel=0):
        """ Get the control mode of the APT Piezo device"""
        response=self.query(c.MGMSG_PZ_REQ_POSCONTROLMODE,c.MGMSG_PZ_GET_POSCONTROLMODE,channelID,destID=destAddress)
        assert response[1]==channelID, "inconsistent channel in response message from piezocontroller"
        return response[2]
        
    def SetVoltOutput(self,channel=0,voltOutput=0.0):
        """ Used to set the output voltage applied to the piezo actuator. 
        This command is applicable only in Open Loop mode. If called when in Closed Loop mode it is ignored."""
        channelID,destAddress=self.channelAddresses[channel]
        voltParam=self._voltageAsFraction(voltOutput)
        self.writeMessage(c.MGMSG_PZ_SET_OUTPUTVOLTS,destID=destAddress,dataPacket=(channelID,voltParam))

    def GetVoltOutput(self,channel=0):
        """ Get the output voltage of the APT Piezo device. Only applicable when in open-loop mode """
        channelID,destAddress=self.channelAddresses[channel]
        response=self.query(c.MGMSG_PZ_REQ_OUTPUTVOLTS,c.MGMSG_PZ_GET_OUTPUTVOLTS,channelID,destID=destAddress)
        dataPacket=response[-1]
        assert dataPacket[0]==channelID, "inconsistent channel in response message from piezocontroller"
        return self._fractionAsVoltage(dataPacket[1])
            
    def SetPosOutput(self,channel=0,posOutput=10.0):
        """ Used to set the output position of piezo actuator. This command is applicable only in Closed Loop mode. 
        If called when in Open Loop mode it is ignored. 
        The position of the actuator is relative to the datum set for the arrangement using the ZeroPosition method."""
        channelID,destAddress=self.channelAddresses[channel]
        posParam=self._positionAsFraction(posOutput)
        self.writeMessage(c.MGMSG_PZ_SET_OUTPUTPOS,destID=destAddress,dataPacket=(channelID,posParam))

    def GetPosOutput(self,channel=0):
        """ Get the current position of the APT Piezo device. Only applicable when in closed-loop mode"""
        channelID,destAddress=self.channelAddresses[channel]
        response=self.query(c.MGMSG_PZ_REQ_OUTPUTPOS,c.MGMSG_PZ_GET_OUTPUTPOS,channelID,destID=destAddress)
        dataPacket=response[-1]
        assert dataPacket[0]==channelID, "inconsistent channel in response message from piezocontroller"
        return self._fractionAsPosition(dataPacket[1])

    def ZeroPosition(self,channel=0):
        """ This function applies a voltage of zero volts to the actuator associated with the channel specified by the lChanID parameter, and then reads the position. 
        This reading is then taken to be the zero reference for all subsequent position readings. 
        This routine is typically called during the initialisation or re-initialisation of the piezo arrangement. """
        channelID,destAddress=self.channelAddresses[channel]
        self.writeMessage(c.MGMSG_PZ_SET_ZERO,channelID,destID=destAddress)

    def GetMaxTravel(self,channel=0):
        """ In the case of actuators with built in position sensing, the Piezoelectric Control Unit can detect the range of travel of the actuator 
        since this information is programmed in the electronic circuit inside the actuator. 
        This function retrieves the maximum travel for the piezo actuator associated with the channel specified by the Chan Ident parameter, 
        and returns a value (in microns) in the Travel parameter."""
        channelID,destAddress=self.channelAddresses[channel]
        response=self.query(c.MGMSG_PZ_REQ_MAXTRAVEL,c.MGMSG_PZ_GET_MAXTRAVEL,channelID,destID=destAddress)
        dataPacket=response[-1]
        assert dataPacket[0]==channelID, "inconsistent channel in response message from piezocontroller"
        return dataPacket[1]*c.PIEZO_TRAVEL_STEP

    def GetMaxOPVoltage(self,channel=0):
        """ The piezo actuator connected to the unit has a specific maximum operating voltage range: 75, 100 or 150 V. 
        This function gets the maximum voltage for the piezo actuator associated with the specified channel."""
        channelID,destAddress=self.channelAddresses[channel]
        response=self.query(c.MGMSG_PZ_REQ_OUTPUTMAXVOLTS,c.MGMSG_PZ_GET_OUTPUTMAXVOLTS,channelID,destID=destAddress)
        dataPacket=response[-1]
        assert dataPacket[0]==channelID, "inconsistent channel in response message from piezocontroller"
        return dataPacket[1]*c.PIEZO_VOLTAGE_STEP

    def LLGetStatusBits(self,channel=0):
        """ Returns a number of status flags pertaining to the operation of the piezo controller channel specified in the Chan Ident parameter. 
        These flags are returned in a single 32 bit integer parameter and can provide additional useful status information for client application development. 
        The individual bits (flags) of the 32 bit integer value are described in the main documentaton."""
        channelID,destAddress=self.channelAddresses[channel]
        response=self.query(c.MGMSG_PZ_REQ_PZSTATUSBITS,c.MGMSG_PZ_GET_PZSTATUSBITS,channelID,destID=destAddress)
        dataPacket=response[-1]
        assert dataPacket[0]==channelID, "inconsistent channel in response message from piezocontroller"
        return dataPacket[1]

    # Helper methods for the above main methods. Change to mixed case since no need for compatibility with ActiveX control
    def _voltageAsFraction(self,voltage):
        """ specify voltage as short representing fraction of max voltage"""
        return round(c.PIEZO_MAX_VOLT_REPR*voltage/self.maxVoltage) 

    def _fractionAsVoltage(self,voltFraction):
        """ convert voltage from short representing fraction of max voltage"""
        return voltFraction/c.PIEZO_MAX_VOLT_REPR*self.maxVoltage

    def _positionAsFraction(self,position):
        """ specify position as short representing fraction of max displacement. Apparently the max value depends on the unit though :( it might be 0xFFFF"""
        return round(c.PIEZO_MAX_POS_REPR*position/self.maxExtension) 

    def _fractionAsPosition(self,positionFraction):
        """ convert position from short representing fraction of max displacement"""
        return positionFraction/c.PIEZO_MAX_POS_REPR*self.maxExtension

       
class AptPiezo(_AptPiezo):
    """ This class contains higher level methods not provided in the Thor Labs ActiveX control, but are very useful nonetheless """

    def deviceDescriptionStrings(self):
        """ Return a list of strings for which the device description is compatible with this class """
        return ["APT Piezo"]

    def getEnableState(self,channel):
        response=self.query(c.MGMSG_MOD_REQ_CHANENABLESTATE,c.MGMSG_MOD_GET_CHANENABLESTATE,channel)
        assert response[1]==channel
        assert response[2]==c.CHAN_ENABLE_STATE_ENABLED or response[2]==c.CHAN_ENABLE_STATE_DISABLED, "Unrecognized enable state received"
        return response[2]==c.CHAN_ENABLE_STATE_ENABLED
    
    def isZeroing(self,channel):
        """ Check to see if the piezo controller is in the middle of zeroing (6th bit True)"""
        StatusBits=self.LLGetStatusBits(channel)
        return (StatusBits>>5) & 1

    def setPosition(self,channel,position):
        """ Move to specified position if valid, and wait for the measured position to stabilize """
        if position>=0 and position <= self.maxExtension:
            self.SetPosOutput(channel,position)
            t0=time.time()
            while abs(position-self.GetPosOutput(channel))>1.01*c.PIEZO_POSITION_ACCURACY:
                if (time.time()-t0)>c.PIEZO_MOVE_TIMEOUT:
                    print("Timeout error moving to "+str(position)+ 'um on channel '+str(channel))
                    break 
                else:
                    time.sleep(10e-3)

    def getPosition(self,channel):
        """ Get the position of the piezo. This is simply a wrapper for GetPosOutput using mixedCase """
        return self.GetPosOutput(channel)

    def zero(self,channel):
        """ Call the zero method and wait for it to finish """       
        self.ZeroPosition(channel)
        t0=time.time()
        while self.isZeroing(channel):
            if (time.time()-t0)>c.PIEZO_ZERO_TIMEOUT:
                print("Timeout error zeroing channel "+str(channel))
                break 
            else:
                time.sleep(500e-3)

    def moveToCenter(self,channel):
        """ Moves the specified channel to half of its maximum extension"""
        self.setPosition(channel,self.maxExtension/2)
