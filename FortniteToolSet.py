import tkinter as tk
from tkinter import messagebox as tkmsgbx
import os
from PIL import Image, ImageTk

# # # # # # # #
# A S S E T S #
# # # # # # # #

AssetsFolder = os.path.join(os.getcwd(), 'FortniteToolSetAssets')
DefaultFont = 'Alef'

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


class MyColor():

    def __init__(self, RGB=None, Hex=None):
        if RGB is None:
            if Hex is None:
                raise(Exception, 'Please init a color using hex or rgb')
            else:
                self._hex = Hex
                self._rgb = self._HexColorToRGB(Hex)
        else:
            if Hex is None:
                self._rgb = RGB
                self._hex = self._RGBToHexColor(RGB)
            else:
                raise(Exception, 'Please init only one color using rgb OR hex')

    def GetHex(self):
        return self._hex

    def GetHashtagHex(self):
        return '#' + self.GetHex()

    def GetRGB(self):
        return self._rgb

    def _HexColorToRGB(self, hex):
        hexR = hex[0:2]
        hexG = hex[2:4]
        hexB = hex[4:6]
        return (int(hexR, 16), int(hexG, 16), int(hexB, 16))

    def _RGBToHexColor(self, rgb):
        return hex(rgb[0])[2:] + hex(rgb[1])[2:] + hex(rgb[2])[2:]

    def MixColor(self, color):
        mixedR = (self.GetRGB[0] + color.GetRGB[0]) / 2
        mixedG = (self.GetRGB[1] + color.GetRGB[1]) / 2
        mixedB = (self.GetRGB[2] + color.GetRGB[2]) / 2
        return MyColor(RGB=(mixedR, mixedG, mixedB))

    def DarkenRGBColor(self, amount):
        newR = max(self.GetRGB[0] - amount, 0)
        newG = max(self.GetRGB[1] - amount, 0)
        newB = max(self.GetRGB[2] - amount, 0)
        return MyColor(RGB=(newR, newG, newB))

    def LightenRGBColor(self, amount):
        newR = min(self.GetRGB[0] + amount, 255)
        newG = min(self.GetRGB[1] + amount, 255)
        newB = min(self.GetRGB[2] + amount, 255)
        return MyColor(RGB=(newR, newG, newB))


# colors
BackgroundColor = MyColor(Hex='222831')  # the color of the window
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
        tk.Frame.__init__(self, self.parent, bg=BackgroundColor.GetHashtagHex())
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

        tk.Canvas.__init__(self, master, bg=BackgroundColor.GetHashtagHex(), highlightthickness=0,
                           height=height, width=width, *args, **kwargs)

        self.create_image(0, 0, image=self.tkImg, anchor='nw')


class BigLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        BigLabelFont = (DefaultFont, BigFontSize)
        BigLabelColor = DefaultTextColor

        tk.Label.__init__(self, master, bg=BackgroundColor.GetHashtagHex(), font=BigLabelFont,
                          fg=BigLabelColor, *args, **kwargs)


class RegularLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        RegularLabelFont = (DefaultFont, RegularFontSize)
        RegularLabelColor = DefaultTextColor

        tk.Label.__init__(self, master, bg=BackgroundColor.GetHashtagHex(), font=RegularLabelFont,
                          fg=RegularLabelColor, *args, **kwargs)


class RegularEntry(tk.Entry):

    def __init__(self, master, *args, **kwargs):

        tk.Entry.__init__(self, master, bg=TrailingColor,
                          font=(DefaultFont, RegularFontSize),  # font
                          relief=tk.FLAT,  # style of the entry
                          bd=2,  # size of border
                          fg='white',  # color of font
                          selectbackground=DrakTextColor,  # background color when text selected
                          *args, **kwargs)


class RegularButton(tk.Button):

    def __init__(self, master, *args, **kwargs):

        tk.Button.__init__(self, master,

                           # button
                           bg=LightTextColor,  # regular color
                           activebackground=DrakTextColor,  # while pressed color
                           bd=0,  # size of border

                           # font
                           font=(DefaultFont, RegularFontSize),
                           fg='white',  # regular color
                           activeforeground='white',  # while pressed color
                           justify=tk.CENTER,  # center all the text lines
                           *args, **kwargs)


class SpecialButton(tk.Button):

    def __init__(self, master, *args, **kwargs):

        tk.Button.__init__(self, master,

                           # button
                           bg=DiffrentColor,  # regular color
                           activebackground=DrakTextColor,  # while pressed color
                           bd=0,  # size of border

                           # font color
                           font=(DefaultFont, RegularFontSize),
                           fg='white',  # regular color
                           activeforeground='white',  # while pressed color
                           justify=tk.CENTER,  # center all the text lines
                           *args, **kwargs)


root = ProgramGUI()
root.mainloop()
