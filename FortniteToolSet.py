import tkinter as tk
from tkinter import messagebox, colorchooser
import os
from PIL import Image, ImageTk
from colour import Color
import pickle


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


# # # # # # # # # #
# S E T T I N G S #
# # # # # # # # # #

class SettingsContainer():

    def __init__(self, FilePath):
        self.AppearanceContainer = DefaultAppearanceSettings()

        self.FilePath = FilePath
        self.SaveChanges()

    def GetAppearanceContainer(self):
        return self.AppearanceContainer

    def SetAppearanceContainer(self, Container):
        self.AppearanceContainer = Container
        self.SaveChanges()

    def SaveChanges(self):
        SettingsSaveFile = open(self.FilePath, "wb")
        pickle.dump(self, SettingsSaveFile)
        SettingsSaveFile.close()


class AppearanceSettingsContainer():

    def __init__(self, BackgroundColor,
                 BackgroudOppositeColor, TrailingColor,
                 DiffrentColor, SpecialColor):

        self.BackgroundColor = MyColor(BackgroundColor)  # the color of the window
        self.BackgroudOppositeColor = MyColor(BackgroudOppositeColor)  # For items on background
        self.TrailingColor = MyColor(TrailingColor)  # buttons, text fields etc.
        self.DiffrentColor = MyColor(DiffrentColor)  # most of the text
        self.SpecialColor = MyColor(SpecialColor)  # For special buttons and functions

        self.__GenerateDarkColor()  # For smaller and less importent text
        self.__GenerateLightColor()  # For text that pops up

    def __GenerateDarkColor(self):
        self.DarkColor = self.DiffrentColor.NewChangeColorLightning(0.6)

    def __GenerateLightColor(self):
        self.LightColor = self.DiffrentColor.NewChangeColorLightning(1.4)

    def GetBackgroundColor(self):
        return self.BackgroundColor.get_hex_l()

    def SetBackgroundColor(self, hex_color):
        self.BackgroundColor = MyColor(hex_color)

    def GetBackgroundOppositeColor(self):
        return self.BackgroudOppositeColor.get_hex_l()

    def SetBackgroundOppositeColor(self, hex_color):
        self.BackgroundOppositeColor = MyColor(hex_color)

    def GetTrailingColor(self):
        return self.TrailingColor.get_hex_l()

    def SetTrailingColor(self, hex_color):
        self.TrailingColor = MyColor(hex_color)

    def GetDiffrentColor(self):
        return self.DiffrentColor.get_hex_l()

    def SetDiffrentColor(self, hex_color):
        self.DiffrentColor = MyColor(hex_color)
        self.__GenerateDarkColor()
        self.__GenerateLightColor()

    def GetSpecialColor(self):
        return self.SpecialColor.get_hex_l()

    def SetSpecialColor(self, hex_color):
        self.SpecialColor = MyColor(hex_color)

    def GetDarkColor(self):
        return self.DarkColor.get_hex_l()

    def GetLightColor(self):
        return self.LightColor.get_hex_l()


class DefaultAppearanceSettings(AppearanceSettingsContainer):

    def __init__(self):

        AppearanceSettingsContainer.__init__(self,
                                             BackgroundColor='#222831',
                                             BackgroudOppositeColor='#FFFFFF',
                                             TrailingColor='#393e46',
                                             DiffrentColor='#51afe1',
                                             SpecialColor='#fd5f00')


# # # # # # # # # # # # #
# G E N E R A L   G U I #
# # # # # # # # # # # # #

class ProgramGUI(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        SettingsPath = "Settings.FortniteToolSet"
        Corrupted = None
        if os.path.isfile(SettingsPath):
            pickle_in = open(SettingsPath, 'rb')
            try:
                self.SettingsContainer = pickle.load(pickle_in)
            except pickle.UnpicklingError:
                self.SettingsContainer = SettingsContainer(SettingsPath)
                # using this to load the window, and only then pop the error message.
                Corrupted = True

        else:
            self.SettingsContainer = SettingsContainer(SettingsPath)

        self.title('FortniteSetUpTool')  # default title
        self.LoadMenuBar()

        self.StatusBar = StatusBar(self)
        self.StatusBar.self_pack()

        container = RegularFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = [HomePage, AppearanceSettingsPage, AboutPage]  # all the pages list
        self.frames = {}
        self.LoadAllPages(parent=container, controller=self)
        self.CurrentPage = None
        self.ShowPage(HomePage)

        self.SetColors(self.SettingsContainer.GetAppearanceContainer())

        if Corrupted:
            messagebox.showerror(
                "Corrupted Settings File", 'Your "Settings.FortniteToolSet" file was corrupted. All your settings returned to their default state.')

    def LoadAllPages(self, parent, controller):
        for frame_obj in self.pages:
            frame = frame_obj(parent, controller)
            self.frames[frame_obj] = frame

    def SetColors(self, ColorPalette):
        for frame in self.frames:
            self.frames[frame].SetColors(ColorPalette)
        self.StatusBar.SetColors(ColorPalette)

    def ShowPage(self, page):
        if self.CurrentPage is not None:
            self.frames[self.CurrentPage].grid_forget()
        self.CurrentPage = page
        CurrentFrame = self.frames[page]
        CurrentFrame.grid(row=0, column=0, sticky="nsew")
        CurrentFrame.ShowMe()

    def SetTitle(self, page_name=None):
        if page_name is None:
            self.title('FortniteToolSet')
        else:
            self.title('%s - FortniteToolSet' % page_name)

    def LoadMenuBar(self):
        menubar = tk.Menu(self)
        program_menu = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label="Program", menu=program_menu)
        program_menu.add_command(label="Home", command=lambda: self.ShowPage(HomePage))
        program_menu.add_command(label="About", command=lambda: self.ShowPage(AboutPage))
        program_menu.add_separator()
        program_menu.add_command(label="Exit", command=lambda: self.Quit())

        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(
            label="Appearance", command=lambda: self.ShowPage(AppearanceSettingsPage))

        self.config(menu=menubar)

    def Quit(self):
        quit = messagebox.askyesno(
            title='Warning!',
            message="You are about to exit. Are you sure?")
        if quit:
            self.deiconify()
            self.destroy()
            self.quit()


# # # # # # # # # # # # # # #
# F R A M E   W I D G E T S #
# # # # # # # # # # # # # # #

class DefaultFrame(tk.Frame):

    elements = []

    def SetColors(self, ColorPalette):
        for element in self.elements:
            element.SetColors(ColorPalette)


class RegularFrame(DefaultFrame):

    def SetColors(self, ColorPalette):
        DefaultFrame.SetColors(self, ColorPalette)
        self.config(background=ColorPalette.GetBackgroundColor())


class DarkFrame(DefaultFrame):

    def SetColors(self, ColorPalette):
        DefaultFrame.SetColors(self, ColorPalette)
        self.config(background=ColorPalette.GetDarkColor())


class LightFrame(DefaultFrame):

    def SetColors(self, ColorPalette):
        DefaultFrame.SetColors(self, ColorPalette)
        self.config(background=ColorPalette.GetLightColor())


# # # # # # # # # # #
# G U I   P A G E S #
# # # # # # # # # # #

class DefaultPage(RegularFrame):

    # default init for all pages in the program
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        RegularFrame.__init__(self, self.parent)
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

        self.elements = [Banner, WelcomeTitle]

    def ShowMe(self):
        self.controller.SetTitle(None)


class AboutPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        TextFrame = RegularFrame(self)
        TextFrame.pack(padx=DefaultPad, pady=DefaultPad)

        ToolSetLabel = BigLabel(TextFrame, text='FortniteToolSet')
        ToolSetLabel.grid(row=0, column=0, padx=DefaultPad / 2)

        StringForTextLabel = ""
        ListForTextLabel = ["Made By RealA10N. For personal use only! (;",
                            "Assets the not mentioned below created by me.",
                            "Some icons in the program are made by Lucy G from Flaticon"]
        for line in ListForTextLabel:
            StringForTextLabel = StringForTextLabel + line + "\n"
        StringForTextLabel = StringForTextLabel[:-1]

        TextLabel = RegularLabel(TextFrame, text=StringForTextLabel)
        TextLabel.grid(row=1, column=0)

        # Icon pack: https://www.flaticon.com/packs/free-basic-ui-elements

        self.elements = [TextFrame, ToolSetLabel, TextLabel]

    def ShowMe(self):
        self.controller.SetTitle('About')


class AppearanceSettingsPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        for column_num in range(2):  # range(2) -> (0, 1)
            self.grid_columnconfigure(column_num, weight=1)

        Title = BigLabel(self, text='Appearance')
        Title.grid(padx=DefaultPad, pady=DefaultPad, row=0, columnspan=2, sticky='n')

        ColorPalette = self.controller.SettingsContainer.GetAppearanceContainer()
        self.SetColorPalette(ColorPalette)

        ColorElementsInfo = {'Background': {'Name': 'Background Color', 'Desc': 'Color for the background of the program.', 'StartingColor': ColorPalette.GetBackgroundColor()},
                             'Opposite': {'Name': 'Background Opposite Color', 'Desc': 'Color for items on the background, like text.', 'StartingColor': ColorPalette.GetBackgroundOppositeColor()},
                             'Trailing': {'Name': 'Trailing Color', 'Desc': 'Color for elements like basic buttons, basic text fields, etc.', 'StartingColor': ColorPalette.GetTrailingColor()},
                             'Different': {'Name': 'Different Color', 'Desc': 'Color with your personality! used in diffrent menus and special elements.', 'StartingColor': ColorPalette.GetDiffrentColor()},
                             'Special': {'Name': 'Special Color', 'Desc': "Completly diffrent. for special features like 'Save' buttons, etc.", 'StartingColor': ColorPalette.GetSpecialColor()},
                             }

        CurRow = 1
        self.ColorElements = {}
        for Element, InfoDict in ColorElementsInfo.items():
            ElementObj = AppearanceSettingLine(
                self, name=InfoDict['Name'], desc=InfoDict['Desc'], color=InfoDict['StartingColor'], grid_row=CurRow)
            CurRow += 1
            self.ColorElements[Element] = ElementObj

        BottomButtonsFrame = RegularFrame(self)
        BottomButtonsFrame.grid(columnspan=2, padx=DefaultPad, pady=DefaultPad)

        SaveButton = SpecialButton(BottomButtonsFrame, text='Save changes',
                                   command=lambda: self.SaveChanges())
        SaveButton.grid(padx=DefaultPad / 2, row=0, column=0, sticky='e')

        BackDefaultbutton = RegularButton(
            BottomButtonsFrame, text='Back To Default', command=lambda: self.ResetToDefault())
        BackDefaultbutton.grid(padx=DefaultPad / 2, row=0, column=1, sticky='w')

        AllColorElements = []
        for name, element in self.ColorElements.items():
            AllColorElements.append(element)

        self.elements = [Title, BottomButtonsFrame, SaveButton, BackDefaultbutton] + \
            AllColorElements

    def SetColorPalette(self, ColorPalette):
        self.controller.SettingsContainer.SetAppearanceContainer(ColorPalette)
        self.controller.SetColors(ColorPalette)

    def ResetToDefault(self):
        reset = messagebox.askyesno(
            title='Warning!',
            message="You are about to reset all the appearance settings to default. Are you sure?")
        if reset:
            NewColorPalette = DefaultAppearanceSettings()
            self.SetColorPalette(NewColorPalette)
            self.ColorElements['Background'].ChangeColor(NewColorPalette.GetBackgroundColor())
            self.ColorElements['Opposite'].ChangeColor(NewColorPalette.GetBackgroundOppositeColor())
            self.ColorElements['Trailing'].ChangeColor(NewColorPalette.GetTrailingColor())
            self.ColorElements['Different'].ChangeColor(NewColorPalette.GetDiffrentColor())
            self.ColorElements['Special'].ChangeColor(NewColorPalette.GetSpecialColor())

    def SaveChanges(self):
        SavedChangesValue = []
        for Name, Element in self.ColorElements.items():
            SavedChangesValue.append(Element.SaveChanges())
        NewColorPalette = AppearanceSettingsContainer(*SavedChangesValue)
        self.SetColorPalette(NewColorPalette)

    def ShowMe(self):
        self.controller.SetTitle('Appearance')


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
                    foreground=ColorPalette.GetSpecialColor())


class RegularLabel(DefaultLabel):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        DefaultLabel.__init__(self, master, font=Font, *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetBackgroundColor(),
                    foreground=ColorPalette.GetDiffrentColor())


class RegularDarkLabel(RegularLabel):

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetDarkColor(), foreground=ColorPalette.GetLightColor())


class RegularLightLabel(RegularLabel):

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetLightColor(), foreground=ColorPalette.GetDarkColor())


class SpecialLightLabel(DefaultLabel):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        DefaultLabel.__init__(self, master, font=Font, *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetLightColor(),
                    foreground=ColorPalette.GetSpecialColor())


class SpecialDarkLabel(DefaultLabel):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, RegularFontSize)

        DefaultLabel.__init__(self, master, font=Font, *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetDarkColor(),
                    foreground=ColorPalette.GetSpecialColor())


class SmallLabel(DefaultLabel):

    def __init__(self, master, *args, **kwargs):

        Font = (DefaultFont, SmallFontSize)

        DefaultLabel.__init__(self, master, font=Font, *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(background=ColorPalette.GetBackgroundColor(),
                    foreground=ColorPalette.GetDarkColor())


class ColorLabel(DefaultLabel):

    def __init__(self, master, *args, **kwargs):
        DefaultLabel.__init__(self, master,
                              padx=DefaultPad,
                              pady=DefaultPad,
                              width=2,
                              relief='ridge',
                              bd=2,
                              *args, **kwargs)


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
                               bd=2,  # size of border

                               # font
                               font=(DefaultFont, RegularFontSize),
                               justify=tk.CENTER,  # center all the text lines
                               relief='ridge',
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
        self.config(background=ColorPalette.GetSpecialColor(),    # regular color
                    activebackground=ColorPalette.GetDarkColor(),  # while pressed color
                    foreground=ColorPalette.GetBackgroundOppositeColor(),        # regular color
                    activeforeground=ColorPalette.GetBackgroundOppositeColor())  # while pressed color


class DefaultRadiobutton(tk.Radiobutton):

    def SetColors(self, ColorPalette):
        pass


class RegularRadiobutton(DefaultRadiobutton):

    def __init__(self, master, *args, **kwargs):

        DefaultRadiobutton.__init__(self, master,
                                    borderwidth=0,  # size of border
                                    font=(DefaultFont, RegularFontSize),
                                    *args, **kwargs)

    def SetColors(self, ColorPalette):
        self.config(bg=ColorPalette.GetBackgroundColor(),  # background color
                    activebackground=ColorPalette.GetBackgroundColor(),  # while pressed color
                    selectcolor=ColorPalette.GetDarkColor(),
                    fg=ColorPalette.GetBackgroundOppositeColor(),  # text color
                    activeforeground=ColorPalette.GetBackgroundOppositeColor())  # while pressed text color


# # # # # # # # # # # # # # # #
# C U S T O M   W I D G E T S #
# # # # # # # # # # # # # # # #

class AppearanceSettingLine():

    def __init__(self, master, name, desc, color, grid_row):

        self.Label = NameDescFrame(master, name, desc)
        self.Label.grid(pady=DefaultPad / 2, padx=DefaultPad / 2, row=grid_row, column=0)
        self.ColorPicker = AppearanceColorPicker(master, color, name)
        self.ColorPicker.grid(pady=DefaultPad / 2, padx=DefaultPad / 2, row=grid_row, column=1)

        self.elements = [self.Label, self.ColorPicker]

    def SetColors(self, ColorPalette):
        for element in self.elements:
            element.SetColors(ColorPalette)

    def ChangeColor(self, color):
        self.ColorPicker.ChangeColor(color)

    def SaveChanges(self):
        return self.ColorPicker.SaveChanges()


class AppearanceColorPicker(RegularFrame):

    def __init__(self, master, starting_value, name, *args, **kwargs):
        RegularFrame.__init__(self, master, *args, **kwargs)

        self.DefaultValue = starting_value
        self.NewValue = starting_value

        self.ColorLabel = ColorLabel(self)
        self.UpdateColorLabel()
        self.ColorLabel.grid(row=0, column=0)

        ChangeButton = RegularButton(
            self, text='Change', command=lambda: self.ChangeColor(self.PickColor(self.NewValue, name)))
        ChangeButton.grid(row=0, column=1)

        ResetButton = RegularButton(self, text='Restore', command=lambda: self.RestoreColor())
        ResetButton.grid(row=0, column=2)

        self.elements = [ChangeButton, ResetButton]

    def UpdateColorLabel(self):
        self.ColorLabel.config(bg=self.NewValue)

    def PickColor(self, starting_color, title):
        return colorchooser.askcolor(starting_color, title='Select {}'.format(title))[1]

    def ChangeColor(self, ColorHex):
        if ColorHex is not None:
            self.NewValue = ColorHex
            self.UpdateColorLabel()

    def RestoreColor(self):
        self.NewValue = self.DefaultValue
        self.UpdateColorLabel()

    def SaveChanges(self):
        self.DefaultValue = self.NewValue
        return self.NewValue


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

        self.elements = [StatusLabel, AutoUpdateFrame,
                         AutoUpdateLabel, TimerLabel, UpdateButton]

    def change_timer_text(self, new_time):
        self.__TimerLabelStr.set(new_time)

    def change_status_text(self, status_text):
        self.__StautsLabelStr.set(status_text)

    def self_pack(self):
        self.pack(side='bottom', fill='both')


class NameDescFrame(RegularFrame):

    def __init__(self, master, settingname, settingdesc, *args, **kwargs):

        RegularFrame.__init__(self, master, *args, **kwargs)

        NameLabel = RegularLabel(self, text=settingname)
        NameLabel.grid(row=0, column=0)
        DescLabel = SmallLabel(self, text=settingdesc, wraplength=175)
        DescLabel.grid(row=1, column=0, padx=DefaultPad)

        self.elements = [NameLabel, DescLabel]

    def SetColors(self, ColorPalette):
        RegularFrame.SetColors(self, ColorPalette)
        for element in self.elements:
            element.SetColors(ColorPalette)


# # # # # # # # # # # # # #
# M A I N   P R O G R A M #
# # # # # # # # # # # # # #

if __name__ == '__main__':
    root = ProgramGUI()
    root.mainloop()
