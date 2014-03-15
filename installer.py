from Tkinter import *
from ScrolledText import ScrolledText
import tkMessageBox as mb
import sys

#In order to retrieve the version, we need to add ka-lite to the path, so we can import kalite.
sys.path.insert(0, './ka-lite')
from kalite import version

#The current version of KA Lite.
VERSION = version.VERSION

#KA Lite license.
LICENSE = open("ka-lite/LICENSE").read()

class WelcomeFrame(Frame):
    """Show the welcome frame where the user can start installing KA Lite or quit.

    Attributes:
        parent: A pointer to the parent frame.
        fle_logo_photo: A pointer to FLE logo image.
        kalite_logo_photo A pointer to KA Lite logo image.
        top_frame: The top frame where FLE logo is placed.
        bottom_frame: Bottom frame.
        bottom_left_frame: This frame is where the KA Lite logo and the version are displayed.
        bottom_right_frame: This frame is where install button and quit button are placed.
        fle_label: A label that shows the image poited by fle_logo_photo.
        kalite_label: A label that shows the image pointed by kalite_logo_photo. 
        install_button: A button to start the installion and proceed to the welcome window.
        quit_button: A button to quit the installer.
        version_label: A label that shows the version of KA Lite.
    """

    def __init__(self, parent):
        Frame.__init__(self, parent)
        """Inits the frame."""

        self.parent = parent
        self.parent.title("FLE - KA Lite Setup - Welcome")
        self.loadImages()
        self.configureLayout()
        self.drawLayout()

    def loadImages(self):
        """Loads the images. The size must be the exact size of the image."""

        self.fle_logo_photo = PhotoImage(file="images/flelogo_resized.gif", width=455, height=150)
        self.kalite_logo_photo = PhotoImage(file="images/kalitelogo_resized.gif", width=255, height=65)

    def configureLayout(self):
        """Configures the frame and the components that belong to this frame."""

        self.pack(fill=BOTH, expand=True)
        self.top_frame = Frame(self)
        self.bottom_frame = Frame(self)
        self.bottom_left_frame = Frame(self.bottom_frame)
        self.bottom_right_frame = Frame(self.bottom_frame)

        self.fle_label = Label(self.top_frame, image=self.fle_logo_photo, width=452, height=150)
        self.fle_label.image = self.fle_logo_photo

        self.kalite_label = Label(self.bottom_left_frame, image=self.kalite_logo_photo, width=250, height=80)
        self.kalite_label.image = self.kalite_logo_photo

        self.install_button = Button(self.bottom_right_frame, text="Install", command=self.showLicenseFrame, width=24, height=5)

        self.quit_button = Button(self.bottom_right_frame, text="Quit", command=self.confirmQuit, width=24, height=5)

        self.version_label = Label(self.bottom_left_frame, text="KA Lite version: " + str(VERSION), width=30, height=5)

    def drawLayout(self):
        """Draws the frame with all the components that were previously configured."""

        self.top_frame.pack(fill=BOTH, expand=True)
        self.bottom_frame.pack(fill=BOTH, expand=True)
        self.bottom_left_frame.pack(fill=BOTH, expand=True, side=LEFT)
        self.bottom_right_frame.pack(fill=BOTH, expand=True, side=RIGHT)
        self.fle_label.pack(expand=True, fill=X)
        self.kalite_label.pack(expand=True, fill=X)
        self.install_button.pack(side=TOP, fill=X)
        self.quit_button.pack(side=BOTTOM, fill=X)
        self.version_label.pack(expand=True, fill=X)

    def showLicenseFrame(self):
        """Changes the frame to the license frame."""
        self.pack_forget()
        self.destroy()
        LicenseFrame(self.parent)

    def showServerConfigurationFrame(self):
        """Changes the frame to the server configuration frame."""
        self.pack_forget()
        self.destroy()
        ServerConfigurationFrame(self.parent)

    def confirmQuit(self):
        if mb.askyesno("Quit the installer.", "Are you sure you want to quit?"):
            self.quit()


class LicenseFrame(Frame):
    """Shows the license agreement and asks the user to accept it in order to proceed.

    Attributes:
        parent: A pointer to the parent frame.
        license_area: The text area that will hold the license.
        accept_var: This variable contains the integer code that corresponds to the state of the accept_button.
        accept_button: The Checkbutton used to accept the license terms.
        next_button: Button to proceed in the installion to the next frame.
        back_button: Button to return to the WelcomeFrame.
    """

    def __init__(self, parent):
        Frame.__init__(self, parent)
        """Inits the frame."""

        self.parent = parent
        self.parent.title("FLE - KA Lite Setup - License")
        self.configureLayout()
        self.drawLayout()

    def configureLayout(self):
        """Configures the frame and the components that belong to this frame."""
        
        self.pack(fill=BOTH, expand=True)

        self.license_area = ScrolledText(self, width=4, height=4, wrap=WORD)
        self.license_area.insert(INSERT, LICENSE)
        self.license_area.config(state=DISABLED)
        self.license_area.focus()

        self.accept_var = IntVar()
        self.accept_button = Checkbutton(self, text="I accept the license terms.", variable=self.accept_var, command=self.onCheck)

        self.next_button = Button(self, text="Next", width=15, height=2, state=DISABLED)
        self.back_button = Button(self, text="Back", width=15, height=2, command=self.showWelcomeFrame)

    def drawLayout(self):
        """Draws the frame with all the components that were previously configured."""

        self.pack(fill=BOTH, expand=True)
        self.license_area.pack(expand=True, fill=BOTH)
        self.accept_button.pack(side=LEFT)
        self.next_button.pack(side=RIGHT, padx=5, pady=5)
        self.back_button.pack(side=RIGHT)

    def onCheck(self):
        """Enables and disables the button to continue."""

        if self.accept_var.get() == 1:
            self.next_button.config(state=NORMAL)
        else:
            self.next_button.config(state=DISABLED)

    def showWelcomeFrame(self):
        """Changes the frame to the welcome frame."""

        self.pack_forget()
        self.destroy()
        WelcomeFrame(self.parent)


class ServerConfigurationFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        """Inits the frame"""

        self.parent = parent
        self.parent.title("FLE - KA Lite Setup - Server configuration")


def createRootWindow(width, height):
    """Creates an instance of Tk which is the main window of the application and configure it.

    Creates the main window of the installer. This window is also used to
    add or remove any other component.

    Args:
        width: An integer that corresponds to the width.
        height: An integer value that corresponds to the height.

    Returns:
        A reference to the main window.
    """

    root_window = Tk()
    root_window.resizable(0,0)
    root_window.protocol('WM_DELETE_WINDOW', ignoreXButton)

    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()

    x_position = (screen_width - width)/2
    y_position = (screen_height - height)/2

    root_window.geometry('%dx%d+%d+%d' % (width, height, x_position, y_position))

    return root_window

def ignoreXButton():
    """For full control over the user options, we are ignoring the closing button that would terminate the installer in any point."""
    pass

def main():
    
    root_window = createRootWindow(445, 350)
    
    WelcomeFrame(root_window)

    root_window.mainloop()


if __name__ == '__main__':
    main()