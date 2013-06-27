from bcd import bcd2bin, bin2bcd
import datetime

DS3234_REG_SECONDS	= 0x00
DS3234_REG_MINUTES	= 0x01
DS3234_REG_HOURS	= 0x02
DS3234_REG_DAY		= 0x03
DS3234_REG_DATE		= 0x04
DS3234_REG_MONTH	= 0x05
DS3234_REG_YEAR		= 0x06

DS3234_24HRS = 0x40

class Ds3234SpiCommunicationError(Exception):
    pass

def _read_data(dev_fp, num_bytes=0):
    data = dev_fp.read(num_bytes + 1)
    if data[0] != '\xff':
        raise Ds3234SpiCommunicationError('SPI read failed with status ' + \
                repr(data[0]))
    return data[1:]

def get_time(dev_fp):
    dev_fp.write('\x00')
    dt_buf = [ord(dt_val) for dt_val in _read_data(dev_fp, 7)]
    tm_sec = bcd2bin(dt_buf[0])
    tm_min = bcd2bin(dt_buf[1])
    tm_hour = bcd2bin(dt_buf[2] & 0x3f)
    tm_mday = bcd2bin(dt_buf[4])
    tm_mon = bcd2bin(dt_buf[5] & 0x1f)
    tm_year = bcd2bin(dt_buf[6]) + 2000
    return datetime.datetime(tm_year, tm_mon, tm_mday, tm_hour, tm_min,
        tm_sec)

def _set_reg(dev_fp, addr, val):
    data = chr(addr | 0x80)
    data += chr(val)
    dev_fp.write(data)
    _read_data(dev_fp)

def set_time(dev_fp, dt):
    _set_reg(dev_fp, DS3234_REG_SECONDS, bin2bcd(dt.second))
    _set_reg(dev_fp, DS3234_REG_MINUTES, bin2bcd(dt.minute))
    _set_reg(dev_fp, DS3234_REG_HOURS, (bin2bcd(dt.hour) & 0x3f) | DS3234_24HRS)
    _set_reg(dev_fp, DS3234_REG_DAY, bin2bcd(dt.isoweekday()))
    _set_reg(dev_fp, DS3234_REG_DATE, bin2bcd(dt.day))
    _set_reg(dev_fp, DS3234_REG_MONTH, bin2bcd(dt.month) & 0x1f)
    _set_reg(dev_fp, DS3234_REG_YEAR, bin2bcd(dt.year - 2000))
