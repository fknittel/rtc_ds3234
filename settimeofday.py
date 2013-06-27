from ctypes import cdll, c_int, POINTER, c_void_p, Structure
import datetime

def _settimeofday(sec_since_epoc):
    libc = cdll['libc.so.6']
    libc.settimeofday.restype = c_int
    class timeval(Structure):
        _fields_ = [('tv_sec', c_int), ('tv_usec', c_int)]
    libc.settimeofday.argtypes = POINTER(timeval), c_void_p
    t = timeval()
    t.tv_sec = sec_since_epoc
    libc.settimeofday(t, None)

def settimeofday(dt_utc):
    sec_since_epoc = (dt_utc - datetime.datetime(1970, 1, 1)).total_seconds()
    _settimeofday(int(sec_since_epoc))
