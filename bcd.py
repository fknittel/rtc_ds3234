class BcdOutOfRange(Exception):
    pass

def bcd2bin(bcd_val):
    return (bcd_val & 0xf) + (((bcd_val & 0xf0) >> 4) * 10)

def bin2bcd(bin_val):
    if not (bin_val >= 0 and bin_val <= 99):
        raise BcdOutOfRange('binary value not between 0 and 99') 
    return (bin_val % 10) | ((bin_val / 10) << 4)
