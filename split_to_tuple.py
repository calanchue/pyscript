'''
Created on 2013. 5. 2.

@author: Hwang-JinHwan


'''

from Tkinter import Tk

input_value = """
aaaa
bbbb
cccc
"""
def copy_to_clipboard(value):
    print "Value : " + value
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(value)
    print "The Value has been copied to the clipboard"
    r.destroy()
    
if __name__ == '__main__':
    result = ', '.join("'" + value + "'" for value in input_value.split())
    copy_to_clipboard(result)

        
        
        


