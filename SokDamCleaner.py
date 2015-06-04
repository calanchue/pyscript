'''
Created on 2015. 6. 4.

@author: Jinhwan
'''
import sys
import re

if __name__ == '__main__':
    w = open("processedSokDam.txt", "w")
    
    with open("sokdam.txt", "r") as input:
        for line in input:
            line = re.sub(r'\([^)]*\)', '', line)
            line = re.sub(r'\[[^)]*\]', '', line)
            sys.stdout.write(line)
            w.write(line)
        
    w.close()