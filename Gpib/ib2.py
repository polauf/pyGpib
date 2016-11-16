# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 14:49:46 2016

@author: polauf
"""

from .constants import *

class addr(int):
    """
    Address class for IEEE488.2
    Holds Pad and Sad.
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
    Holds list of addresses Address class for IEEE488.2.
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