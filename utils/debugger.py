import inspect
import pdb
import traceback
from colorama import Fore as c

def dprint(title:str = "COMMENT", comment:str = "", color:str = "RESET"):
    '''
    Prints a simple comment to the console. Where:
        - title: The title of the comment
        - comment: The comment to be printed
        - color: The color of the title
    '''

    color = color.upper()

    if color == "RESET":
        color = c.RESET
    elif color == "RED":
        color = c.RED
    elif color == "GREEN":
        color = c.GREEN
    elif color == "YELLOW":
        color = c.YELLOW
    elif color == "BLUE":
        color = c.BLUE
    elif color == "MAGENTA":
        color = c.MAGENTA
    elif color == "CYAN":
        color = c.CYAN
    elif color == "WHITE":
        color = c.WHITE
    elif color == "BLACK":
        color = c.BLACK
    else:
        color = c.RESET

    print(f"[ {color}{title}{c.RESET} ] {comment}")

def info(comment:str = ""):
    '''
    Prints a debug message to the console. Where:
        - comment: The comment to be printed
    '''
    actual_file = inspect.currentframe().f_back.f_code.co_filename
    actual_line = inspect.currentframe().f_back.f_lineno
    print(f"\n[ {c.YELLOW}DEBUG{c.RESET} ] {comment}\n > {c.BLACK}File{c.RESET}: {actual_file}\n > {c.BLACK}Line{c.RESET}: {actual_line}\n")

def trace(comment:str = ""):
    '''
    Prints a trace message to the console. Where:
        - comment: The comment to be printed
    '''
    actual_file = inspect.currentframe().f_back.f_code.co_filename
    actual_line = inspect.currentframe().f_back.f_lineno
    print(f"\n[ {c.YELLOW}DEBUG{c.RESET} ] {comment}\n > {c.BLACK}File{c.RESET}: {actual_file}\n > {c.BLACK}Line{c.RESET}: {actual_line}\n")
    pdb.set_trace()

def set_break(comment:str = ""):
    '''
    Prints a trace message to the console. Where:
        - comment: The comment to be printed
    '''
    actual_file = inspect.currentframe().f_back.f_code.co_filename
    actual_line = inspect.currentframe().f_back.f_lineno
    print(f"\n[ {c.YELLOW}DEBUG{c.RESET} ] {comment}\n > {c.BLACK}File{c.RESET}: {actual_file}\n > {c.BLACK}Line{c.RESET}: {actual_line}\n")
    breakpoint()

def error(comment:str = ""):
    '''
    Prints an error message to the console. Where:
        - comment: The comment to be printed
    '''
    actual_file = inspect.currentframe().f_back.f_code.co_filename
    actual_line = inspect.currentframe().f_back.f_lineno
    print(f"\n[ {c.RED}ERROR{c.RESET} ] {comment}\n > {c.BLACK}File{c.RESET}: {actual_file}\n > {c.BLACK}Line{c.RESET}: {actual_line}\n")
    traceback.print_exc()

if __name__ == "__main__":
    set_break()