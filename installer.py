from Tkinter import *
from ScrolledText import ScrolledText
import tkMessageBox as mb
import tkFileDialog as fd
from ttk import Progressbar
import sys, os, platform, shutil

#In order to retrieve the version, we need to add ka-lite to the path, so we can import kalite.
sys.path.insert(0, './ka-lite')
from kalite import version

#The current version of KA Lite.
VERSION = version.VERSION

#KA Lite license.
LICENSE = open("ka-lite/LICENSE").read()

#Default installation target path
TARGET_PATH = os.path.dirname(os.path.abspath(__file__))

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

        self.top_frame = Frame(self)
        self.bottom_frame = Frame(self)
        self.bottom_left_frame = Frame(self.bottom_frame)
        self.bottom_right_frame = Frame(self.bottom_frame)

        self.fle_label = Label(self.top_frame, image=self.fle_logo_photo, width=452, height=150)
        self.fle_label.image = self.fle_logo_photo

        self.kalite_label = Label(self.bottom_left_frame, image=self.kalite_logo_photo, width=250, height=80)
        self.kalite_label.image = self.kalite_logo_photo

        self.install_button = Button(self.bottom_right_frame, text="Install", command=self.showLicenseFrame, width=24, height=5)

        self.quit_button = Button(self.bottom_right_frame, text="Quit", command=quitInstaller, width=24, height=5)

        self.version_label = Label(self.bottom_left_frame, text="KA Lite version: " + str(VERSION), width=30, height=5)

    def drawLayout(self):
        """Draws the frame with all the components that were previously configured."""

        self.pack(fill=BOTH, expand=True)
        self.top_frame.pack(fill=BOTH, expand=True)
        self.bottom_frame.pack(fill=BOTH, expand=True)
        self.bottom_left_frame.pack(fill=BOTH, expand=True, side=LEFT)
        self.bottom_right_frame.pack(fill=BOTH, expand=True, side=RIGHT)
        self.fle_label.pack(fill=X, expand=True)
        self.kalite_label.pack(fill=X, expand=True)
        self.install_button.pack(fill=X, side=TOP)
        self.quit_button.pack(fill=X, side=BOTTOM)
        self.version_label.pack(fill=X, expand=True)

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
        self.loadImages()
        self.configureLayout()
        self.drawLayout()

    def loadImages(self):
        """Loads the images. The size must be the exact size of the image."""

        self.kaliteleaf_photo = PhotoImage(file="images/kaliteleaf.gif", width=16, height=16)

    def configureLayout(self):
        """Configures the frame and the components that belong to this frame."""

        self.top_frame = Frame(self, relief=RAISED, borderwidth=1)

        self.tip_label = Label(self.top_frame, text="Please read the license carefully.")
        self.kaliteleaf_label = Label(self.top_frame, image=self.kaliteleaf_photo, width=16, height=16)
        self.kaliteleaf_label.image = self.kaliteleaf_photo
        
        self.license_area = ScrolledText(self, width=4, height=4, wrap=WORD)
        self.license_area.insert(INSERT, LICENSE)
        self.license_area.config(state=DISABLED)
        self.license_area.focus()

        self.accept_var = IntVar()
        self.accept_button = Checkbutton(self, text="I accept the license terms.", variable=self.accept_var, command=self.onCheck)

        self.next_button = Button(self, text="Next", width=15, height=2, command=self.showServerConfigurationFrame, state=DISABLED)
        self.back_button = Button(self, text="Back", width=15, height=2, command=self.showWelcomeFrame)

    def drawLayout(self):
        """Draws the frame with all the components that were previously configured."""

        self.top_frame.pack(fill=X)
        self.tip_label.pack(fill=X, side=LEFT, padx=5, pady=5)
        self.kaliteleaf_label.pack(fill=X, side=RIGHT, padx=5, pady=5)
        self.pack(fill=BOTH, expand=True)
        self.license_area.pack(fill=BOTH, expand=True)
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

    def showServerConfigurationFrame(self):
        """Changes to the server configuration frame."""

        self.pack_forget()
        self.destroy()
        ServerConfigurationFrame(self.parent)


class ServerConfigurationFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        """Inits the frame"""

        self.parent = parent
        self.parent.title("FLE - KA Lite Setup - Server configuration")
        self.loadImages()
        self.configureLayout()
        self.drawLayout()

    def loadImages(self):
        """Loads the images. The size must be the exact size of the image."""

        self.kaliteleaf_photo = PhotoImage(file="images/kaliteleaf.gif", width=16, height=16)

    def configureLayout(self):

        self.top_frame = Frame(self, relief=RAISED, borderwidth=1)

        self.tip_label = Label(self.top_frame, text="Gathering data to configure KA Lite server.")
        self.kaliteleaf_label = Label(self.top_frame, image=self.kaliteleaf_photo, width=16, height=16)
        self.kaliteleaf_label.image = self.kaliteleaf_photo

        self.server_frame = Frame(self)
        self.server_name_label = Label(self.server_frame, text="Server name:")
        self.server_name_entry = Entry(self.server_frame, width=42)
        self.server_name_entry.focus()

        self.description_frame = Frame(self)
        self.description_label = Label(self.description_frame, text="Description:")
        self.description_entry = Entry(self.description_frame, width=42)

        self.run_at_startup_frame = Frame(self)
        self.run_at_startup_var = IntVar()
        self.run_at_startup_button = Checkbutton(self.run_at_startup_frame, text="Run KA Lite when the system starts.", variable=self.run_at_startup_var, command=self.onCheckSystemStartUp)

        self.run_at_user_log_frame = Frame(self)
        self.run_at_user_log_var = IntVar()
        self.run_at_user_log_button = Checkbutton(self.run_at_user_log_frame, text="Run KA Lite when the user logs in.", variable=self.run_at_user_log_var, command=self.onCheckUserLogs)

        self.auto_start_frame = Frame(self)
        self.auto_start_var = IntVar()
        self.auto_start_buttom = Checkbutton(self.auto_start_frame, text="Auto start the server.", variable=self.auto_start_var, command=self.onCheckAutoStart, state=DISABLED)

        self.bottom_space_frame = Frame(self)

        self.next_button = Button(self, text="Next", width=15, height=2, command=self.showSelectPathFrame)
        self.back_button = Button(self, text="Back", width=15, height=2, command=self.showLicenseFrame)

    def drawLayout(self):
        self.pack(fill=BOTH, expand=True)
        self.top_frame.pack(fill=X)
        self.tip_label.pack(fill=X, side=LEFT, padx=5, pady=5)
        self.kaliteleaf_label.pack(fill=X, side=RIGHT, padx=5, pady=5)

        self.server_frame.pack(fill=X, pady=10)
        self.server_name_label.pack(side=LEFT, padx=10)
        self.server_name_entry.pack(side=RIGHT, padx=10)

        self.description_frame.pack(fill=X)
        self.description_label.pack(side=LEFT, padx=10)
        self.description_entry.pack(side=RIGHT, padx=10)

        self.run_at_startup_frame.pack(fill=X)
        self.run_at_startup_button.pack(side=LEFT, padx=10, pady=(10,0))

        self.run_at_user_log_frame.pack(fill=X)
        self.run_at_user_log_button.pack(side=LEFT, padx=10)

        self.auto_start_frame.pack(fill=X)
        self.auto_start_buttom.pack(side=LEFT, padx=10)

        self.bottom_space_frame.pack(fill=BOTH, expand=True)
        self.next_button.pack(side=RIGHT, padx=5, pady=5)
        self.back_button.pack(side=RIGHT)
        
    def showLicenseFrame(self):
        self.pack_forget()
        self.destroy()
        LicenseFrame(self.parent)

    def showSelectPathFrame(self):
        self.pack_forget()
        self.destroy()
        SelectPathFrame(self.parent)

    def setAutoStartButtonStatus(self):
        if self.run_at_startup_var.get() or self.run_at_user_log_var.get() == 1:
            self.auto_start_buttom.config(state=NORMAL)
        else:
            self.auto_start_buttom.config(state=DISABLED)

    def onCheckSystemStartUp(self):
        if self.run_at_startup_var.get() == 1:
            pass
        else:
            pass
        self.setAutoStartButtonStatus()

    def onCheckUserLogs(self):
        if self.run_at_user_log_var.get() == 1:
            pass
        else:
            pass
        self.setAutoStartButtonStatus()

    def onCheckAutoStart(self):
        if self.auto_start_var.get() == 1:
            pass
        else:
            pass


class SelectPathFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.parent.title("FLE - KA Lite Setup - Select where to install KA Lite")
        self.loadImages()
        self.configureLayout()
        self.drawLayout()

    def loadImages(self):
        """Loads the images. The size must be the exact size of the image."""

        self.kaliteleaf_photo = PhotoImage(file="images/kaliteleaf.gif", width=16, height=16)

    def configureLayout(self):

        self.top_frame = Frame(self, relief=RAISED, borderwidth=1)

        self.tip_label = Label(self.top_frame, text="Select the path where you want to install.")
        self.kaliteleaf_label = Label(self.top_frame, image=self.kaliteleaf_photo, width=16, height=16)
        self.kaliteleaf_label.image = self.kaliteleaf_photo

        self.path_label_one_frame = Frame(self)
        self.path_label_one = Label(self.path_label_one_frame, text="Setup will install KA Lite into the following folder.")
        self.path_label_two_frame = Frame(self)
        self.path_label_two = Label(self.path_label_two_frame, text="If you would like to select a different folder, click Browse.")

        self.path_frame = Frame(self)
        self.path_entry_text = StringVar()
        self.path_entry = Entry(self.path_frame, width=50, textvariable=self.path_entry_text)

        global TARGET_PATH
        self.path_entry.insert(INSERT, TARGET_PATH)
        self.browse_button = Button(self.path_frame, text="Browse", width=8, height=1, command=self.browseDirectory)

        self.bottom_space_frame = Frame(self)

        self.next_button = Button(self, text="Next", width=15, height=2, command=self.showInstallationFrame)
        self.back_button = Button(self, text="Back", width=15, height=2, command=self.showServerConfigurationFrame)

    def drawLayout(self):
        self.pack(fill=BOTH, expand=True)
        self.top_frame.pack(fill=X)
        self.tip_label.pack(fill=X, side=LEFT, padx=5, pady=5)
        self.kaliteleaf_label.pack(fill=X, side=RIGHT, padx=5, pady=5)

        self.path_label_one_frame.pack(fill=X)
        self.path_label_one.pack(fill=X, expand=True, pady=(10,5))

        self.path_label_two_frame.pack(fill=X)
        self.path_label_two.pack(fill=X, side=LEFT, pady=(10,10))

        self.path_frame.pack(fill=X, side=TOP)
        self.path_entry.pack(fill=X, side=LEFT, padx=(10,0), pady=(15,0))
        self.browse_button.pack(fill=X, side=RIGHT, padx=(0,10), pady=(15,0))

        self.bottom_space_frame.pack(fill=BOTH, expand=True)

        self.next_button.pack(side=RIGHT, padx=5, pady=5)
        self.back_button.pack(side=RIGHT)

    def browseDirectory(self):
        global TARGET_PATH
        TARGET_PATH = fd.askdirectory()
        if platform.system() == 'Windows':
            TARGET_PATH = TARGET_PATH.replace("/", "\\")
        self.path_entry.delete(0, END)
        self.path_entry.insert(INSERT, TARGET_PATH)

    def showServerConfigurationFrame(self):
        self.pack_forget()
        self.destroy()
        ServerConfigurationFrame(self.parent)

    def showInstallationFrame(self):
        global TARGET_PATH
        if self.path_entry_text.get() == "":
            mb.showerror("Invalid directory", "Path cannot be empty.")
            return

        if not os.path.exists(os.path.dirname(self.path_entry_text.get())):
            try:
                if mb.askyesno("Directory doesn't exist.", "'%s' doesn't exist, do you want to create it?" % (os.path.dirname(self.path_entry_text.get()))):
                    os.makedirs(self.path_entry_text.get())
                else:
                    return
            except OSError:
                mb.showerror("Invalid directory", "You must enter a valid directory.")
                return

        TARGET_PATH = self.path_entry_text.get()
        self.pack_forget()
        self.destroy()
        InstallationFrame(self.parent)


class InstallationFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("FLE - KA Lite Setup - Start installation")
        self.loadImages()
        self.configureLayout()
        self.drawLayout()

    def loadImages(self):
        """Loads the images. The size must be the exact size of the image."""

        self.kaliteleaf_photo = PhotoImage(file="images/kaliteleaf.gif", width=16, height=16)

    def configureLayout(self):

        self.top_frame = Frame(self, relief=RAISED, borderwidth=1)

        self.tip_label_text = StringVar()
        self.tip_label = Label(self.top_frame, textvariable=self.tip_label_text)
        self.tip_label_text.set("Install KA Lite")

        self.kaliteleaf_label = Label(self.top_frame, image=self.kaliteleaf_photo, width=16, height=16)
        self.kaliteleaf_label.image = self.kaliteleaf_photo

        self.info_label_text = StringVar()
        self.info_label_frame = Frame(self)
        self.info_label = Label(self.info_label_frame, textvariable=self.info_label_text)
        self.info_label_text.set("Ready to start...")

        self.progress_bar_frame = Frame(self)
        self.progress_bar_value = IntVar()
        self.progress_bar = Progressbar(self.progress_bar_frame, mode="indeterminate", variable=self.progress_bar_value, length=400)

        self.bottom_space_frame = Frame(self)

        self.install_button_frame = Frame(self)
        self.install_button = Button(self.install_button_frame, text="Install", command=self.startInstallation, width=15, height=2)

        self.quit_button = Button(self.install_button_frame, text="Quit", state=DISABLED, command=quitInstaller, width=15, height=2)

    def drawLayout(self):

        self.pack(fill=BOTH, expand=True)
        self.top_frame.pack(fill=X)
        self.tip_label.pack(fill=X, side=LEFT, padx=5, pady=5)
        self.kaliteleaf_label.pack(fill=X, side=RIGHT, padx=5, pady=5)

        self.info_label_frame.pack(fill=X)
        self.info_label.pack(fill=X, expand=True, padx=10, pady=10)

        self.progress_bar_frame.pack(fill=X)
        self.progress_bar.pack(fill=X, expand=True, padx=15, pady=15)

        self.bottom_space_frame.pack(fill=BOTH, expand=True)

        self.quit_button.pack(fill=X, side=RIGHT)

        self.install_button_frame.pack(fill=X, padx=5, pady=5)
        self.install_button.pack(fill=X, side=RIGHT, padx=5)

    def startInstallation(self):
        global TARGET_PATH
        if not TARGET_PATH:
            return
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ka-lite")
        self.progress_bar.start(10)
        self.number_of_files = 0
        t1 = FuncThread(self.startInstall, src, self.progress_bar, self.number_of_files, self.progress_bar_value, self.tip_label_text, self.info_label_text, self.install_button, self.quit_button)
        t1.start()

    def startInstall(self, src, progress_bar, number_of_files, progress_bar_value, tip_label_text, info_label_text, install_button, quit_button):
        install_button.config(state=DISABLED)
        tip_label_text.set("Preparing to install KA Lite...")
        info_label_text.set("Calculating the number of files to copy...")

        files = []     
        if os.path.isdir(src):
            for path, dirs, filenames, in os.walk(src):
                files.extend(filenames)
        number_of_files = len(files)
        
        progress_bar.stop()
        progress_bar.config(maximum=number_of_files, mode="determinate", length=400)
        progress_bar_value.set(0)
        count = 0

        tip_label_text.set("Installing...")
        info_label_text.set(str(count)+" of "+str(number_of_files)+" copied.")
        
        list = []
        for path, dirs, filenames in os.walk(src):
            list.append((path, dirs, filenames))
        if not os.path.exists(TARGET_PATH):
            os.makedirs(TARGET_PATH)

        for t in list:
            for directory in t[1]:
                destDir = t[0].replace(src,TARGET_PATH)
                if not os.path.exists(os.path.join(destDir, directory)):
                    os.makedirs(os.path.join(destDir, directory))

            for sfile in t[2]:
                srcFile = os.path.join(t[0], sfile) 
                destFile = os.path.join(t[0].replace(src, TARGET_PATH), sfile)             
                shutil.copy(srcFile, destFile)
                count+=1
                info_label_text.set(str(count)+" of "+str(number_of_files)+" copied.")
                progress_bar_value.set(count)

        quit_button.config(state=NORMAL)
        tip_label_text.set("Installation complete.")
        info_label_text.set("All files were sucessfuly copied.")
        return

import threading
class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)


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
    root_window.protocol('WM_DELETE_WINDOW', quitInstaller)
    root_window.tk.call('wm', 'iconphoto', root_window._w, PhotoImage(file="images/kaliteleaf.gif", width=16, height=16))

    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()

    x_position = (screen_width - width)/2
    y_position = (screen_height - height)/2

    root_window.geometry('%dx%d+%d+%d' % (width, height, x_position, y_position))

    return root_window

def quitInstaller():
    """This function controls what happen when the user press the X button or any other option to quit the installer.
    """
    if mb.askyesno("Quit the installer.", "Are you sure you want to quit?"):
            sys.exit(0)

def main():
    
    root_window = createRootWindow(445, 350)
    
    WelcomeFrame(root_window)

    root_window.mainloop()


if __name__ == '__main__':
    main()