# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 14:49:46 2016

@author: polauf
"""

from .constnants import *

#gpib 488.1

_lib.ibask.argtypes= (c_int,c_int,POINTER(c_uint))

def ibask(boarddev,option):
    ptr=c_uint(0)
    r=_lib.ibask(boarddev,option,ptr)
    return ptr.value,r


_lib.ibcac.argtypes= (c_int,c_int)
ibcac=_lib.ibcac
_lib.ibclr.argtypes= (c_int,)
ibclr=_lib.ibclr
_lib.ibcmd.argtypes= (c_int,POINTER(c_char),_size_t)

def ibcmd(boarddev,message):
    return _lib.ibcmd(boarddev,bytes(message,'ascii'),len(message))

_lib.ibconfig.argtypes= (c_int,c_int,c_uint)
ibconfig=_lib.ibconfig
_lib.ibln.argtypes = (c_int, c_int,c_int,POINTER(c_short))

def ibln(board,pad,sad=0):
    ptr=c_short(0)
    r=_lib.ibln(board,pad,sad,ptr)
    return ptr.value,r

_lib.ibdev.argtypes= (c_int,c_int,c_uint,c_int,c_int,c_uint)
ibdev=_lib.ibdev
_lib.ibgts.argtypes= (c_int,c_int)
ibgts=_lib.ibgts
_lib.iblines.argtypes = (c_int,POINTER(c_short))

def iblines(board):
    ptr=c_short(0)
    r=_lib.iblines(board)
    return ptr.value,r
    
_lib.ibloc.argtypes= (c_int,)
ibloc=_lib.ibloc
_lib.ibonl.argtypes= (c_int,c_int)
ibonl=_lib.ibonl
_lib.ibrd.argtypes= (c_int,POINTER(c_char),_size_t)

def ibrd(boarddev,length=1):
    arr=(c_char*length)()
    r=_lib.ibrd(boarddev,arr,length)
    return arr.value,r


_lib.ibrsp.argtypes = (c_int,POINTER(c_short))

def ibrsp(boarddev):
    ptr=c_short(0)
    _lib.ibrsp(boarddev,ptr)
    return ptr.value

_lib.ibsic.argtypes= (c_int,)
ibsic=_lib.ibsic
_lib.ibtrg.argtypes= (c_int,)
ibtrg=_lib.ibtrg
_lib.ibwait.argtypes= (c_int,c_int)
ibwait=_lib.ibwait
_lib.ibwrt.argtypes= (c_int,POINTER(c_char),_size_t)

def ibwrt(boarddev,message):
    return _lib.ibwrt(boarddev,bytes(message,'ascii'),len(message))
    
#end gpib 488.1
