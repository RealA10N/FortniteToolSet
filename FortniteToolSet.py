import tkinter as tk
from tkinter import messagebox, colorchooser
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

    def GetBackgroundColor(self):
        return self.BackgroundColor.get_hex_l()

    def GetBackgroundOppositeColor(self):
        return self.BackgroudOppositeColor.get_hex_l()

    def GetTrailingColor(self):
        return self.TrailingColor.get_hex_l()

    def GetDefaultColor(self):
        return self.DefaultColor.get_hex_l()

    def GetDiffrentColor(self):
        return self.DiffrentColor.get_hex_l()

    def GetDarkColor(self):
        return self.DarkColor.get_hex_l()

    def GetLightColor(self):
        return self.LightColor.get_hex_l()


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

        self.StatusBar = StatusBar(self)
        self.StatusBar.self_pack()

        container = RegularFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = (HomePage, AboutPage, SettingsPage)  # all the pages list
        self.frames = {}
        self.LoadAllPages(parent=container, controller=self)
        self.ShowPage(HomePage)

        self.SetColorPalette(DefaultColorPalette())

    def LoadAllPages(self, parent, controller):
        for frame_obj in self.pages:
            frame = frame_obj(parent, controller)
            self.frames[frame_obj] = frame

    def SetColorPalette(self, ColorPalette):
        for frame in self.frames:
            self.frames[frame].SetAllElementsColors(ColorPalette)
        self.StatusBar.SetAllElementsColors(ColorPalette)

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
        quit = messagebox.askyesno(
            title=self.GetTitle('Warning!'),
            message="You are about to exit. Are you sure?")
        if quit:
            self.deiconify()
            self.destroy()
            self.quit()


# # # # # # # # # # #
# G U I   P A G E S #
# # # # # # # # # # #

class DefaultFrame(tk.Frame):

    def SetColors(self, ColorPalette):
        pass


class RegularFrame(DefaultFrame):

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetBackgroundColor())


class DarkFrame(DefaultFrame):

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetDarkColor())


class LightFrame(DefaultFrame):

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetLightColor())


class DefaultPage(RegularFrame):

    # default init for all pages in the program
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.elements = ()  # empty tuple
        RegularFrame.__init__(self, self.parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)

    # will run every time the page loads
    def ShowMe(self):
        pass

    def SetAllElementsColors(self, ColorPalette):
        for element in self.elements:
            element.SetColors(ColorPalette)


class HomePage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        # banner image
        imgBanner = Image.open(os.path.join(AssetsFolder, 'Banner.png')).resize((500, 250))
        Banner = ImageCanvas(self, imgBanner)
        Banner.pack(padx=DefaultPad, pady=DefaultPad)

        WelcomeTitle = BigLabel(self, text='Welcome Back!')
        WelcomeTitle.pack(padx=DefaultPad, pady=DefaultPad)

        AllScriptsButton = RegularButton(
            self, text='All Scripts Routine', command=lambda: self.allscriptsroutine())
        AllScriptsButton.pack(padx=DefaultPad, pady=DefaultPad)

        self.elements = (self, Banner, WelcomeTitle, AllScriptsButton)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('Home'))


class AboutPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        Title = RegularLabel(self, text='About - coming soon!')
        Title.pack(padx=DefaultPad, pady=DefaultPad)

        self.elements = (self, Title)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('About'))


class SettingsPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        Title = BigLabel(self, text='Settigns')
        Title.grid(padx=DefaultPad, pady=DefaultPad, row=0, columnspan=2, sticky='n')

        self.BackgroundColorHex = tk.StringVar()
        BackgroundColorEntry = RegularEntry(self, textvariable=self.BackgroundColorHex)
        BackgroundColorEntry.grid()

        saveframe = RegularFrame(self)
        saveframe.grid(columnspan=2, padx=DefaultPad, pady=DefaultPad, sticky='n')

        Savebutton = SpecialButton(saveframe, text='Save changes',
                                   command=lambda: self.SaveChanges())
        Savebutton.grid(row=0, column=0, sticky='e')

        Resetbutton = RegularButton(saveframe, text='Reset changes')
        Resetbutton.grid(padx=DefaultPad, pady=DefaultPad, row=0, column=1, sticky='w')

        self.elements = (self, Title, saveframe, Savebutton, Resetbutton, BackgroundColorEntry)

    def SaveChanges(self):
        NewColorPalette = DefaultColorPalette()
        NewColorPalette.BackgroundColor = MyColor(self.BackgroundColorHex.get())
        self.controller.SetColorPalette(NewColorPalette)

    def ShowMe(self):
        self.controller.title(self.controller.GetTitle('Settings'))


# # # # # # # # # # # # # #
# G U I   E L E M E N T S #
# # # # # # # # # # # # # #

class DefaultCanvas(tk.Canvas):

    def SetColors(self, ColorPalette):
        pass


class ImageCanvas(DefaultCanvas):

    def __init__(self, master, pilImg, *args, **kwargs):

        self.pilImg = pilImg
        self.tkImg = ImageTk.PhotoImage(self.pilImg)
        width, height = pilImg.size

        tk.Canvas.__init__(self, master, highlightthickness=0,
                           height=height, width=width, *args, **kwargs)

        self.create_image(0, 0, image=self.tkImg, anchor='nw')

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetBackgroundColor())


class DefaultLabel(tk.Label):

    def SetColors(self, ColorPalette):
        pass


class BigLabel(DefaultLabel):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, BigFontSize)

        DefaultLabel.__init__(self, master, font=Font, *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetBackgroundColor(),
                    foreground=ColorPalette.GetDiffrentColor())


class RegularLabel(DefaultLabel):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        DefaultLabel.__init__(self, master, font=Font, *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetBackgroundColor(),
                    foreground=ColorPalette.GetDefaultColor())


class RegularDarkLabel(DefaultLabel):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        DefaultLabel.__init__(self, master, font=Font, *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetDarkColor(), foreground=ColorPalette.GetLightColor())


class RegularLightLabel(DefaultLabel):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        DefaultLabel.__init__(self, master, font=Font, *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetLightColor(), foreground=ColorPalette.GetDarkColor())


class SpecialLightLabel(DefaultLabel):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        DefaultLabel.__init__(self, master, font=Font, *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetLightColor(),
                    foreground=ColorPalette.GetDiffrentColor())


class SpecialDarkLabel(DefaultLabel):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        DefaultLabel.__init__(self, master, font=Font, *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetDarkColor(),
                    foreground=ColorPalette.GetDiffrentColor())


class SmallLabel(DefaultLabel):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, SmallFontSize)

        DefaultLabel.__init__(self, master, font=Font, *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetBackgroundColor(),
                    foreground=ColorPalette.GetDarkColor())


class DefaultEntry(tk.Entry):

    def SetColors(self, ColorPalette):
        pass


class RegularEntry(DefaultEntry):

    def __init__(self, master, *args, **kwargs):

        DefaultEntry.__init__(self, master,
                              font=(DefaultFont, RegularFontSize),  # font
                              relief=tk.FLAT,  # style of the entry
                              bd=2,  # size of border
                              *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetTrailingColor(),
                    foreground=ColorPalette.GetBackgroundOppositeColor(),  # color of font
                    selectbackground=ColorPalette.GetDarkColor())  # background color when text selected


class DefaultButton(tk.Button):

    def SetColors(self, ColorPalette):
        pass


class RegularButton(DefaultButton):

    def __init__(self, master, *args, **kwargs):

        DefaultButton.__init__(self, master,
                               # button
                               bd=0,  # size of border

                               # font
                               font=(DefaultFont, RegularFontSize),
                               justify=tk.CENTER,  # center all the text lines
                               *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetTrailingColor(),    # regular color
                    activebackground=ColorPalette.GetDarkColor(),  # while pressed color
                    foreground=ColorPalette.GetBackgroundOppositeColor(),        # regular color
                    activeforeground=ColorPalette.GetBackgroundOppositeColor())  # while pressed color


class SmallButton(RegularButton):

    def __init__(self, master, *args, **kwargs):

        DefaultButton.__init__(self, master,
                               # button
                               bd=0,  # size of border

                               # font
                               font=(DefaultFont, SmallFontSize),
                               justify=tk.CENTER,  # center all the text lines
                               *args, **kwargs)


class SpecialButton(RegularButton):

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetDiffrentColor(),    # regular color
                    activebackground=ColorPalette.GetDarkColor(),  # while pressed color
                    foreground=ColorPalette.GetBackgroundOppositeColor(),        # regular color
                    activeforeground=ColorPalette.GetBackgroundOppositeColor())  # while pressed color


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


class StatusBar(DarkFrame):

    def __init__(self, master, *args, **kwargs):

        DarkFrame.__init__(self, master, *args, **kwargs)

        for column_num in range(2):  # range(2) -> (0, 1)
            self.grid_columnconfigure(column_num, weight=1)

        # status label
        self.__StautsLabelStr = tk.StringVar()
        self.__StautsLabelStr.set('Nothing running right now!')
        StatusLabel = RegularDarkLabel(self, textvariable=self.__StautsLabelStr)
        StatusLabel.grid(row=0, column=0, padx=DefaultPad, pady=DefaultPad / 3, sticky='w')

        AutoUpdateFrame = DarkFrame(self)
        AutoUpdateFrame.grid(row=0, column=1, padx=DefaultPad / 2, pady=DefaultPad / 3, sticky='e')

        # auto update Label
        self.__AutoUpdateLabelStr = tk.StringVar()
        self.__AutoUpdateLabelStr.set('Next auto update in:')
        AutoUpdateLabel = RegularDarkLabel(AutoUpdateFrame, textvariable=self.__AutoUpdateLabelStr)
        AutoUpdateLabel.grid(row=0, column=0)

        # timer label
        self.__TimerLabelStr = tk.StringVar()
        self.__TimerLabelStr.set('4:39')
        TimerLabel = SpecialDarkLabel(AutoUpdateFrame, textvariable=self.__TimerLabelStr)
        TimerLabel.grid(row=0, column=1)

        # update button
        self.__UpdateButtonStr = tk.StringVar()
        self.__UpdateButtonStr.set('Update')
        UpdateButton = SmallButton(AutoUpdateFrame, textvariable=self.__UpdateButtonStr)
        UpdateButton.grid(row=0, column=2, padx=DefaultPad / 2)

        self.elements = (self, StatusLabel, AutoUpdateFrame,
                         AutoUpdateLabel, TimerLabel, UpdateButton)

    def SetAllElementsColors(self, ColorPalette):
        for element in self.elements:
            element.SetColors(ColorPalette)

    def change_timer_text(self, new_time):
        self.__TimerLabelStr.set(new_time)

    def change_status_text(self, status_text):
        self.__StautsLabelStr.set(status_text)

    def self_pack(self):
        self.pack(side='bottom', fill='both')


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
