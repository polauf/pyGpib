#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 11:36:04 2016

@author: polauf
"""
from ctypes import c_int,c_uint,c_short,c_char,c_size_t,c_long,POINTER
from ctypes import windll as _dll
from enum import IntEnum

NLend=2
DABend=1
NULLend=0

STOPend = 0x0100

NOADDR=c_short(0xFFFF)

NOSAD=0
ALLSAD=-1

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

GPIB_LIBRARIES=('gpib-32','gpib488','libgpib.so')
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


#needed from iee488.1
_lib.ibask.argtypes= (c_int,c_int,POINTER(c_uint))
def ibask(boarddev,option):
    ptr=c_uint(0)
    r=_lib.ibask(boarddev,option,ptr)
    return ptr.value,r

_lib.ibconfig.argtypes= (c_int,c_int,c_uint)
ibconfig=_lib.ibconfig
#end

class addr(int):
    """
    Address class
    Holds Pad and Sad as IEEE488.2 needs.
    """
    def __new__(cls,pad,sad=NOSAD):
        if 0<=pad<31:
            return  super(addr, cls).__new__(cls,((pad & 0xFF) | (sad << 8)) )
        else:
            raise ValueError('PAD must be 0-30.')
        
    @property
    def pad(self):
        return int.__int__(self) & 0xFF

    @property
    def sad(self):
        return (int.__int__(self) >> 4 ) & 0xFF
       
    
    def __repr__(self):
        return repr('<%d:%s>'%(self.pad,'%d'%self.sad if self.sad!=ALLSAD else 'ALL'))
        
    def __str__(self):
        return '%d:%s'%(self.pad,'%d'%self.sad if self.sad!=ALLSAD else 'ALL')
        
    def __add__(self,other):
        try:
            other=int(other)
        except:
            raise ValueError("Can't convert to int '%s'."%(other,))
        return addr(self.pad+other,self.sad)
        
    def __radd__(self,other):
        if isinstance(other,addr):
            return addr(other.pad+self.pad,other.sad)
        else:
            return self.__add__(other)
    
    def array(self):
         "Return carray of addresses terminated with NOADDR.(convinience for lib functions)"
        return (c_short*2)(int.__int__(self),NOADDR)
    
    def arrayInOut(self):
        "Return carrays of addresses terminated with NOADDR and free array of same length (convinience for lib functions).
        return (c_short*2)(int.__int__(self),NOADDR),(c_short*1)()
        
class addrs(list):
    """
    Holds list of addresses.
    """
    def __init__(self,values=None):
        self.values=[]
        if isinstance(values,(int,float)):
            self.values.append(addr(values))
        else:
            for i in values:
                if isinstance(i,(list,tuple)) and len(i)==2:
                    self.values.append(addr(*i))
                else:
                    self.values.append(addr(i))
                
    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __delitem__(self, key):
        del self.values[key]

    def __iter__(self):
        return iter(self.values)

    def __reversed__(self):
        return addrs(reversed(self.values))
                
    def __repr__(self):
        return repr('SCPI '+self.values.__repr__())
        
    
    def array(self):
        "Return carray of addresses terminated with NOADDR.(convinience for lib functions)"
        return (c_short*(len(self.values)+1))(*self.values,NOADDR)
        
    def arrayInOut(self):
        "Return carrays of addresses terminated with NOADDR and free array of same length (convinience for lib functions)."
        return (c_short*(len(self.values)+1))(*self.values,NOADDR),(c_short*(len(self.values)))()
    

_lib.AllSpoll.argtypes= (c_int,POINTER(c_short),POINTER(c_short))
_lib.AllSpoll.restype=c_short
def AllSpoll(board,address):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
    i,o=address.arrayInOut()
    r=_lib.AllSpoll(board,i,o)
    return tuple(o),r

_lib.DevClearList.argtypes= (c_int,POINTER(c_short))
_lib.DevClearList.restype=c_short
def DevClear(board,address):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
    return _lib.DevClearList(board,address.array())
        
_lib.EnableLocal.argtypes= (c_int,POINTER(c_short))
_lib.EnableLocal.restype=c_short
def EnableLocal(board,address):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
    return _lib.EnableLocal(board,address.array())

_lib.EnableRemote.argtypes= (c_int,POINTER(c_short))
_lib.EnableRemote.restype=c_short
def EnableRemote(board,address):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
    return _lib.EnableRemote(board,address.array())
        
_lib.FindLstn.argtypes= (c_int,POINTER(c_short),POINTER(c_short),c_int)
_lib.FindLstn.restype=c_short
def FindLstn(board,address):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
    i,o=address.arrayInOut()
    r=_lib.FindLstn(board,i,o,len(o))
    return tuple(o),r
      
_lib.FindRQS.argtypes= (c_int,POINTER(c_short),c_short)
_lib.FindRQS.restype=c_short
def FindRQS(board,address):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
    ptr=c_short(0)
    r=_lib.FindRQS(board,address.array(),ptr)
    return ptr.value,r

_lib.PassControl.argtypes= (c_int,c_short)   
_lib.PassControl.restype=c_short
PassControl=_lib.PassControl
 
_lib.PPoll.argtypes= (c_int,POINTER(c_short))   
_lib.PPoll.restype=c_short
def PPoll(board):
    ptr=c_short(0)
    r=_lib.PPoll(board,ptr)
    return ptr.value,r

_lib.PPollConfig.argtypes= (c_int,c_short,c_int,c_int) 
_lib.PPollConfig.restype=c_short
PPollConfig=_lib.PPollConfig

_lib.PPollUnconfig.argtypes= (c_int,POINTER(c_short))
_lib.PPollUnconfig.restype=c_short
def PPollUnconfig(board,address):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
    return _lib.PPollUnconfig(board,address.array())
    
_lib.RcvRespMsg.argtypes= (c_int,POINTER(c_char),_size_t,c_int)
_lib.RcvRespMsg.restype=c_short
def RcvRespMsg(board,length=1,termination=NULLend):
    arr=(c_char*length)()
    r=_lib.RcvRespMsg(board,arr,length,termination)
    return arr.value,r
    
_lib.ReadStatusByte.argtypes= (c_int,c_short,c_short)
_lib.ReadStatusByte.restype=c_short
ReadStatusByte=_lib.ReadStatusByte

_lib.Receive.argtypes= (c_int,c_short,POINTER(c_char),_size_t,c_int)
_lib.Receive.restype=c_short
def Receive(board,address,length=1,termination=NULLend):
    if not isinstance(address,(addrs,addr)):
        address=addr(address)
    arr=(c_char*length)()
    r=_lib.Receive(board,address,arr,length,termination)
    return arr.value,r
    
_lib.ReceiveSetup.argtypes= (c_int,c_short)
_lib.ReceiveSetup.restype=c_short
ReceiveSetup=_lib.ReceiveSetup

_lib.ResetSys.argtypes= (c_int,POINTER(c_short))
_lib.ResetSys.restype=c_short
def ResetSys(board,address):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
    return _lib.ResetSys(board,address.array())

_lib.SendList.argtypes= (c_int,POINTER(c_short),POINTER(c_char),_size_t,c_int)
_lib.SendList.restype=c_short
def Send(board,address,message,termination=NULLend):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
    return _lib.SendList(board,address.array(),bytes(message,'ascii'),len(message),termination)
        
_lib.SendCmds.argtypes= (c_int,POINTER(c_char),_size_t)
_lib.SendDataBytes.argtypes= (c_int,POINTER(c_char),_size_t,c_int)

_lib.SendIFC.argtypes= (c_int,)
_lib.SendIFC.restype=c_short
SendIFC=_lib.SendIFC
_lib.SendLLO.argtypes= (c_int,)
_lib.SendLLO.restype=c_short
SendLLO=_lib.SendLLO
_lib.SendSetup.argtypes= (c_int,POINTER(c_short))

_lib.SetRWLS.argtypes= (c_int,POINTER(c_short))
_lib.SetRWLS.restype=c_short
def SetRWLS(board,address):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
        print(address,(c_short*(len(address.values)+1))(*address.values,NOADDR))
    return _lib.SetRWLS(board,address.array())

_lib.TestSRQ.argtypes= (c_int,POINTER(c_short))
_lib.TestSRQ.restype=c_short
def TestSRQ(board,address):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
    return _lib.TestSRQ(board,address.array())
    
_lib.TestSys.argtypes= (c_int,POINTER(c_short),POINTER(c_short))
_lib.TestSys.restype=c_short
def TestSys(board,address):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
    i,o=address.arrayInOut()
    r=_lib.TestSys(board,i,o)
    return tuple(o),r

_lib.TriggerList.argtypes= (c_int,POINTER(c_short))
_lib.TriggerList.restype=c_short
def Trigger(board,address):
    if not isinstance(address,(addrs,addr)):
        address=addrs(address)
    return _lib.TriggerList(board,address.array())
_lib.WaitSRQ.argtypes= (c_int,POINTER(c_short))
_lib.WaitSRQ.restype=c_short




class SCPIError(Exception):
    def __init__(self,errno=None,device=None):
        self.errno=errno
        self.device=device
            
    def __str__(self):
        if isinstance(self.errno,int):
            if self.device is not None:
                return Error(self.errno)+' Device: %s.'%(self.device,)
            else:
                return Error(self.errno)+' Device: Unknown.'
        else:
            return str(self.errno) 

        
class SCPI:
    
    _boards=0
    
    def __init__(self,address,board=0,end=NLend):
        self.address=addr(address)
        self.board=board
        self.end=end
        self.name='SCPI Device %d:%d'%(self.board,self.address)
        self._initBoard()
        self.identify()
        
    def initBoard(self):
        if not self._boards&(1<<self.board):
            ResetSys(self.board,self.board)
            self._boards^=(1<<self.board)
        
    def identify(self):
        pass
    
    def restart(self):
        SetRWLS(self.board,self.address)
        
    def _error(self,status):
        if status&(1<<ERR):
            raise SCPIError(status,self.name)
            
    def lock(self):
        self._error(EnableRemote(self.board,self.address))
        
    def unlock(self):
        self._error(EnableLocal(self.board,self.address))
        
    def write(self,message):
        self._error(Send(self.board,self.address,message,self.end))
        
    def readline(self,length=None,chunk=32,terminator='\n'):
        if length is None:
            t=None
            if terminator is not None:
                t=ord(terminator)
            b,s=Receive(self.board,self.address,chunk,self.end)
            if b and not (s & 1<<END):        
                while not (s & 1<<ERR) or not (s & 1<<TIMO):
                    a,s=Receive(self.board,self.address,chunk,self.end)
                    b+=a
                    if (s & 1<<END) or (t is not None and b[-1]==t):   
                        break
            self._error(s)
            return str(b,'ascii') 
        else:
            return self.read(length)
         
    def read(self,length=32):
        r=Receive(self.board,self.address,length,self.end)
        self._error(r[1])
        return str(r[0],'ascii')
        
    def queryline(self,message,length=None,chunk=32):
        self.write(message)
        return self.readline(chunk=chunk)

    def query(self,message,length=32):
        self.write(message)
        return self.read(length)
        
    def __getitem__(self,message):
        if isinstance(message,(list,tuple)):
            self.write(';'.join(message))
            if any(filter(lambda x: x.endswith('?'),message)):
                return self.readline()
        else:
            self.write(message)
            if message.endswith('?'):
                return self.readline()
