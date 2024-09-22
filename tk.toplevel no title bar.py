import tkinter as tk
from ctypes import windll, wintypes
# ctypes.windll represent loaded shared libraries. 
# functions in these libraries use the standard C calling convention, and are assumed to return int
# cite: https://docs.python.org/3.8/library/ctypes.html#ctypes.CDLL

# cite: https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowlongw#parameters
GWL_STYLE = -16

# cite: https://learn.microsoft.com/en-us/windows/win32/winmsg/window-styles
WS_SYSMENU = 0x00080000

# cite: https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowpos#parameters
SWP_FRAMECHANGED = 0x0020
SWP_NOACTIVATE = 0x0010
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001

#* write short names for functions and specify argument and return types
GetWindowLong = windll.user32.GetWindowLongW
# GetWindowLongW should be https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowlongw

GetWindowLong.restype = wintypes.ULONG
# wintypes.ULONG represents the C unsigned long datatype; search keyword: c_ulong

GetWindowLong.argtypes = (wintypes.HWND, wintypes.INT)
# wintypes.HWND represents the C void* type. The value is represented as integer; search keyword: c_void_p
# wintypes.INT represents the C signed int datatype; search keyword: c_uint
# cite: https://docs.python.org/3/library/ctypes.html

SetWindowLong = windll.user32.SetWindowLongW
# SetWindowLongW should be https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowlongw

SetWindowLong.restype = wintypes.ULONG
SetWindowLong.argtypes = (wintypes.HWND, wintypes.INT, wintypes.ULONG)

SetWindowPos = windll.user32.SetWindowPos
# SetWindowPos should be https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowpos

class App():
    """
    original: https://stackoverflow.com/a/45487021
    """
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("200x50")
        
        self.tplvl = tk.Toplevel(self.window, padx=20, pady=20)
        self.tplvl.withdraw()
        
        self.btn_show = tk.Button(self.window, text="show toplevel", command=lambda:self.tplvl.deiconify())
        self.btn_show.pack()
        
        self.btn_close = tk.Button(self.tplvl, text="hide toplevel", command=lambda:self.tplvl.withdraw())
        self.btn_close.pack()
        
        #! must have update first, then remove_win_title()
        self.window.update()
        
        self.remove_win_title(self.tplvl)
        
        self.window.mainloop()       

    def remove_win_title(self, widget:tk.Toplevel):
        hwnd = windll.user32.GetParent(widget.winfo_id())
        style = GetWindowLong(hwnd, GWL_STYLE) # get existing style
        style = style & ~WS_SYSMENU # bitwise and
        SetWindowLong(hwnd, GWL_STYLE, style)
        SetWindowPos(hwnd, 0, 0,0,0,0, SWP_FRAMECHANGED | SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE)

    def addback_win_title(self, widget:tk.Toplevel):
        hwnd = windll.user32.GetParent(widget.winfo_id())
        style = GetWindowLong(hwnd, GWL_STYLE) # get existing style
        style = style | WS_SYSMENU # bitwise or
        SetWindowLong(hwnd, GWL_STYLE, style)
        SetWindowPos(hwnd, 0, 0,0,0,0, SWP_FRAMECHANGED | SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE)

if __name__ == "__main__":
    App()
