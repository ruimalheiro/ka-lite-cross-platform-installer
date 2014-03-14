from Tkinter import Tk, Frame, BOTH, Label, Button

USE_IMAGES = True

try:
	from PIL import Image, ImageTk
except ImportError:
	raise ImportError
	USE_IMAGES = False

import tkMessageBox
from ttk import Style
import sys

sys.path.insert(0, './ka-lite')

from kalite import version

current_version = version.VERSION


class Installer(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initGUI()	
 

    def initGUI(self):
      
        self.parent.title("FLE - KA Lite Setup - Welcome!")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()

        Style().configure("TButton", font='serif 10')

        if USE_IMAGES:
	        fle_logo = Image.open("images//flelogo.png")
	        fle_logo_resized = fle_logo.resize((455,150), Image.ANTIALIAS)
	        fle_logo_photo = ImageTk.PhotoImage(fle_logo_resized)

	        fle_label = Label(self, image=fle_logo_photo, width=452, height=150)
	        fle_label.image = fle_logo_photo
	        fle_label.place(x=-4, y=-4)

	        kalite_logo = Image.open("images/kalitelogo.bmp")
	        kalite_logo_resized = kalite_logo.resize((250,70), Image.ANTIALIAS)
	        kalite_logo_photo = ImageTk.PhotoImage(kalite_logo_resized)

	        kalite_label = Label(self, image=kalite_logo_photo, width=250, height=80)
	        kalite_label.image = kalite_logo_photo
	        kalite_label.place(x=0, y=160)

        install_button = Button(self, text="Install", command=self.startInstall, width=24, height=5)
        install_button.place(x=265, y=165)

        quit_button = Button(self, text="Quit", command=self.quit, width=24, height=5)
        quit_button.place(x=265, y=260)

        version_label = Label(self, text="KA Lite version: " + str(current_version), width=30, height=5)
        version_label.place(x=0, y=250)


    def centerWindow(self):

    	width = 450
    	height = 350

    	screen_width = self.parent.winfo_screenwidth()
    	screen_height = self.parent.winfo_screenheight()

    	x_position = (screen_width - width)/2
    	y_position = (screen_height - height)/2

    	self.parent.geometry('%dx%d+%d+%d' % (width, height, x_position, y_position))


    def startInstall(self):

        tkMessageBox.showinfo("Hello World!", "Installing KA Lite...")


def main():
  
    root_window = Tk()
    root_window.resizable(0,0)
    root_window.iconbitmap("images/logo48.ico")

    installer = Installer(root_window)

    root_window.mainloop() 


if __name__ == '__main__':
    main()