from __future__ import print_function,division
from . import aptconsts as c
import pylibftdi
import time
from struct import pack,unpack,error


# In debug mode we print out all messages which are sent (in hex)
DEBUG_MODE=False

class MessageReceiptError(Exception): pass
class DeviceNotFoundError(Exception): pass

class AptDevice(object):
    """ Wrapper around the Apt protocol via the ftd2xx driver for USB communication with the FT232BM USB peripheral chip in the APT controllers.
   Below is a list of messages defined for all APT devices. Only a small portion of them necessary have been implemented so far taken from the spec
   http://www.thorlabs.com/software/apt/APT_Communications_Protocol_Rev_9.pdf
   The communication uses the pylibftdi driver.
   """

#    def __init__(self,hwser=None):
#        # Find out how many ftd2xx devices are connected to the USB bus
#        numDevices=ftd2xx.createDeviceInfoList()
#        # Check each device to see if either the serial number matches (if given) or the description string is recognized as valid for the class type
#        numMatchingDevices=0
#        for dev in range(numDevices):
#            detail=ftd2xx.getDeviceInfoDetail(dev)
#            if hwser!=None and detail["serial"]!="" and int(detail["serial"])==hwser:
#                # Get the first device which matches the serial number if given
#                numMatchingDevices+=1
#                self.device=device=ftd2xx.open(dev)
#                break
#            elif hwser==None and (detail["description"] in self.deviceDescriptionStrings()):
#                # Get the first device which is valid for the given class if no hwser
#                numMatchingDevices+=1
#                if numMatchingDevices==1:
#                    self.device=device=ftd2xx.open(dev)
#            elif dev==numDevices-1 and numMatchingDevices==0:
#                # Raise an exception if no devices were found
#                if hwser!=None:
#                    errorStr="Hardware serial number " + str(hwser) + " was not found" 
#                else:
#                    errorStr="No devices found matching class name " + type(self).__name__ + ". Expand the definition of CLASS_STRING_MAPPING if necessary"
#                raise DeviceNotFoundError, errorStr
#        # Print a warning message if no serial given and multiple devices were found which matched the class type
#        if numMatchingDevices>1 and hwser==None: 
#            print(str(numMatchingDevices)+" devices found matching " + type(self).__name__ + "; the first device was opened")
#        # Inititalize the device according to FTD2xx and APT requirements
#        device.setBaudRate(ftd2xx.defines.BAUD_115200)
#        device.setDataCharacteristics(ftd2xx.defines.BITS_8,ftd2xx.defines.STOP_BITS_1,ftd2xx.defines.PARITY_NONE)
#        self.delay()
#        device.purge()
#        self.delay()
#        device.resetDevice()
#        device.setFlowControl(ftd2xx.defines.FLOW_RTS_CTS)
#        device.setTimeouts(c.WRITE_TIMEOUT,c.READ_TIMEOUT)
#        # Check first 2 digits of serial number to see if it's normal type or card/slot type, and build self.channelAddresses as list of (chanID,destAddress) tuples
#        self.channelAddresses=[]
#        if device.serial[0:2] in c.BAY_TYPE_SERIAL_PREFIXES:
#            # Get the device info
#            serNum,model,hwtype,firmwareVer,notes,hwVer,modState,numCh=self.query(c.MGMSG_HW_REQ_INFO,c.MGMSG_HW_GET_INFO,destID=c.RACK_CONTROLLER_ID)[-1]
#            # Check each bay to see if it's enabled and also request hardware info
#            for bay in range(numCh):
#                bayId=c.ALL_BAYS[bay]
#                self.writeMessage(c.MGMSG_HW_NO_FLASH_PROGRAMMING,destID=bayId)
#                if self.BayUsed(bay):
#                    bayInfo=self.query(c.MGMSG_HW_REQ_INFO,c.MGMSG_HW_GET_INFO,destID=bayId)[-1]
#                    self.channelAddresses.append((c.CHANNEL_1,bayId))
#        else:
#            # Otherwise just build a list of the channel numbers
#            self.writeMessage(c.MGMSG_HW_NO_FLASH_PROGRAMMING,destID=c.GENERIC_USB_ID)
#            serNum,model,hwtype,firmwareVer,notes,hwVer,modState,numCh=self.query(c.MGMSG_HW_REQ_INFO,c.MGMSG_HW_GET_INFO)[-1]
#            for channel in range(numCh):
#                self.channelAddresses.append((c.ALL_CHANNELS[channel],c.GENERIC_USB_ID))  
#        for channel in range(len(self.channelAddresses)):
#            self.writeMessage(c.MGMSG_MOD_SET_CHANENABLESTATE,1,c.CHAN_ENABLE_STATE_ENABLED,c.RACK_CONTROLLER_ID)            
#            self.EnableHWChannel(channel)
#        # Set the controller type
#        self.controllerType=model.replace("\x00","").strip()
#        # Print a message saying we've connected to the device successfuly
#        print("Connected to %s device with serial number %d. Notes about device: %s"%(model.replace('\x00', ''),serNum,notes.replace('\x00', '')))

# TOTALLY REWRITE THE INIT FUNCTION
    def __init__(self,hwser=None):
      # add Thorlabs devices to USB_PID_LIST -> in the __init__.py script
      #pylibftdi.USB_PID_LIST.append(0xfaf0)

      # Get list of connected devices
      devList = pylibftdi.Driver().list_devices()
      # Find out how many serial devices are connected to the USB bus
      numDevices = len(devList)
#        # Check each device to see if either the serial number matches (if given) or the description string is recognized as valid for the class type
      numMatchingDevices=0
      for dev in range(numDevices):
        detail = devList[dev]
        if hwser!=None and detail[2]!="" and int(detail[2])==hwser:
          # Get the first device which matches the serial number if given
          numMatchingDevices+=1
          self.device=device=pylibftdi.Device(mode='b',device_id=detail[2].decode())
          break
        elif hwser==None and (detail[1].decode() in self.deviceDescriptionStrings()):
          # Get the first device which is valid for the given class if no hwser
          numMatchingDevices+=1
          if numMatchingDevices==1:
            self.device=device=pylibftdi.Device(mode='b',device_id=detail[2].decode())
          elif dev==numDevices-1 and numMatchingDevices==0:
             # Raise an exception if no devices were found
             if hwser!=None:
                 errorStr="Hardware serial number " + str(hwser) + " was not found" 
             else:
                 errorStr="No devices found matching class name " + type(self).__name__ + ". Expand the definition of CLASS_STRING_MAPPING if necessary"
             raise DeviceNotFoundError(errorStr)
      # Print a warning message if no serial given and multiple devices were found which matched the class type
      if numMatchingDevices>1 and hwser==None: 
          print(str(numMatchingDevices)+" devices found matching " + type(self).__name__ + "; the first device was opened")
      # Inititalize the device according to FTD2xx and APT requirements
      device.baudrate = 115200

      # Return exception if there is an error in ftdi function
      def _checked_c(ret):
        if not ret == 0:
          raise Exception(device.ftdi_fn.ftdi_get_error_string())

      _checked_c(device.ftdi_fn.ftdi_set_line_property( 8,  # number of bits
                                                        1,  # number of stop bits
                                                        0   # no parity
                                                        ))
      self.delay()
      device.flush(pylibftdi.FLUSH_BOTH)
      self.delay()

      # Skip the reset part

      # From ftdi.h
      SIO_RTS_CTS_HS = (0x1 << 8)
      _checked_c(device.ftdi_fn.ftdi_setflowctrl(SIO_RTS_CTS_HS))
      _checked_c(device.ftdi_fn.ftdi_setrts(1))

      # Check first 2 digits of serial number to see if it's normal type or card/slot type, and build self.channelAddresses as list of (chanID,destAddress) tuples
      self.channelAddresses=[]
      if device.device_id[0:2] in c.BAY_TYPE_SERIAL_PREFIXES:
        # Get the device info
        serNum,model,hwtype,firmwareVer,notes,hwVer,modState,numCh=self.query(c.MGMSG_HW_REQ_INFO,c.MGMSG_HW_GET_INFO,destID=c.RACK_CONTROLLER_ID)[-1]
        # Check each bay to see if it's enabled and also request hardware info
        for bay in range(numCh):
          bayId=c.ALL_BAYS[bay]
          self.writeMessage(c.MGMSG_HW_NO_FLASH_PROGRAMMING,destID=bayId)
          if self.BayUsed(bay):
            bayInfo=self.query(c.MGMSG_HW_REQ_INFO,c.MGMSG_HW_GET_INFO,destID=bayId)[-1]
            self.channelAddresses.append((c.CHANNEL_1,bayId))
      else:
        # Otherwise just build a list of the channel numbers
        self.writeMessage(c.MGMSG_HW_NO_FLASH_PROGRAMMING,destID=c.GENERIC_USB_ID)
        try:
          serNum,model,hwtype,firmwareVer,notes,hwVer,modState,numCh=self.query(c.MGMSG_HW_REQ_INFO,c.MGMSG_HW_GET_INFO,waitTime=c.INIT_QUERY_TIMEOUT)[-1]
        except:
          print('Device not responding, trying manual initialization')
          numCh = 1
          model = b'TCD001\x00\x00'
          serNum = 00000000
          notes = b'APT DC Motor Controller'
        for channel in range(numCh):
          self.channelAddresses.append((c.ALL_CHANNELS[channel],c.GENERIC_USB_ID))  
      for channel in range(len(self.channelAddresses)):
        self.writeMessage(c.MGMSG_MOD_SET_CHANENABLESTATE,1,c.CHAN_ENABLE_STATE_ENABLED,c.RACK_CONTROLLER_ID)            
        self.EnableHWChannel(channel)
      # Set the controller type
      #print(model)
      #input()
      self.controllerType=model.split(b'\x00',1)[0].decode()
      # Print a message saying we've connected to the device successfuly
      print("Connected to %s device with serial number %d. Notes about device: %s"%(model.split(b'\x00',1)[0].decode(),serNum,notes.split(b'\x00',1)[0].decode()))


        
    def __del__(self):
        if not self.device.closed:
            self.device.close()

    def close(self):
        self.device.close()

    def writeMessage(self,messageID,param1=0x00,param2=0x00,destID=c.GENERIC_USB_ID,sourceID=c.HOST_CONTROLLER_ID,dataPacket=None):
        """ Send message to device given messageID, parameters 1 & 2, destination and sourceID ID, and optional data packet, 
        where dataPacket is an array of numeric values. The method converts all the values to hex according to the protocol
        specification for the message, and sends this to the device."""
        if dataPacket!=None:
            # If a data packet is included then header consists of concatenation of: messageID (2 bytes),number of bytes in dataPacket (2 bytes), destination byte with MSB=1 (i.e. or'd with 0x80), sourceID byte
            try:
                dataPacketStr=pack(c.getPacketStruct(messageID) , *dataPacket)
            except error as e:
                raise error("Error packing message " +hex(messageID)+"; probably the packet structure is recorded incorrectly in c.getPacketStruct()")
            message=pack(c.HEADER_FORMAT_WITH_DATA , messageID , len(dataPacketStr) , destID|0x80 , sourceID) + dataPacketStr
        else:
            # If no data packet then header consists of concatenation of: messageID (2 bytes),param 1 byte, param2 bytes,destination byte, sourceID byte
            message=pack(c.HEADER_FORMAT_WITHOUT_DATA,messageID,param1,param2,destID,sourceID)
        if DEBUG_MODE: self.disp(message,"TX:  ")
        #input()
        numBytesWritten=self.device.write(message)
    
    def query(self,txMessageID,rxMessageID,param1=0,param2=0,destID=c.GENERIC_USB_ID,sourceID=c.HOST_CONTROLLER_ID,dataPacket=None,waitTime=None):
        """ Sends the REQ query message given by txMessageID, and then retrieves the GET response message given by rxMessageID from the device.
        param1,param2,destID,and sourceID for the REQ message can also be specified if non-default values are required.
        The return value is a 7 element tuple with the first 6 values the messageID,param1,param2,destID,sourceID from the GET message header
        and the final value of the tuple is another tuple containing the values of the data packet, or None if there was no data packet.
        A wait parameter can also be optionally specified (in seconds) which introduces a waiting period between writing and reading """
        self.writeMessage(txMessageID,param1,param2,destID,sourceID,dataPacket)
        if waitTime!=None:
            # Keep reading the response until the query timeout is exceeded if wait flag specified
            t0=time.time()
            while True:
                try:
                    response=self.readMessage()
                    break
                except MessageReceiptError:
                    if time.time()-t0 > waitTime/1000: raise
        else:
            # Otherwise just wait for the ordinary read timeout
            response=self.readMessage()
        # Check that the received message is the one which was expected
        if response[0]!=rxMessageID:
            raise MessageReceiptError("Error querying apt device when sending messageID " + hex(txMessageID) + ".... Expected to receive messageID " + hex(rxMessageID) + " but got " + hex(response[0]))
        return response             

    def _read(self,length,waitTime=c.READ_TIMEOUT):
      """
      If block is True, then we will return only when have have length number of
      bytes. Otherwise we will perform a read, then immediately return with
      however many bytes we managed to read.

      Note that if no data is available, then an empty byte string will be
      returned.
      """
      data = bytes()
      t0 = time.time()
      while len(data) < length:
        diff = length - len(data)
        data += self.device.read(diff)
        if waitTime!=None and time.time()-t0 > waitTime/1000:
          break

        time.sleep(0.001)

      return data

      

    def readMessage(self):
        """ Read a single message from the device and return tuple of messageID, parameters 1 & 2, destination and sourceID ID, and data packet 
        (if included), where dataPacket is a tuple of all the message dependent parameters decoded from hex, 
        as specified in the protocol documentation. Normally the user doesn't need to call this method as it's automatically called by query()"""
        # Read 6 byte header from device
        headerRaw=self._read(c.NUM_HEADER_BYTES)
        if headerRaw==b'': raise MessageReceiptError("Timeout reading from the device")
        # Check if a data packet is attached (i.e. get the 5th byte and check if the MSB is set)
        #print(headerRaw)
        self.disp(headerRaw)
        #input()
        #isDataPacket=unpack("B",headerRaw[4])[0]>>7
        isDataPacket = headerRaw[4]>>7
        #print(isDataPacket)
        #input()
        # Read data packet if it exists, and interpret the message accordingly
        if isDataPacket:
            header=unpack(c.HEADER_FORMAT_WITH_DATA,headerRaw)
            messageID=header[0]
            dataPacketLength=header[1]
            param1=None
            param2=None
            destID=header[2]
            sourceID=header[3]
            destID=destID&0x7F
            dataPacketRaw=self._read(dataPacketLength)
            if DEBUG_MODE: self.disp(headerRaw+dataPacketRaw,"RX:  ")
            try:
                dataPacket=unpack(c.getPacketStruct(messageID),dataPacketRaw)
            except error as e:
                # If an error occurs, it's likely due to a problem with the manual inputted data for packet structure in aptconsts
                raise
        else:
            if DEBUG_MODE: self.disp(headerRaw,"RX:  ")
            header=unpack(c.HEADER_FORMAT_WITHOUT_DATA,headerRaw)
            messageID=header[0]
            param1=header[1]
            param2=header[2]
            destID=header[3]
            sourceID=header[4]
            dataPacket=None
        # Return tuple containing all the message parameters
        return (messageID,param1,param2,destID,sourceID,dataPacket)
    
    def delay(self,delayTime=c.PURGE_DELAY):
        """ Sleep for specified time given in ms """
        time.sleep(delayTime/1000)
        
    def disp(self,s,prefixStr="",suffixStr=""):
        """ Convenience method to give the hex for a raw string """
        dispStr=prefixStr + str([hex(c) for c in s]) + suffixStr
        #dispStr = prefixStr + str(s) + suffixStr
        #print(dispStr)


    def BayUsed(self,bayId):
        """ Check if the specified bay is occupied """
        response=self.query(c.MGMSG_RACK_REQ_BAYUSED,c.MGMSG_RACK_GET_BAYUSED,bayId,0,c.RACK_CONTROLLER_ID)
        state=response[2]
        if state==c.BAY_OCCUPIED:
            return True
        elif state==c.BAY_EMPTY:
            return False
        else:
            raise MessageReceiptError("Invalid response from MGMSG_RACK_REQ_BAYUSED")

    def EnableHWChannel(self,channel=0):
        """ Sent to enable the specified drive channel. """       
        channelID,destAddress=self.channelAddresses[channel]
        self.writeMessage(c.MGMSG_MOD_SET_CHANENABLESTATE,channelID,c.CHAN_ENABLE_STATE_ENABLED,destAddress)

    def DisableHWChannel(self,channel=0):
        """ Sent to disable the specified drive channel. """       
        channelID,destAddress=self.channelAddresses[channel]
        self.writeMessage(c.MGMSG_MOD_SET_CHANENABLESTATE,channelID,c.CHAN_ENABLE_STATE_DISABLED,destAddress)


