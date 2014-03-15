from Tkinter import Tk, Frame, BOTH, Label, Button, RIGHT, PhotoImage, X, Y
from ttk import Style
import tkMessageBox
import sys

#In order to retrieve the version, we need to add ka-lite to the path, so we can import kalite.
sys.path.insert(0, './ka-lite')
from kalite import version

#The current version of KA Lite.
current_version = version.VERSION


class LicenseWindow(Frame):
    """Shows the license agreement and asks the user to accept it in order to proceed.

    Attributes:
        parent: A pointer to the parent container.
    """

    def __init__(self, parent):
        Frame.__init__(self, parent)
        """Inits the frame."""

        self.parent = parent
        self.parent.title("FLE - KA Lite Setup - License")
        self.configureLayout()

    def configureLayout(self):
        """Configures the frame and the components that belong to this frame."""
        self.pack(fill=X, expand=1)



class WelcomeWindow(Frame):
    """Show the welcome window where the user can start installing KA Lite or quit.

    Attributes:
        parent: A pointer to the parent container.
        fle_logo_photo: A pointer to FLE logo image.
        kalite_logo_photo A pointer to KA Lite logo image.
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
        self.parent.title("FLE - KA Lite Setup - Welcome!")
        self.loadImages()
        self.configureLayout()
        self.drawLayout()

    def loadImages(self):
        """Loads the images. The size must be the exact size of the image."""

        self.fle_logo_photo = PhotoImage(file="images/flelogo_resized.gif", width=455, height=150)
        self.kalite_logo_photo = PhotoImage(file="images/kalitelogo_resized.gif", width=255, height=65)

    def configureLayout(self):
        """Configures the frame and the components that belong to this frame."""

        self.pack(fill=BOTH, expand=1)

        self.fle_label = Label(self, image=self.fle_logo_photo, width=452, height=150)
        self.fle_label.image = self.fle_logo_photo

        self.kalite_label = Label(self, image=self.kalite_logo_photo, width=250, height=80)
        self.kalite_label.image = self.kalite_logo_photo

        self.install_button = Button(self, text="Install", command=self.startInstall, width=24, height=5)

        self.quit_button = Button(self, text="Quit", command=self.quit, width=24, height=5)

        self.version_label = Label(self, text="KA Lite version: " + str(current_version), width=30, height=5)

    def drawLayout(self):
        """Draws the frame with all the components that were previously configured."""

        self.fle_label.place(x=-4, y=-4)
        self.kalite_label.place(x=0, y=160)
        self.install_button.place(x=265, y=165)
        self.quit_button.place(x=265, y=260)
        self.version_label.place(x=0, y=250)
        self.pack()

    def startInstall(self):
        """Changes the frame to the license frame."""
        self.pack_forget()
        LicenseWindow(self.parent)


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

    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()

    x_position = (screen_width - width)/2
    y_position = (screen_height - height)/2

    root_window.geometry('%dx%d+%d+%d' % (width, height, x_position, y_position))

    return root_window


def main():
    
    root_window = createRootWindow(445, 350)
    
    WelcomeWindow(root_window)

    root_window.mainloop()


if __name__ == '__main__':
    main()