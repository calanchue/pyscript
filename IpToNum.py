'''
Created on 2013. 4. 9.

@author: Hwang-JinHwan



'''

def twos_comp32(val):
    bits=32
    """compute the 2's compliment of int value val"""
    if( (val&(1<<(bits-1))) != 0 ):
        val = val - (1<<bits)
    return val        

def ip2num(ipString):
    if ipString is None:
        raise Exception("Invalid IP")
    try:
        octets = [octet.strip() for octet in ipString.split('.')]
    except Exception,e:
        raise e

    num = (int(octets[0])<<24) + (int(octets[1])<<16) + (int(octets[2])<<8) + int(octets[3])
    return num

def ip2int(ipString):
    return twos_comp32(ip2num(ipString))

if __name__ == '__main__':
    while True:
        value = raw_input("input ip. ex)192.169.244.5 # ")
        try :
            print ip2int(value)
        except ValueError : 
            print "invalid input = %s" % value
    
    pass