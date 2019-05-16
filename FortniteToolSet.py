import tkinter as tk
from tkinter import messagebox as tkmsgbx
import os
from PIL import Image, ImageTk
from colour import Color


# # # # # # # #
# A S S E T S #
# # # # # # # #

AssetsFolder = os.path.join(os.getcwd(), 'FortniteToolSetAssets')
DefaultFont = 'Alef'

BigFontSize = 20
RegularFontSize = 12
SmallFontSize = 8

DefaultPad = 10

# # # # # # # # # # # # # # # # #
# C O L O R   F U N C T I O N S #
# # # # # # # # # # # # # # # # #


class MyColor(Color):

    def __init__(self, *args, **kwargs):

        Color.__init__(self, *args, **kwargs)

    def NewChangeColorLightning(self, amount):

        newr = min(self.red * amount, 1)
        newg = min(self.green * amount, 1)
        newb = min(self.blue * amount, 1)

        return MyColor(rgb=(newr, newg, newb))


class MyColorPalette():

    def __init__(self, BackgroundColor,
                 BackgroudOppositeColor, TrailingColor,
                 DefaultColor, DiffrentColor):

        self.BackgroundColor = MyColor(BackgroundColor)  # the color of the window
        self.BackgroudOppositeColor = MyColor(BackgroudOppositeColor)  # For items on background
        self.TrailingColor = MyColor(TrailingColor)  # buttons, text fields etc.
        self.DefaultColor = MyColor(DefaultColor)  # most of the text
        self.DiffrentColor = MyColor(DiffrentColor)  # For special buttons and functions

        self.DarkColor = self.DefaultColor.NewChangeColorLightning(
            0.6)   # For smaller and less importent text
        self.LightColor = self.DefaultColor.NewChangeColorLightning(1.4)  # For text that pops up


class DefaultColorPalette(MyColorPalette):

    def __init__(self):

        MyColorPalette.__init__(self,
                                BackgroundColor='#222831',
                                BackgroudOppositeColor='#FFFFFF',
                                TrailingColor='#393e46',
                                DefaultColor='#51afe1',
                                DiffrentColor='#fd5f00')


ColorPalette = DefaultColorPalette()


# # # # # # # # # # # # #
# G E N E R A L   G U I #
# # # # # # # # # # # # #


class ProgramGUI(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.title('FortniteSetUpTool')  # default title
        self.LoadMenuBar()

        container = RegularFrame(self)
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
        program_menu.add_command(label="Settings", command=lambda: self.ShowPage(SettingsPage))
        program_menu.add_command(label="About", command=lambda: self.ShowPage(AboutPage))

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


class RegularFrame(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(
            self, master, bg=ColorPalette.BackgroundColor.get_hex_l(), *args, **kwargs)


class DarkFrame(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(
            self, master, bg=ColorPalette.DarkColor.get_hex_l(), *args, **kwargs)


class LightFrame(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(
            self, master, bg=ColorPalette.LightColor.get_hex_l(), *args, **kwargs)


class DefaultPage(RegularFrame):

    # default init for all pages in the program
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        RegularFrame.__init__(self, self.parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)

    # will run every time the page loads
    def ShowMe(self):
        pass


class HomePage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        # banner image
        imgBanner = Image.open(os.path.join(AssetsFolder, 'Banner.png')).resize((500, 250))
        Banner = ImageCanvas(self, imgBanner)
        Banner.pack(padx=DefaultPad, pady=DefaultPad)

        WelcomeTitle = BigLabel(self, text='Welcome Back!')
        WelcomeTitle.pack(padx=DefaultPad, pady=DefaultPad)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('Home'))


class AboutPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        Title = tk.Label(self, text='About - coming soon!')
        Title.pack(padx=DefaultPad, pady=DefaultPad)

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

        tk.Canvas.__init__(self, master, bg=ColorPalette.BackgroundColor.get_hex_l(), highlightthickness=0,
                           height=height, width=width, *args, **kwargs)

        self.create_image(0, 0, image=self.tkImg, anchor='nw')


class BigLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, BigFontSize)

        tk.Label.__init__(self, master, bg=ColorPalette.BackgroundColor.get_hex_l(), font=Font,
                          fg=ColorPalette.DiffrentColor.get_hex_l(), *args, **kwargs)


class RegularLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        tk.Label.__init__(self, master, bg=ColorPalette.BackgroundColor.get_hex_l(), font=Font,
                          fg=ColorPalette.DefaultColor.get_hex_l(), *args, **kwargs)


class RegularDarkLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        tk.Label.__init__(self, master, bg=ColorPalette.DarkColor.get_hex_l(), font=Font,
                          fg=ColorPalette.LightColor.get_hex_l(), *args, **kwargs)


class RegularLightLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        tk.Label.__init__(self, master, bg=ColorPalette.LightColor.get_hex_l(), font=Font,
                          fg=ColorPalette.DarkColor.get_hex_l(), *args, **kwargs)


class SpecialLightLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        tk.Label.__init__(self, master, bg=ColorPalette.LightColor.get_hex_l(), font=Font,
                          fg=ColorPalette.DiffrentColor.get_hex_l(), *args, **kwargs)


class SpecialDarkLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        tk.Label.__init__(self, master, bg=ColorPalette.DarkColor.get_hex_l(), font=Font,
                          fg=ColorPalette.DiffrentColor.get_hex_l(), *args, **kwargs)


class SmallLabel(tk.Label):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, SmallFontSize)

        tk.Label.__init__(self, master, bg=ColorPalette.BackgroundColor.get_hex_l(), font=Font,
                          fg=ColorPalette.DarkColor.get_hex_l(), *args, **kwargs)


class RegularEntry(tk.Entry):

    def __init__(self, master, *args, **kwargs):

        tk.Entry.__init__(self, master, bg=ColorPalette.TrailingColor.get_hex_l(),
                          font=(DefaultFont, RegularFontSize),  # font
                          relief=tk.FLAT,  # style of the entry
                          bd=2,  # size of border
                          fg=ColorPalette.BackgroudOppositeColor.get_hex_l(),  # color of font
                          selectbackground=ColorPalette.DarkColor.get_hex_l(),  # background color when text selected
                          *args, **kwargs)


class RegularButton(tk.Button):

    def __init__(self, master, *args, **kwargs):

        tk.Button.__init__(self, master,

                           # button
                           bg=ColorPalette.TrailingColor.get_hex_l(),  # regular color
                           activebackground=ColorPalette.DarkColor.get_hex_l(),  # while pressed color
                           bd=0,  # size of border

                           # font
                           font=(DefaultFont, RegularFontSize),
                           fg=ColorPalette.BackgroudOppositeColor.get_hex_l(),  # regular color
                           activeforeground=ColorPalette.BackgroudOppositeColor.get_hex_l(),  # while pressed color
                           justify=tk.CENTER,  # center all the text lines
                           *args, **kwargs)


class SmallButton(tk.Button):

    def __init__(self, master, *args, **kwargs):

        tk.Button.__init__(self, master,

                           # button
                           bg=ColorPalette.TrailingColor.get_hex_l(),  # regular color
                           activebackground=ColorPalette.DarkColor.get_hex_l(),  # while pressed color
                           bd=0,  # size of border

                           # font
                           font=(DefaultFont, SmallFontSize),
                           fg=ColorPalette.BackgroudOppositeColor.get_hex_l(),  # regular color
                           activeforeground=ColorPalette.BackgroudOppositeColor.get_hex_l(),  # while pressed color
                           justify=tk.CENTER,  # center all the text lines
                           *args, **kwargs)


class SpecialButton(tk.Button):

    def __init__(self, master, *args, **kwargs):

        tk.Button.__init__(self, master,

                           # button
                           bg=ColorPalette.DiffrentColor.get_hex_l(),  # regular color
                           activebackground=ColorPalette.DarkColor.get_hex_l(),  # while pressed color
                           bd=0,  # size of border

                           # font
                           font=(DefaultFont, RegularFontSize),
                           fg=ColorPalette.BackgroudOppositeColor.get_hex_l(),  # regular color
                           activeforeground=ColorPalette.BackgroudOppositeColor.get_hex_l(),  # while pressed color
                           justify=tk.CENTER,  # center all the text lines
                           *args, **kwargs)


class RegularRadiobutton(tk.Radiobutton):

    def __init__(self, master, *args, **kwargs):

        tk.Radiobutton.__init__(self, master,
                                # button
                                bg=ColorPalette.BackgroundColor.get_hex_l(),  # background color
                                activebackground=ColorPalette.BackgroundColor.get_hex_l(),  # while pressed color
                                borderwidth=0,  # size of border
                                selectcolor=ColorPalette.DarkColor.get_hex_l(),

                                # font
                                font=(DefaultFont, RegularFontSize),
                                fg=ColorPalette.BackgroudOppositeColor.get_hex_l(),  # text Color
                                activeforeground=ColorPalette.BackgroudOppositeColor.get_hex_l(),  # while pressed color
                                *args, **kwargs)







class NameDescFrame(RegularFrame):

    def __init__(self, master, settingname, settingdesc, *args, **kwargs):

        RegularFrame.__init__(self, master, *args, **kwargs)

        # text
        RegularLabel(self, text=settingname).grid(row=0, column=0)
        SmallLabel(self, text=settingdesc, wraplength=150).grid(
            row=1, column=0, padx=DefaultPad)


if __name__ == '__main__':
    root = ProgramGUI()
    root.mainloop()
