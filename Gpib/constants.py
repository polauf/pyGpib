# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 14:49:46 2016

@author: polauf
"""
from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
   # linux
   GPIB_LIBRARIES=('libgpib.so',)
   from ctypes import cdll as _dll
elif _platform == "darwin":
    raise NotImplemented('Not implemented for MACOS')
elif _platform == "win32":
   from ctypes import windll as _dll
   GPIB_LIBRARIES=('gpib-32','gpib488')
   
   
   
from ctypes import c_int,c_short,c_uint,c_char,c_size_t,c_long,byref,POINTER
from enum import IntEnum

NLend=2
DABend=1
NULLend=0
STOPend = 0x0100
NOADDR=c_short(0xFFFF)
NOSAD=0
ALLSAD=-1


_lib=None
_libName=''


#load library object
for l in GPIB_LIBRARIES:
    try:
        _lib=_dll.LoadLibrary(l)
        _libName=l
    except:
        pass
if _lib is None:
    raise RuntimeError('GPIB Library not found.')

if _libName!='gpib488':
    _size_t=c_long
else:
    _size_t= c_size_t



class Ib(IntEnum):
    PAD            = 0x0001  # Primary Address
    SAD            = 0x0002  # Secondary Address
    TMO            = 0x0003  # Timeout Value
    EOT            = 0x0004  # Send EOI with last data byte?
    PPC            = 0x0005  # Parallel Poll Configure
    READDR         = 0x0006  # Repeat Addressing
    AUTOPOLL       = 0x0007  # Disable Auto Serial Polling
    CICPROT        = 0x0007  # CIC protocol
    SC             = 0x000A  # Board is System Controller?
    SRE            = 0x000B  # Assert SRE on device calls?
    EOSrd          = 0x000C  # Terminate reads on EOS
    EOSwrt         = 0x000D  # Send EOI with EOS character
    EOScmp         = 0x000E  # Use 7 or 8-bit EOS compare
    EOSchar        = 0x000F  # The EOS character
    PP2            = 0x0010  # Use Parallel Poll Mode 2
    TIMING         = 0x0011  # NORMAL, HIGH, or VERY_HIGH timing
    DMA            = 0x0012  # Use DMA for I/O
    SendLLO        = 0x0017  # Enable/disable the sending of LLO
    SPollTime      = 0x0018  # Set the timeout value for serial polls
    PPollTime      = 0x0019  # Set the parallel poll length period
    EndBitIsNormal = 0x001A  # Remove EOS from END bit of IBSTA
    UnAddr         = 0x001B  # Enable/disable device unaddressing
    HSCableLength  = 0x001F  # Length of cable specified for high speed timing
    Ist            = 0x0020  # Set the IST bit
    Rsv            = 0x0021  # Set the RSV byte
    LON            = 0x0022  # Enter listen only mode
    EOS            = 0x0025  # Macro for ibeos
    Serial         = 0x0023  # only to read Serial number

class TMO(IntEnum):
    TNONE=0
    T10us=1
    T30us=2
    T100us=3
    T300us=4
    T1ms=5
    T3ms=6
    T10ms=7
    T30ms=8
    T100ms=9
    T300ms=10
    T1s=11
    T3s=12
    T10s=13
    T30s=14
    T100s=15
    T300s=16
    T1000s=17

DCAS,DTAS,LACS,TACS,ATN,CIC,REM,LOK,CMPL,RQS,SRQI,END,TIMO,ERR = \
0,1,2,3,4,5,6,7,8,11,12,13,14,15

GPIB_STATUS=(
    (DCAS,'DCAS','Device Clear State'),
    (DTAS,'DTAS','Device Trigger Status'),
    (LACS,'LACS','Listener'),
    (TACS,'TACS','Talker'),
    (ATN,'ATN','Attention'),
    (CIC,'CIC','Controller-In-Charge'),
    (REM,'REM','Remote State'),
    (LOK,'LOK','Lockout State'),
    (CMPL,'CMPL','I/O Completed'),
    (RQS,'RQS','Device Requesting Service'),
    (SRQI,'SRQI','SRQ Interrupt Received'),
    (END,'END','END or EOS Detected'),
    (TIMO,'TIMO','Timeout Error'),
    (ERR,'ERR','GPIB Error'),
)
EDVR,ECIC,ENOL,EADR,EARG,ESAC,EABO,ENEB,EDMA,EOIP,ECAP,EFSO,EBUS,ESTB,ESRQ, \
ETAB,ELCK,EARM,EHDL,WCFG,EWIP,ERST,EPWR = \
0,1,2,3,4,5,6,7,8,10,11,12,14,15,16,20,21,22,23,24,26,27,28

GPIB_ERRORS=(
    (EDVR,'EDVR','Driver Error'),
    (ECIC,'ECIC','Specified GPIB interface board is not CIC'),
    (ENOL,'ENOL','No listening device(s)'),
    (EADR,'EADR','GPIB interface board not addressed'),
    (EARG,'EARG','Invalid argument'),
    (ESAC,'ESAC','Board is not the system controller'),
    (EABO,'EABO','I/O operation aborted'),
    (ENEB,'ENEB','Non-existent GPIB board'),
    (EDMA,'EDMA','DMA Error'),
    (EOIP,'EOIP','Function not allowed while I/O is in progress'),
    (ECAP,'ECAP','No capability for operation'),
    (EFSO,'EFSO','File system error'),
    (EBUS,'EBUS','Command byte transfer error'),
    (ESTB,'ESTB','Serial poll status byte(s) lost'),
    (ESRQ,'ESRQ','SRQ in “ON” position'),
    (ETAB,'ETAB','Table problem'),
    (ELCK,'ELCK','GPIB Interface is locked and cannot be accessed'),
    (EARM,'EARM','Ibnotify event failed to rearm'),
    (EHDL,'EHDL','Invalid handle'),
    (WCFG,'WCFG','Configuration warning'),
    (EWIP,'EWIP','Wait in progress on specified handle'),
    (ERST,'ERST','Event notification was canceled due to reset on the interface'),
    (EPWR,'EPWR','Interface lost power'),
)

ibsta=_lib.ThreadIbsta
iberr=_lib.ThreadIberr
ibcntl=_lib.ThreadIbcnt

def Status(status=None,short=False):
    """Parse Ibsta:
    status: (optional) Ibsta integer. If its not None call ibsta itself
    short : Bool add description of states.
    return tuple of states.
    """
    if status is None:
        status=ibsta()
    return tuple(map(lambda x: x[1] if short else '%s : %s'%x[1:],filter(lambda x: (status&(1<<x[0])),GPIB_STATUS)))

def Error(error=None,short=False):
    """Parse IbErr:
    status: (optional) Iberr integer. If its not None call ibsta and after if there is error Iberr itself
    short : Bool add description of error.
    return errorstring.
    """    
    if error is None: 
        if not ibsta()&(1<<ERR):
            return
        else:
            error=iberr()
    err=next(filter(lambda i:i[0]==error,GPIB_ERRORS),(error,'EEE','Unknown Error'))
    return '%s'%err[1] if short else '%s : %s'%err[1:]