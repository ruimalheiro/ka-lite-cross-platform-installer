from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.config import Config
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '350')
Config.set('kivy', 'window_icon', 'logo48.ico')
import os, sys, shutil
from kivy.factory import Factory
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.event import EventDispatcher
import win32api


def get_drives_in_windows():
    drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
    for i in range(len(drives)):
        drives[i] = drives[i].replace('\\','')
    return drives

DRIVES = get_drives_in_windows()
TARGET_DIR = ""
    
# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""

<WelcomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        RstDocument:
            text: 'Welcome to KA Lite Setup\\n====\\nThis is the awesome new installer GUI.'
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 0.4
            Button:
                text: 'Continue'
                on_press: root.manager.current = 'directory'
            Button:
                text: 'Quit'

<LicenseScreen>:
    BoxLayout:
        Button:
            text: 'Continue'
            on_press: root.manager.current = 'directory'
        Button:
            text: 'Go back'
            on_press: root.manager.current = 'welcome'
            
<DirectoryScreen>:
    text_input: text_input
    id: d_screen
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser
            dirselect: True
            show_hidden: True
            on_selection: text_input.text = d_screen.is_directory(self.selection and self.selection[0])
            
        TextInput:
            id: text_input 
            size_hint_y: None
            height: 30
            multiline: False
            text: filechooser.path

        BoxLayout:
            size_hint_y: None
            height: 30
            Spinner:
                text: d_screen.get_drives()[0]
                values: d_screen.get_drives()
                on_release: d_screen.select_drive(self.text)
            Button:
                text: "New folder"

            Button:
                text: "Continue"
                on_press: d_screen.set_target_dir(filechooser.path, text_input.text)
                
            Button:
                text: "Go back"
                on_press: root.manager.current = 'welcome'
                
<InstallScreen>:
    id: install_id
    bar: p_id
    label: l_id
    i_button: i_button
    g_button: g_button
    BoxLayout:
        orientation: "vertical"
        Label:
            id: l_id
            text: "0 files copied."
        ProgressBar:
            id: p_id
            value: 0
            max: 500
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 0.3
            Button:
                id: i_button
                text: "Install"
                on_press: install_id.start_install()
            Button:
                id: g_button
                text: "Go back"
                on_press: root.manager.current = 'directory'
                
<FinishScreen>:
    id: finish_id
    BoxLayout:
        orientation: "vertical"
        RstDocument:
            text: 'Installation complete!\\n====\\nThank you for testing.'
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 0.4
            Button:
                text: "Finish"
                on_press: finish_id.exit()
""")

# Declare both screens
class WelcomeScreen(Screen):
    pass

class LicenseScreen(Screen):
    pass
    
class DirectoryScreen(Screen):
    def is_directory(self, d):
        if os.path.isdir(d):
            return d
        return ""
        
    def set_target_dir(self, path, target):
        global TARGET_DIR
        TARGET_DIR = os.path.join(path,target)
        sm.current = 'install'
        
    def get_drives(self):
        global DRIVES
        return DRIVES
        
    def select_drive(self, letter):
        print letter
        
numCopied = 0

class CopyOptions(object):

    count = 0
    numFiles = 0
    tree = []
    #src = sys._MEIPASS2 + '\ka-lite'
    src = os.path.join(os.path.dirname(sys.executable), "\ka-lite")
    dest = ""
    
    def get_num_files(self):
        return self.numFiles

    def countFiles(self, directory):
        files = []     
        if os.path.isdir(directory):
            for path, dirs, filenames, in os.walk(directory):
                files.extend(filenames)
        return len(files)
    
    def makedirs(self, dest, *args):
        if not os.path.exists(dest):
            os.makedirs(dest)
        
    def create_tupple_list(self, src):
        list = []
        for path, dirs, filenames in os.walk(src):
            list.append((path, dirs, filenames))
        return list
        
    def create_dir(self, path, dirs, src, dest, *args):
        for directory in dirs:
            destDir = path.replace(src,dest)
            self.makedirs(os.path.join(destDir, directory))
        
    def create_file(self, path, filenames, src, dest, *args):
        global numCopied
        for sfile in filenames:
            srcFile = os.path.join(path, sfile) 
            destFile = os.path.join(path.replace(src, dest), sfile)                
            shutil.copy(srcFile, destFile)
            numCopied += 1
            
    def prepare_copy(self):
        global TARGET_DIR
        self.dest = TARGET_DIR
        print "SOURCE: %s" % self.src
        print "preparing copy..."
        self.numFiles = self.countFiles(self.src)
        self.tree = self.create_tupple_list(self.src)
          
        #self.dest = "\Users\Rui\Desktop\TEST_AREA\Kivy-1.7.2-w32\dist"
        #self.makedirs(os.path.join(self.dest, 'ka-lite'))
        #self.dest = self.dest + "\ka-lite"
        
        if self.numFiles > 0:
            self.makedirs(self.dest)
        
        print "preparation done."
        return self.numFiles
            
    def copy_files(self, *args):
        global numCopied
        for t in self.tree[self.count:]:
            self.create_dir(t[0], t[1], self.src, self.dest)
            self.create_file(t[0], t[2], self.src, self.dest)
            self.count+=1
            return
            
            
            #for path, dirs, filenames in os.walk(src):
                #for directory in dirs:
                    #destDir = path.replace(src,dest)
                    #self.makedirs(os.path.join(destDir, directory))
            
                #for sfile in filenames:
                    #srcFile = os.path.join(path, sfile) 
                    #destFile = os.path.join(path.replace(src, dest), sfile)                
                    #shutil.copy(srcFile, destFile)
                    #numCopied += 1
  
class InstallScreen(Screen):

    bar = ObjectProperty(None)
    label = ObjectProperty(None)
    i_button = ObjectProperty(None)
    g_button = ObjectProperty(None)
    copy_ob = CopyOptions()
    
    def start_install(self):
        self.start_bar_update()
        self.start_label_update()
        self.remove_widget(self.i_button)
        self.remove_widget(self.g_button)
        self.label.text = "preparing to copy files..."
        self.bar.max = self.copy_ob.prepare_copy()
        Clock.schedule_interval(self.copy_ob.copy_files, 0.02)
        Clock.schedule_interval(self.check_status, 0.02)
        
    def check_status(self, *args):
        global numCopied
        if numCopied == self.copy_ob.get_num_files():
            Clock.unschedule(self.copy_ob.copy_files)
            Clock.unschedule(self.update_bar)
            Clock.unschedule(self.update_label)
            Clock.unschedule(self.check_status)
            sm.current = 'finish'
        
    def start_bar_update(self):
        Clock.schedule_interval(self.update_bar, 0.02)
        
    def start_label_update(self):
        Clock.schedule_interval(self.update_label, 0.02)
    
    def update_bar(self, *args):
        global numCopied
        self.bar.value = numCopied
        
    def update_label(self, *args):
        global numCopied
        self.label.text = "%d files copied." % numCopied
        
    
class FinishScreen(Screen):
    def exit(self):
        sys.exit(0)
                 

# Create the screen manager
sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='welcome'))
sm.add_widget(LicenseScreen(name='license'))
sm.add_widget(DirectoryScreen(name='directory'))
sm.add_widget(InstallScreen(name='install'))
sm.add_widget(FinishScreen(name='finish'))


Factory.register('DirectoryScreen', cls=DirectoryScreen)
Factory.register('InstallScreen', cls=InstallScreen)
Factory.register('FinishScreen', cls=FinishScreen)


class KaliteApp(App):
    icon = 'logo32.png'
    title = 'KA Lite Setup test'
    def build(self):
        return sm


if __name__ == '__main__':
    KaliteApp().run()