from __future__ import division

# Header structure with and without data packet attached
NUM_HEADER_BYTES=6  # number of bytes to read for message headers
HEADER_FORMAT_WITHOUT_DATA = '<HBBBB'
HEADER_FORMAT_WITH_DATA = '<HHBB'
# Packet Structures (list of bytes required for each value in the packet)
def getPacketStruct(msgID):
    """ given msgID return a format string which can be used by struct.pack and struct.unpack to convert the message data packet to and from hex.
   Note: all messages with data packets should be accounted for here, but there are almost certainly data entry errors, so some may be missing or incorrect. Few of them have been tested """
    # 1 word
    if msgID in [0x07D1,0x07D3,0x07E8,0x07EA,0x0875]:
        return '<H'
    # 2 words
    elif msgID in [0x042C,0x04B3,0x04B5,0x04FB,0x04FD,0x0643,0x0645,0x0646,0x0648,0x0652,0x0654,0x07D0,0x0651,0x0609,0x0611,0x07E7]:
        return '<HH'
    # 3 words
    elif msgID in [0x0655,0x0657,0x0700,0x0702,0x04B9,0x0680,0x0682,0x0683,0x0685,0x07DE]:
        return '<HHH'
    # 5 words
    elif msgID in [0x0426,0x0428,0x07D4,0x07D6,0x0670,0x0672]:
        return '<HHHHH'
    # 6 words
    elif msgID in [0x04E0,0x04E2,0x0618,0x0620]:
        return '<HHHHHH'
    # 7 words
    elif msgID in [0x07DA,0x07DC,0x04DA,0x04DC,0x04E0,0x04E2]:
        return '<HHHHHHH'
    # 9 words
    elif msgID in [0x04E9,0x04EB]:
        return '<HHHHHHHHH'
    # 1 word + 1 long
    elif msgID in [0x043A,0x0445,0x0450,0x0410,0x0412,0x0409,0x040B,0x0453]:
        return "<Hl"
    # 1 word + 3 longs
    elif msgID in [0x043C,0x0447,0x0452,0x0448,0x0413,0x0415]:
        return "<Hlll"
    elif msgID in [0x0481,0x0466,0x0464]:
        return "<HllI"
    elif msgID in [0x04A0,0x04A2,0x04E6,0x04E8]:
        return "<HllllH"
    elif msgID in [0x0703,0x0705,0x04C3,0x04C5]:
        return "<HHHllllHlH"
    elif msgID in [0x042A]:
        return "<HlllH"
    elif msgID in [0x065C,0x063F]:
        return "<HI"
    elif msgID in [0x0440,0x0442]:
        return "<HHHll"
    elif msgID in [0x0416,0x0418]:
        return "<HHllllH"
    elif msgID in [0x0423,0x0425]:
        return "<HHHllH"
    elif msgID in [0x04B0,0x04B2]:
        return "<HHlHlHlHl"
    elif msgID in [0x04B6,0x04B8]:
        return "<HHllHH"
    elif msgID in [0x04E3,0x04E5]:
        return "<HHIHH"
    elif msgID in [0x04D7,0x04D9]:
        return "<HHHIHHHHHIHH"
    elif msgID in [0x04F0,0x04F2]:
        return "<HH16sIIlllllHHHHIIII"
    elif msgID in [0x0606,0x0608]:
        return "<f"
    elif msgID in [0x0621,0x0623]:
        return "<"+("H"*32)
    elif msgID in [0x0626,0x0628]:
        return "<Hhh"
    elif msgID in [0x0630,0x0632]:
        return "<HhhhHH"
    elif msgID in [0x0633,0x0635]:
        return "<Hh"
    elif msgID in [0x0636,0x0638]:
        return "<l"
    elif msgID in [0x07EB,0x07ED]:
        return "<hh4x"
    elif msgID==0x0661:
        return "<HhhI"
    elif msgID==0x0081:
        return "<HH64s"
    elif msgID==0x0006:
        return '<l8sHI48s12xHHH'
    elif msgID==0x0227:
        return "<I"
    elif msgID==0x0491:
        return "<HlHHI"
    elif msgID ==0x0614:
        return "<HHfHHH"
    elif msgID ==0x063A:
        return "<fHH"
    elif msgID ==0x0665:
        return "<HHHfHHHIhhh"
    elif msgID ==0x0821:
        return "<HHI"
    elif msgID ==0x0881:
        return "<hhHhhI"
    elif msgID in [0x0800,0x0802,0x0870,0x0872]:
        raise Exception("Message " + hex(msgID) + " has a variable data packet structure due to the use of submessages, which hasn't been implemented yet")
    else:
        raise Exception("Message " + hex(msgID) + " does not have a packet structure specified. Please check the documentation for this messageID")
  
# Message codes for all the standard APT messages (only a small fraction of these are actually implemented)
MGMSG_MOD_IDENTIFY = 0x0223
MGMSG_MOD_SET_CHANENABLESTATE = 0x0210
MGMSG_MOD_REQ_CHANENABLESTATE = 0x0211
MGMSG_MOD_GET_CHANENABLESTATE = 0x0212
MGMSG_HW_DISCONNECT = 0x0002
MGMSG_HW_RESPONSE = 0x0080
MGMSG_HW_RICHRESPONSE = 0x0081
MGMSG_HW_START_UPDATEMSGS = 0x0011
MGMSG_HW_STOP_UPDATEMSGS = 0x0012
MGMSG_HW_REQ_INFO = 0x0005
MGMSG_HW_GET_INFO = 0x0006
MGMSG_RACK_REQ_BAYUSED = 0x0060
MGMSG_RACK_GET_BAYUSED = 0x0061
MGMSG_HUB_REQ_BAYUSED = 0x0065
MGMSG_HUB_GET_BAYUSED = 0x0066
MGMSG_RACK_REQ_STATUSBITS = 0x0226
MGMSG_RACK_GET_STATUSBITS = 0x0227
MGMSG_RACK_SET_DIGOUTPUTS = 0x0228
MGMSG_RACK_REQ_DIGOUTPUTS = 0x0229
MGMSG_RACK_GET_DIGOUTPUTS = 0x0230
MGMSG_MOD_SET_DIGOUTPUTS = 0x0213
MGMSG_MOD_REQ_DIGOUTPUTS = 0x0214
MGMSG_MOD_GET_DIGOUTPUTS = 0x0215
# Message codes for all the motor related messages
MGMSG_HW_YES_FLASH_PROGRAMMING = 0x0017
MGMSG_HW_NO_FLASH_PROGRAMMING = 0x0018
MGMSG_MOT_SET_POSCOUNTER = 0x0410
MGMSG_MOT_REQ_POSCOUNTER = 0x0411
MGMSG_MOT_GET_POSCOUNTER = 0x0412
MGMSG_MOT_SET_ENCCOUNTER = 0x0409
MGMSG_MOT_REQ_ENCCOUNTER = 0x040A
MGMSG_MOT_GET_ENCCOUNTER = 0x040B
MGMSG_MOT_SET_VELPARAMS = 0x0413
MGMSG_MOT_REQ_VELPARAMS = 0x0414
MGMSG_MOT_GET_VELPARAMS = 0x0415
MGMSG_MOT_SET_JOGPARAMS = 0x0416
MGMSG_MOT_REQ_JOGPARAMS = 0x0417
MGMSG_MOT_GET_JOGPARAMS = 0x0418
MGMSG_MOT_REQ_ADCINPUTS = 0x042B
MGMSG_MOT_GET_ADCINPUTS = 0x042C
MGMSG_MOT_SET_POWERPARAMS = 0x0426
MGMSG_MOT_REQ_POWERPARAMS = 0x0427
MGMSG_MOT_GET_POWERPARAMS = 0x0428
MGMSG_MOT_SET_GENMOVEPARAMS = 0x043A
MGMSG_MOT_REQ_GENMOVEPARAMS = 0x043B
MGMSG_MOT_GET_GENMOVEPARAMS = 0x043C
MGMSG_MOT_SET_MOVERELPARAMS = 0x0445
MGMSG_MOT_REQ_MOVERELPARAMS = 0x0446
MGMSG_MOT_GET_MOVERELPARAMS = 0x0447
MGMSG_MOT_SET_MOVEABSPARAMS = 0x0450
MGMSG_MOT_REQ_MOVEABSPARAMS = 0x0451
MGMSG_MOT_GET_MOVEABSPARAMS = 0x0452
MGMSG_MOT_SET_HOMEPARAMS = 0x0440
MGMSG_MOT_REQ_HOMEPARAMS = 0x0441
MGMSG_MOT_GET_HOMEPARAMS = 0x0442
MGMSG_MOT_SET_LIMSWITCHPARAMS = 0x0423
MGMSG_MOT_REQ_LIMSWITCHPARAMS = 0x0424
MGMSG_MOT_GET_LIMSWITCHPARAMS = 0x0425
MGMSG_MOT_MOVE_HOME = 0x0443
MGMSG_MOT_MOVE_HOMED = 0x0444
MGMSG_MOT_MOVE_RELATIVE = 0x0448
MGMSG_MOT_MOVE_COMPLETED = 0x0464
MGMSG_MOT_MOVE_ABSOLUTE = 0x0453
MGMSG_MOT_MOVE_JOG = 0x046A
MGMSG_MOT_MOVE_VELOCITY = 0x0457
MGMSG_MOT_MOVE_STOP = 0x0465
MGMSG_MOT_MOVE_STOPPED = 0x0466
MGMSG_MOT_SET_DCPIDPARAMS = 0x04A0
MGMSG_MOT_REQ_DCPIDPARAMS = 0x04A1
MGMSG_MOT_GET_DCPIDPARAMS = 0x04A2
MGMSG_MOT_SET_AVMODES = 0x04B3
MGMSG_MOT_REQ_AVMODES = 0x04B4
MGMSG_MOT_GET_AVMODES = 0x04B5
MGMSG_MOT_SET_POTPARAMS = 0x04B0
MGMSG_MOT_REQ_POTPARAMS = 0x04B1
MGMSG_MOT_GET_POTPARAMS = 0x04B2
MGMSG_MOT_SET_BUTTONPARAMS = 0x04B6
MGMSG_MOT_REQ_BUTTONPARAMS = 0x04B7
MGMSG_MOT_GET_BUTTONPARAMS = 0x04B8
MGMSG_MOT_SET_EEPROMPARAMS = 0x04B9
MGMSG_MOT_SET_PMDPOSITIONLOOPPARAMS = 0x04D7
MGMSG_MOT_REQ_PMDPOSITIONLOOPPARAMS = 0x04D8
MGMSG_MOT_GET_PMDPOSITIONLOOPPARAMS = 0x04D9
MGMSG_MOT_SET_PMDMOTOROUTPUTPARAMS = 0x04DA
MGMSG_MOT_REQ_PMDMOTOROUTPUTPARAMS = 0x04DB
MGMSG_MOT_GET_PMDMOTOROUTPUTPARAMS = 0x04DC
MGMSG_MOT_SET_PMDTRACKSETTLEPARAMS = 0x04E0
MGMSG_MOT_REQ_PMDTRACKSETTLEPARAMS = 0x04E1
MGMSG_MOT_GET_PMDTRACKSETTLEPARAMS = 0x04E2
MGMSG_MOT_SET_PMDPROFILEMODEPARAMS = 0x04E3
MGMSG_MOT_REQ_PMDPROFILEMODEPARAMS = 0x04E4
MGMSG_MOT_GET_PMDPROFILEMODEPARAMS = 0x04E5
MGMSG_MOT_SET_PMDJOYSTICKPARAMS = 0x04E6
MGMSG_MOT_REQ_PMDJOYSTICKPARAMS = 0x04E7
MGMSG_MOT_GET_PMDJOYSTICKPARAMS = 0x04E8
MGMSG_MOT_SET_PMDCURRENTLOOPPARAMS = 0x04D4
MGMSG_MOT_REQ_PMDCURRENTLOOPPARAMS = 0x04D5
MGMSG_MOT_GET_PMDCURRENTLOOPPARAMS = 0x04D6
MGMSG_MOT_SET_PMDSETTLEDCURRENTLOOPPARAMS = 0x04E9
MGMSG_MOT_REQ_PMDSETTLEDCURRENTLOOPPARAMS = 0x04EA
MGMSG_MOT_GET_PMDSETTLEDCURRENTLOOPPARAMS = 0x04EB
MGMSG_MOT_SET_PMDSTAGEAXISPARAMS = 0x04F0
MGMSG_MOT_REQ_PMDSTAGEAXISPARAMS = 0x04F1
MGMSG_MOT_GET_PMDSTAGEAXISPARAMS = 0x04F2
MGMSG_MOT_GET_STATUSUPDATE = 0x0481
MGMSG_MOT_REQ_STATUSUPDATE = 0x0480
MGMSG_MOT_GET_DCSTATUSUPDATE = 0x0491
MGMSG_MOT_REQ_DCSTATUSUPDATE = 0x0490
MGMSG_MOT_ACK_DCSTATUSUPDATE = 0x0492
MGMSG_MOT_REQ_STATUSBITS = 0x0429
MGMSG_MOT_GET_STATUSBITS = 0x042A
MGMSG_MOT_SUSPEND_ENDOFMOVEMSGS = 0x046B
MGMSG_MOT_RESUME_ENDOFMOVEMSGS = 0x046C
MGMSG_MOT_SET_TRIGGER = 0x0500
MGMSG_MOT_REQ_TRIGGER = 0x0501
MGMSG_MOT_GET_TRIGGER = 0x0502
MGMSG_MOT_SET_TDIPARAMS = 0x04FB
MGMSG_MOT_REQ_TDIPARAMS = 0x04FC
MGMSG_MOT_GET_TDIPARAMS = 0x04FD
# Message codes for all the solenoid related messages
MGMSG_MOT_SET_SOL_OPERATINGMODE = 0x04C0
MGMSG_MOT_REQ_SOL_OPERATINGMODE = 0x04C1
MGMSG_MOT_GET_SOL_OPERATINGMODE = 0x04C2
MGMSG_MOT_SET_SOL_CYCLEPARAMS = 0x04C3
MGMSG_MOT_REQ_SOL_CYCLEPARAMS = 0x04C4
MGMSG_MOT_GET_SOL_CYCLEPARAMS = 0x04C5
MGMSG_MOT_SET_SOL_INTERLOCKMODE = 0x04C6
MGMSG_MOT_REQ_SOL_INTERLOCKMODE = 0x04C7
MGMSG_MOT_GET_SOL_INTERLOCKMODE = 0x04C8
MGMSG_MOT_SET_SOL_STATE = 0x04CB
MGMSG_MOT_REQ_SOL_STATE = 0x04CC
MGMSG_MOT_GET_SOL_STATE = 0x04CD
# Message codes for all the piezo related messages
MGMSG_PZ_SET_POSCONTROLMODE = 0x0640
MGMSG_PZ_REQ_POSCONTROLMODE = 0x0641
MGMSG_PZ_GET_POSCONTROLMODE = 0x0642
MGMSG_PZ_SET_OUTPUTVOLTS = 0x0643
MGMSG_PZ_REQ_OUTPUTVOLTS = 0x0644
MGMSG_PZ_GET_OUTPUTVOLTS = 0x0645
MGMSG_PZ_SET_OUTPUTPOS = 0x0646
MGMSG_PZ_REQ_OUTPUTPOS = 0x0647
MGMSG_PZ_GET_OUTPUTPOS = 0x0648
MGMSG_PZ_SET_INPUTVOLTSSRC = 0x0652
MGMSG_PZ_REQ_INPUTVOLTSSRC = 0x0653
MGMSG_PZ_GET_INPUTVOLTSSRC = 0x0654
MGMSG_PZ_SET_PICONSTS = 0x0655
MGMSG_PZ_REQ_PICONSTS = 0x0656
MGMSG_PZ_GET_PICONSTS = 0x0657
MGMSG_PZ_REQ_PZSTATUSBITS = 0x065B
MGMSG_PZ_GET_PZSTATUSBITS = 0x065C
MGMSG_PZ_GET_PZSTATUSUPDATE = 0x0661
MGMSG_PZ_ACK_PZSTATUSUPDATE = 0x0662
MGMSG_PZ_SET_OUTPUTLUT = 0x0700
MGMSG_PZ_REQ_OUTPUTLUT = 0x0701
MGMSG_PZ_GET_OUTPUTLUT = 0x0702
MGMSG_PZ_SET_OUTPUTLUTPARAMS = 0x0703
MGMSG_PZ_REQ_OUTPUTLUTPARAMS = 0x0704
MGMSG_PZ_GET_OUTPUTLUTPARAMS = 0x0705
MGMSG_PZ_START_LUTOUTPUT = 0x0706
MGMSG_PZ_STOP_LUTOUTPUT = 0x0707
MGMSG_PZ_SET_EEPROMPARAMS = 0x07D0
MGMSG_PZ_SET_TPZ_DISPSETTINGS = 0x07D1
MGMSG_PZ_REQ_TPZ_DISPSETTINGS = 0x07D2
MGMSG_PZ_GET_TPZ_DISPSETTINGS = 0x07D3
MGMSG_PZ_SET_TPZ_IOSETTINGS = 0x07D4
MGMSG_PZ_REQ_TPZ_IOSETTINGS = 0x07D5
MGMSG_PZ_GET_TPZ_IOSETTINGS = 0x07D6
MGMSG_PZ_SET_ZERO = 0x0658
MGMSG_PZ_REQ_MAXTRAVEL = 0x0650
MGMSG_PZ_GET_MAXTRAVEL = 0x0651
MGMSG_PZ_SET_IOSETTINGS = 0x0670
MGMSG_PZ_REQ_IOSETTINGS = 0x0671
MGMSG_PZ_GET_IOSETTINGS = 0x0672
MGMSG_PZ_SET_OUTPUTMAXVOLTS = 0x0680
MGMSG_PZ_REQ_OUTPUTMAXVOLTS = 0x0681
MGMSG_PZ_GET_OUTPUTMAXVOLTS = 0x0682
MGMSG_PZ_SET_TPZ_SLEWRATES = 0x0683
MGMSG_PZ_REQ_TPZ_SLEWRATES = 0x0684
MGMSG_PZ_GET_TPZ_SLEWRATES = 0x0685
MGMSG_MOT_SET_PZSTAGEPARAMDEFAULTS = 0x0686
MGMSG_PZ_SET_LUTVALUETYPE = 0x0708
MGMSG_PZ_SET_TSG_IOSETTINGS = 0x07DA
MGMSG_PZ_REQ_TSG_IOSETTINGS = 0x07DB
MGMSG_PZ_GET_TSG_IOSETTINGS = 0x07DC
MGMSG_PZ_REQ_TSG_READING = 0x07DD
MGMSG_PZ_GET_TSG_READING = 0x07DE
# Message codes for all the NanoTrak related messages
MGMSG_PZ_SET_NTMODE = 0x0603
MGMSG_PZ_REQ_NTMODE = 0x0604
MGMSG_PZ_GET_NTMODE = 0x0605
MGMSG_PZ_SET_NTTRACKTHRESHOLD = 0x0606
MGMSG_PZ_REQ_NTTRACKTHRESHOLD = 0x0607
MGMSG_PZ_GET_NTTRACKTHRESHOLD = 0x0608
MGMSG_PZ_SET_NTCIRCHOMEPOS = 0x0609
MGMSG_PZ_REQ_NTCIRCHOMEPOS = 0x0610
MGMSG_PZ_GET_NTCIRCHOMEPOS = 0x0611
MGMSG_PZ_MOVE_NTCIRCTOHOMEPOS = 0x0612
MGMSG_PZ_REQ_NTCIRCCENTREPOS = 0x0613
MGMSG_PZ_GET_NTCIRCCENTREPOS = 0x0614
MGMSG_PZ_SET_NTCIRCPARAMS = 0x0618
MGMSG_PZ_REQ_NTCIRCPARAMS = 0x0619
MGMSG_PZ_GET_NTCIRCPARAMS = 0x0620
MGMSG_PZ_SET_NTCIRCDIA = 0x061A
MGMSG_PZ_SET_NTCIRCDIALUT = 0x0621
MGMSG_PZ_REQ_NTCIRCDIALUT = 0x0622
MGMSG_PZ_GET_NTCIRCDIALUT = 0x0623
MGMSG_PZ_SET_NTPHASECOMPPARAMS = 0x0626
MGMSG_PZ_REQ_NTPHASECOMPPARAMS = 0x0627
MGMSG_PZ_GET_NTPHASECOMPPARAMS = 0x0628
MGMSG_PZ_SET_NTTIARANGEPARAMS = 0x0630
MGMSG_PZ_REQ_NTTIARANGEPARAMS = 0x0631
MGMSG_PZ_GET_NTTIARANGEPARAMS = 0x0632
MGMSG_PZ_SET_NTGAINPARAMS = 0x0633
MGMSG_PZ_REQ_NTGAINPARAMS = 0x0634
MGMSG_PZ_GET_NTGAINPARAMS = 0x0635
MGMSG_PZ_SET_NTTIALPFILTERPARAMS = 0x0636
MGMSG_PZ_REQ_NTTIALPFILTERPARAMS = 0x0637
MGMSG_PZ_GET_NTTIALPFILTERPARAMS = 0x0638
MGMSG_PZ_REQ_NTTIAREADING = 0x0639
MGMSG_PZ_GET_NTTIAREADING = 0x063A
MGMSG_PZ_SET_NTFEEDBACKSRC = 0x063B
MGMSG_PZ_REQ_NTFEEDBACKSRC = 0x063C
MGMSG_PZ_GET_NTFEEDBACKSRC = 0x063D
MGMSG_PZ_REQ_NTSTATUSBITS = 0x063E
MGMSG_PZ_GET_NTSTATUSBITS = 0x063F
MGMSG_PZ_REQ_NTSTATUSUPDATE = 0x0664
MGMSG_PZ_GET_NTSTATUSUPDATE = 0x0665
MGMSG_PZ_ACK_NTSTATUSUPDATE = 0x0666
MGMSG_NT_SET_EEPROMPARAMS = 0x07E7
MGMSG_NT_SET_TNA_DISPSETTINGS = 0x07E8
MGMSG_NT_REQ_TNA_DISPSETTINGS = 0x07E
MGMSG_NT_GET_TNA_DISPSETTINGS = 0x07EA
MGMSG_NT_SET_TNAIOSETTINGS = 0x07EB
MGMSG_NT_REQ_TNAIOSETTINGS = 0x07EC
MGMSG_NT_GET_TNAIOSETTINGS = 0x07ED
# Message codes for all the laser related messages
MGMSG_LA_SET_PARAMS = 0x0800
MGMSG_LA_REQ_PARAMS = 0x0801
MGMSG_LA_GET_PARAMS = 0x0802
MGMSG_LA_ENABLEOUTPUT = 0x0811
MGMSG_LA_DISABLEOUTPUT = 0x0812
MGMSG_LA_REQ_STATUSUPDATE = 0x0820
MGMSG_LA_GET_STATUSUPDATE = 0x0821
MGMSG_LA_ACK_STATUSUPDATE = 0x0822
# Message codes for all the Quad control related messages
MGMSG_QUAD_SET_PARAMS = 0x0870
MGMSG_QUAD_REQ_PARAMS = 0x0871
MGMSG_QUAD_GET_PARAMS = 0x0872
MGMSG_QUAD_REQ_STATUSUPDATE = 0x0880
MGMSG_QUAD_GET_STATUSUPDATE = 0x0881
MGMSG_QUAD_SET_EEPROMPARAMS = 0x0875

""" ----------------Generic system constants ---------------------------"""
# Timeouts in ms
READ_TIMEOUT=500  
WRITE_TIMEOUT=5000  
QUERY_TIMEOUT=60000
INIT_QUERY_TIMEOUT=5000
PURGE_DELAY=50      
# Device IDs
HOST_CONTROLLER_ID = 0x01
RACK_CONTROLLER_ID = 0x11
BAY_0_ID = 0x21
BAY_1_ID = 0x22
BAY_2_ID = 0x23
BAY_3_ID = 0x24
BAY_4_ID = 0x25
BAY_5_ID = 0x26
BAY_6_ID = 0x27
BAY_7_ID = 0x28
BAY_8_ID = 0x29
BAY_9_ID = 0x2A
GENERIC_USB_ID = 0x50
# Other constants relating to bays
BAY_OCCUPIED=0x01
BAY_EMPTY=0x02
ALL_BAYS=[BAY_0_ID,BAY_1_ID,BAY_2_ID,BAY_3_ID,BAY_4_ID,BAY_5_ID,BAY_6_ID,BAY_7_ID,BAY_8_ID,BAY_9_ID]
BAY_TYPE_SERIAL_PREFIXES=["70","71","73","94"]      # The first two digits of the serial numbers of the controllers which use the bay type architecture
# Channel IDs
CHANNEL_1=0x01
CHANNEL_2=0x02
ALL_CHANNELS=[CHANNEL_1,CHANNEL_2]
# Other constants relating to channels
CHAN_ENABLE_STATE_ENABLED=0x01
CHAN_ENABLE_STATE_DISABLED=0x02

""" ------------ Constants and methods for motor controllers ------------------"""
def getMotorScalingFactors(controllerType,stageType):
    """ Get the conversion factor between encoder units and real (position/velocity/acceleration) units (e.g. mm,mm/s,mm/s/s for linear drive, 
    deg, deg/s, deg/s/s for angular) given the controller type and stage type as strings.  This data comes from section 8 of the introduction (p. 14 onwards) 
    from the 'Thorlabs APT Controllers Host-Controller Communications Protocol Issue 9'    
    """
    # convert the controller/motor strings to uppercase for versatility
    controller=controllerType.upper()
    stage=stageType.upper()
    # De-inflect into family names from specific models
    if controller[0:-1] in ["BBD10","BBD20","BSC00","BSC10","BSC20"]: controller=controller[0:-1]+"X"
    if stage[0:2] in ["Z8","Z6"]: stage=stage[0:2]+"XX"
    # define a dictionary for encCnt based
    if controller=="TDC001":
        T=2048/6e6
        encCnt={"MTS25-Z8":34304,"MTS50-Z8":34304,"PRM1-Z8":1919.64,"Z8XX":34304,"Z6XX":24600}
        return {"position":encCnt[stage],"velocity":encCnt[stage]*T*65536,"acceleration":encCnt[stage]*T**2*65536}
    elif controller in ["TBD001","BBD10X","BBD20X"]:
        T=102.4e-6
        encCnt={"DDSM100":2000,"MLS203":20000}
        return {"position":encCnt[stage],"velocity":encCnt[stage]*T*65536,"acceleration":encCnt[stage]*T**2*65536}
    elif controller in ["TST001","BSC00X","BSC10X","MST601"]:
        encCnt={"DRV001":51200,"DRV013":25600,"DRV014":25600,"DRV113":20480,"DRV114":20480,"FW103":71/0.998,"NR360":4693/0.999}
        return {"position":encCnt[stage],"velocity":encCnt[stage],"acceleration":encCnt[stage]}
    elif controller in ["BSC20X","MST602"]:
        encCnt={"DRV001":819200,"DRV013":409600,"DRV014":409600,"DRV113":327680,"DRV114":327680,"FW103":1138/1.0002,"NR360":75091/0.99997}
        return {"position":encCnt[stage],"velocity":encCnt[stage]*53.68,"acceleration":encCnt[stage]/90.9}
    else:
       raise NameError("Controller type: " + controller + " not found")

# Constants for the motor
MOTOR_JOG_FORWARD=0x01
MOTOR_JOG_REVERSE=0x02

#DEFAULT_STAGE_TYPE="DRV001"
DEFAULT_STAGE_TYPE="TDC001"

""" ---- Hardware specific constants.  These should be added by developers as needed when developing classes for specific apt hardware devices -----"""

# Constsants for piezo controller
PIEZO_OPEN_LOOP_MODE = 0x01
PIEZO_CLOSED_LOOP_MODE = 0x02
### All of the constants should probably be added and defaults assigned in aptlib instead of just putting the default values here
PIEZO_INPUT_VOLTS_SRC_SW = 0x01
PIEZO_PID_PROP_CONST=0x64
PIEZO_PID_INT_CONST=0x64
PIEZO_AMP_CURRENT_LIM=0x02
PIEZO_AMP_LP_FILTER=0x03
PIEZO_AMP_FEEDBACK_SIGNAL=0xFFFF
PIEZO_AMP_BNCMODE_LVOUT=0xFFFF
PIEZO_MAX_VOLT_REPR=0x7FFF          # Number representing 100% voltage
PIEZO_MAX_POS_REPR=0x7FFF           # Number representing 100% extension (apparently depending on unit it may be 0x7FFF or 0xFFF)
PIEZO_VOLTAGE_STEP = 0.1            # 0.1V resolution in specifying voltage
PIEZO_TRAVEL_STEP = 0.1             # 0.1 um resolution in specifying position   
PIEZO_POSITION_ACCURACY = .02       # 20nm positional accuracy for closed loop piezo controller
PIEZO_MOVE_TIMEOUT=1.0              # Timeout in seconds specified for position to reach target level
PIEZO_ZERO_TIMEOUT=20.0             # Timeout in seconds specified for zero to finish
