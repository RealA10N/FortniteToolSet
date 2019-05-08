import tkinter as tk
from tkinter import messagebox as tkmsgbx
import os
from PIL import Image, ImageTk

# # # # # # # #
# A S S E T S #
# # # # # # # #

AssetsFolder = os.path.join(os.getcwd(), 'FortniteToolSetAssets')
DefaultFont = 'Alef'

# colors
BackgroundColor = '#222831'   # the color of the window
TrailingColor = '#393e46'     # buttons, text fields etc.
WhiteColor = '#eeeeee'        # gives the whites presonal style (;
DefaultTextColor = '#145374'  # most of the text
DrakTextColor = '#00334e'     # For smaller and less importent text
LightTextColor = '#5588a3'    # For text that pops up
DiffrentColor = '#fd5f00'     # Complatly diffrent color, for special buttons and functions

BigFontSize = 20
RegularFontSize = 12
SmallFontSize = 8

DefaultPadX = 10
DefaultPadY = 10

# # # # # # # # # # # # # # # # #
# C O L O R   F U N C T I O N S #
# # # # # # # # # # # # # # # # #


def HexColorToRGB(hex):
    hexR = hex[0:2]
    hexG = hex[2:4]
    hexB = hex[4:6]
    return (int(hexR, 16), int(hexG, 16), int(hexB, 16))


def RGBToHexColor(rgb):
    return hex(rgb[0])[2:] + hex(rgb[1])[2:] + hex(rgb[2])[2:]


def MixRGBColors(rgb1, rgb2):
    mixedR = (rgb1[0] + rgb2[0]) / 2
    mixedG = (rgb1[1] + rgb2[1]) / 2
    mixedB = (rgb1[2] + rgb2[2]) / 2
    return (mixedR, mixedG, mixedB)


def DarkenRGBColor(rgb, amount):
    newR = max(rgb[0] - amount, 0)
    newG = max(rgb[1] - amount, 0)
    newB = max(rgb[2] - amount, 0)
    return (newR, newG, newB)


def LightenRGBColor(rgb, amount):
    newR = min(rgb[0] + amount, 255)
    newG = min(rgb[1] + amount, 255)
    newB = min(rgb[2] + amount, 255)
    return (newR, newG, newB)


# # # # # # # # # # # # #
# G E N E R A L   G U I #
# # # # # # # # # # # # #


class ProgramGUI(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # place window on top & in the middle of the screen
        self.eval('tk::PlaceWindow %s' % self.winfo_toplevel())

        self.title('FortniteSetUpTool')  # default title
        self.LoadMenuBar()

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.LoadAllPages(parent=container, controller=self)
        self.ShowPage(HomePage)

    def LoadAllPages(self, parent, controller):
        pages = (HomePage, AboutPage, SettingsPage)  # all the pages list
        for frame_obj in pages:
            frame = frame_obj(parent, controller)
            self.frames[frame_obj] = frame

    def ShowPage(self, page):
        frame = self.frames[page]
        frame.ShowMe()
        frame.tkraise()

    def GetTitle(self, page_name):
        return '%s | FortniteToolSet' % page_name

    def LoadMenuBar(self):
        menubar = tk.Menu(self)
        program_menu = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label="Program", menu=program_menu)
        program_menu.add_command(label="Home", command=lambda: self.ShowPage(HomePage))
        program_menu.add_command(label="About", command=lambda: self.ShowPage(AboutPage))
        program_menu.add_command(label="Settings", command=lambda: self.ShowPage(SettingsPage))

        program_menu.add_separator()

        program_menu.add_command(label="Exit", command=lambda: self.Quit())

        self.config(menu=menubar)

    def Quit(self):
        quit = tkmsgbx.askyesno(
            title=self.GetTitle('Warning!'),
            message="You are about to exit. Are you sure?")
        if quit:
            self.deiconify()
            self.destroy()
            self.quit()


# # # # # # # # # # #
# G U I   P A G E S #
# # # # # # # # # # #

class DefaultPage(tk.Frame):

    # default init for all pages in the program
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, self.parent, bg=BackgroundColor)
        self.grid(row=0, column=0, sticky="nsew")

    # will run every time the page loads
    def ShowMe(self):
        pass


class HomePage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        # banner image
        imgBanner = Image.open(os.path.join(AssetsFolder, 'Banner.png')).resize((500, 250))
        Banner = ImageCanvas(self, imgBanner)
        Banner.pack(padx=DefaultPadX, pady=DefaultPadY)

        WelcomeTitle = BigLabel(self, text='Welcome Back!')
        WelcomeTitle.pack(padx=DefaultPadX, pady=DefaultPadY)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('Home'))


class AboutPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        Title = tk.Label(self, text='About - coming soon!')
        Title.pack(padx=DefaultPadX, pady=DefaultPadY)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('About'))


class SettingsPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        TestEntry = RegularEntry(self)
        TestEntry.grid(row=0, column=0)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('Settings'))


# # # # # # # # # # # # # #
# G U I   E L E M E N T S #
# # # # # # # # # # # # # #

# crates a transperent canvas and pastes image on it
class ImageCanvas(tk.Canvas):

    def __init__(self, master, pilImg, *args, **kwargs):

        self.pilImg = pilImg
        self.tkImg = ImageTk.PhotoImage(self.pilImg)
        width, height = pilImg.size

        tk.Canvas.__init__(self, master, bg=BackgroundColor, highlightthickness=0,
                           height=height, width=width, *args, **kwargs)

        self.create_image(0, 0, image=self.tkImg, anchor='nw')


class BigLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        BigLabelFont = (DefaultFont, BigFontSize)
        BigLabelColor = DefaultTextColor

        tk.Label.__init__(self, master, bg=BackgroundColor, font=BigLabelFont,
                          fg=BigLabelColor, *args, **kwargs)


class RegularLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        RegularLabelFont = (DefaultFont, RegularFontSize)
        RegularLabelColor = DefaultTextColor

        tk.Label.__init__(self, master, bg=BackgroundColor, font=RegularLabelFont,
                          fg=RegularLabelColor, *args, **kwargs)


class RegularEntry(tk.Entry):

    def __init__(self, master, *args, **kwargs):

        tk.Entry.__init__(self, master, bg=TrailingColor,
                          font=(DefaultFont, RegularFontSize),  # font
                          relief=tk.FLAT,  # style of the entry
                          bd=2,  # size of border
                          fg=WhiteColor,  # color of font
                          selectbackground=DrakTextColor,  # background color when text selected
                          *args, **kwargs)


root = ProgramGUI()
root.mainloop()
