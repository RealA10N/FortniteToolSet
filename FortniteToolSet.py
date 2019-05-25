import tkinter as tk
from tkinter import messagebox, colorchooser
import os
from PIL import Image, ImageTk
from colour import Color
import pickle
import win32clipboard
from io import BytesIO


# # # # # # # #
# A S S E T S #
# # # # # # # #

AssetsFolder = os.path.join(os.getcwd(), 'FortniteToolSetAssets')
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
                 DiffrentColor, SpecialColor, Font, RegularFontSize):

        self.BackgroundColor = MyColor(BackgroundColor)  # the color of the window
        self.BackgroudOppositeColor = MyColor(BackgroudOppositeColor)  # For items on background
        self.TrailingColor = MyColor(TrailingColor)  # buttons, text fields etc.
        self.DiffrentColor = MyColor(DiffrentColor)  # most of the text
        self.SpecialColor = MyColor(SpecialColor)  # For special buttons and functions

        self.__GenerateDarkColor()  # For smaller and less importent text
        self.__GenerateLightColor()  # For text that pops up

        self.Font = Font
        self.SetFontSize(RegularFontSize)

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

    # - - - - - - - - - - #
    # n o t   c o l o r s #
    # - - - - - - - - - - #

    def SetFont(self, FontName):
        self.Font = FontName

    def SetFontSize(self, RegularFontSize):
        multiplier = (5 / 3)  # 1.666666...
        self.RegularFontSize = int(RegularFontSize)
        self.BigFontSize = int(self.RegularFontSize * multiplier)
        self.SmallFontSize = int(self.RegularFontSize / multiplier)

    def GetFontSize(self):
        return self.RegularFontSize

    def GetFont(self):
        return self.Font

    def GetRegularFont(self):
        return (self.Font, self.RegularFontSize)

    def GetBigFont(self):
        return (self.Font, self.BigFontSize)

    def GetSmallFont(self):
        return (self.Font, self.SmallFontSize)


class DefaultAppearanceSettings(AppearanceSettingsContainer):

    def __init__(self):

        AppearanceSettingsContainer.__init__(self,
                                             # c o l o r s
                                             BackgroundColor='#222831',
                                             BackgroudOppositeColor='#FFFFFF',
                                             TrailingColor='#393e46',
                                             DiffrentColor='#51afe1',
                                             SpecialColor='#fd5f00',

                                             # f o n t
                                             Font='Alef',
                                             RegularFontSize=12)


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
            except:
                self.SettingsContainer = SettingsContainer(SettingsPath)
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

        self.SetAppearance(self.SettingsContainer.GetAppearanceContainer())

        if Corrupted:  # using this to load the window, and only then pop the error message.
            messagebox.showerror(
                "Corrupted Settings File", 'Your "Settings.FortniteToolSet" file was corrupted. All your settings returned to their default state.')

    def LoadAllPages(self, parent, controller):
        for frame_obj in self.pages:
            frame = frame_obj(parent, controller)
            self.frames[frame_obj] = frame

    def SetAppearance(self, Container):
        for frame in self.frames:
            self.frames[frame].SetAppearance(Container)
        self.StatusBar.SetAppearance(Container)

    def ShowPage(self, page):
        CurrentFrame = self.frames[page]
        CurrentFrame.grid(row=0, column=0, sticky="nsew")

        if self.CurrentPage is not None:
            self.frames[self.CurrentPage].grid_forget()

        self.CurrentPage = page
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

    def SetAppearance(self, Container):
        for element in self.elements:
            element.SetAppearance(Container)


class RegularFrame(DefaultFrame):

    def SetAppearance(self, Container):
        DefaultFrame.SetAppearance(self, Container)
        self.config(background=Container.GetBackgroundColor())


class DarkFrame(DefaultFrame):

    def SetAppearance(self, Container):
        DefaultFrame.SetAppearance(self, Container)
        self.config(background=Container.GetDarkColor())


class LightFrame(DefaultFrame):

    def SetAppearance(self, Container):
        DefaultFrame.SetAppearance(self, Container)
        self.config(background=Container.GetLightColor())


# # # # # # # # # # #
# G U I   P A G E S #
# # # # # # # # # # #

class DefaultPage(RegularFrame):

    # default init for all pages in the program
    def __init__(self, parent, controller, basic_name):
        self.parent = parent
        self.controller = controller
        self.basic_name = basic_name
        RegularFrame.__init__(self, self.parent)
        self.grid_columnconfigure(0, weight=1)

    # will run every time the page loads
    def ShowMe(self):
        self.controller.SetTitle(self.basic_name)


class HomePage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller, basic_name=None)

        # banner image
        imgBanner = Image.open(os.path.join(AssetsFolder, 'Banner.png')).resize((500, 250))
        Banner = ImageCanvas(self, imgBanner)
        Banner.pack(padx=DefaultPad, pady=DefaultPad)

        WelcomeTitle = BigLabel(self, text='Welcome Back!')
        WelcomeTitle.pack(padx=DefaultPad, pady=DefaultPad)

        self.elements = [Banner, WelcomeTitle]


class AboutPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller, basic_name='About')

        TextFrame = RegularFrame(self)
        TextFrame.pack(padx=DefaultPad, pady=DefaultPad)

        ToolSetLabel = BigLabel(TextFrame, text='FortniteToolSet')
        ToolSetLabel.grid(row=0, column=0, padx=DefaultPad / 2)

        ListForTextLabel = ["Made By RealA10N. For personal use only! (;",
                            "Assets the not mentioned below created by me.",
                            "Some icons in the program are made by Lucy G from Flaticon"]

        TextLabel = RegularLabel(TextFrame, text=LinesListToString(ListForTextLabel))
        TextLabel.grid(row=1, column=0)

        # Icon pack: https://www.flaticon.com/packs/free-basic-ui-elements

        self.elements = [TextFrame, ToolSetLabel, TextLabel]


class AppearanceSettingsPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller, basic_name='Appearance')

        CurRow = 0
        for column_num in range(2):  # range(2) -> (0, 1)
            self.grid_columnconfigure(column_num, weight=1)

        Title = BigLabel(self, text='Appearance')
        Title.grid(padx=DefaultPad, pady=DefaultPad, row=CurRow, columnspan=2, sticky='n')
        CurRow += 1

        ColorPalette = self.controller.SettingsContainer.GetAppearanceContainer()
        self.SetColorPalette(ColorPalette)

        ColorElementsInfo = {'Background': {'Name': 'Background Color', 'Desc': 'Color for the background of the program.', 'StartingColor': ColorPalette.GetBackgroundColor()},
                             'Opposite': {'Name': 'Background Opposite Color', 'Desc': 'Color for items on the background, like text.', 'StartingColor': ColorPalette.GetBackgroundOppositeColor()},
                             'Trailing': {'Name': 'Trailing Color', 'Desc': 'Color for elements like basic buttons, basic text fields, etc.', 'StartingColor': ColorPalette.GetTrailingColor()},
                             'Different': {'Name': 'Different Color', 'Desc': 'Color with your personality! used in diffrent menus and special elements.', 'StartingColor': ColorPalette.GetDiffrentColor()},
                             'Special': {'Name': 'Special Color', 'Desc': "Completly diffrent. for special features like 'Save' buttons, etc.", 'StartingColor': ColorPalette.GetSpecialColor()},
                             }

        self.ColorElements = {}
        for Element, InfoDict in ColorElementsInfo.items():
            ElementObj = AppearanceColorLine(
                self, name=InfoDict['Name'], desc=InfoDict['Desc'], color=InfoDict['StartingColor'], grid_row=CurRow)
            CurRow += 1
            self.ColorElements[Element] = ElementObj

        SeparateLine = RegularLongLine(self)
        SeparateLine.grid(row=CurRow, columnspan=2, padx=DefaultPad, pady=DefaultPad)
        CurRow += 1

        self.FontLine = AppearanceEntryLine(
            self, 'Font', 'Select the program default font. Make sure the font is installed!', ColorPalette.GetFont(), grid_row=CurRow)
        CurRow += 1

        self.FontSizeLine = AppearanceSpinboxLine(
            self, 'Font Size', 'The size of the regular text. Other text will adapt to this setting.', ColorPalette.GetFontSize(), 10, 20, grid_row=CurRow)
        CurRow += 1

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

        self.elements = [Title, SeparateLine, self.FontLine, self.FontSizeLine, BottomButtonsFrame, SaveButton, BackDefaultbutton] + \
            AllColorElements

    def SetColorPalette(self, ColorPalette):
        self.controller.SettingsContainer.SetAppearanceContainer(ColorPalette)
        self.controller.SetAppearance(ColorPalette)

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
            self.FontLine.SetValue(NewColorPalette.GetFont())
            self.FontSizeLine.SetValue(NewColorPalette.GetFontSize())

    def SaveChanges(self):
        SavedChangesValue = []
        for Name, Element in self.ColorElements.items():
            SavedChangesValue.append(Element.SaveChanges())
        NewColorPalette = AppearanceSettingsContainer(
            *SavedChangesValue, Font=self.FontLine.GetValue(), RegularFontSize=self.FontSizeLine.GetValue())
        self.SetColorPalette(NewColorPalette)



# # # # # # # # # # # # # #
# G U I   E L E M E N T S #
# # # # # # # # # # # # # #

class DefaultCanvas(tk.Canvas):

    def SetAppearance(self, Container):
        pass


class ImageCanvas(DefaultCanvas):

    def __init__(self, master, pilImg, *args, **kwargs):

        self.pilImg = pilImg
        self.tkImg = ImageTk.PhotoImage(self.pilImg)
        width, height = pilImg.size

        tk.Canvas.__init__(self, master, highlightthickness=0,
                           height=height, width=width, *args, **kwargs)

        self.create_image(0, 0, image=self.tkImg, anchor='nw')

    def SetAppearance(self, Container):
        self.config(background=Container.GetBackgroundColor())


class LineCanvas(DefaultCanvas):

    def __init__(self, master, SizeX, SizeY, *args, **kwargs):
        DefaultCanvas.__init__(self, master, width=SizeX, height=SizeY,
                               highlightthickness=0, *args, **kwargs)

    def SetAppearance(self, Container):
        pass


class HorizontalLine(LineCanvas):

    def __init__(self, master, length):
        LineCanvas.__init__(self, master, SizeX=length, SizeY=2)


class RegularShortLine(HorizontalLine):

    def __init__(self, master):
        HorizontalLine.__init__(self, master, 150)

    def SetAppearance(self, Container):
        self.config(background=Container.GetDiffrentColor())


class RegularLongLine(HorizontalLine):

    def __init__(self, master):
        HorizontalLine.__init__(self, master, 300)

    def SetAppearance(self, Container):
        self.config(background=Container.GetDiffrentColor())


class SpecialShortLine(HorizontalLine):

    def __init__(self, master):
        HorizontalLine.__init__(self, master, 150)

    def SetAppearance(self, Container):
        self.config(background=Container.GetSpecialColor())


class SpecialLongLine(HorizontalLine):

    def __init__(self, master):
        HorizontalLine.__init__(self, master, 300)

    def SetAppearance(self, Container):
        self.config(background=Container.GetSpecialColor())


class DefaultLabel(tk.Label):

    def SetAppearance(self, Container):
        pass


class BigLabel(DefaultLabel):

    def SetAppearance(self, Container):
        self.config(background=Container.GetBackgroundColor(),
                    foreground=Container.GetSpecialColor(),
                    font=Container.GetBigFont())


class RegularLabel(DefaultLabel):

    def SetAppearance(self, Container):
        self.config(background=Container.GetBackgroundColor(),
                    foreground=Container.GetDiffrentColor(),
                    font=Container.GetRegularFont())


class RegularDarkLabel(RegularLabel):

    def SetAppearance(self, Container):
        self.config(background=Container.GetDarkColor(),
                    foreground=Container.GetLightColor(),
                    font=Container.GetRegularFont())


class RegularLightLabel(RegularLabel):

    def SetAppearance(self, Container):
        self.config(background=Container.GetLightColor(),
                    foreground=Container.GetDarkColor(),
                    font=Container.GetRegularFont())


class SpecialLightLabel(DefaultLabel):

    def SetAppearance(self, Container):
        self.config(background=Container.GetLightColor(),
                    foreground=Container.GetSpecialColor(),
                    font=Container.GetRegularFont())


class SpecialDarkLabel(DefaultLabel):

    def SetAppearance(self, Container):
        self.config(background=Container.GetDarkColor(),
                    foreground=Container.GetSpecialColor(),
                    font=Container.GetRegularFont())


class SmallLabel(DefaultLabel):

    def SetAppearance(self, Container):
        self.config(background=Container.GetBackgroundColor(),
                    foreground=Container.GetDarkColor(),
                    font=Container.GetSmallFont())


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

    def SetAppearance(self, Container):
        pass


class RegularEntry(DefaultEntry):

    def __init__(self, master, *args, **kwargs):

        DefaultEntry.__init__(self, master,
                              relief=tk.FLAT,  # style of the entry
                              bd=2,  # size of border
                              width=15,
                              *args, **kwargs)

    def SetAppearance(self, Container):
        self.config(background=Container.GetTrailingColor(),
                    foreground=Container.GetBackgroundOppositeColor(),  # color of font
                    selectbackground=Container.GetDarkColor(),  # background color when text selected
                    font=Container.GetRegularFont())  # font


class RegularLongEntry(RegularEntry):

    def __init__(self, master, *args, **kwargs):
        DefaultEntry.__init__(self, master,
                              relief=tk.FLAT,  # style of the entry
                              bd=2,  # size of border
                              *args, **kwargs)


class DefaultButton(tk.Button):

    def SetAppearance(self, Container):
        pass


class RegularButton(DefaultButton):

    def __init__(self, master, *args, **kwargs):

        DefaultButton.__init__(self, master,
                               # button
                               bd=2,  # size of border

                               # font
                               justify=tk.CENTER,  # center all the text lines
                               relief='ridge',
                               *args, **kwargs)

    def SetAppearance(self, Container):
        self.config(background=Container.GetTrailingColor(),  # regular color
                    activebackground=Container.GetDarkColor(),  # while pressed color
                    foreground=Container.GetBackgroundOppositeColor(),  # regular color
                    activeforeground=Container.GetBackgroundOppositeColor(),  # while pressed color
                    font=Container.GetRegularFont())  # font


class SmallButton(RegularButton):

    def __init__(self, master, *args, **kwargs):

        DefaultButton.__init__(self, master,
                               # button
                               bd=0,  # size of border

                               # font
                               justify=tk.CENTER,  # center all the text lines
                               *args, **kwargs)

    def SetAppearance(self, Container):
        self.config(background=Container.GetTrailingColor(),  # regular color
                    activebackground=Container.GetDarkColor(),  # while pressed color
                    foreground=Container.GetBackgroundOppositeColor(),  # regular color
                    activeforeground=Container.GetBackgroundOppositeColor(),  # while pressed color
                    font=Container.GetSmallFont())  # font


class SpecialButton(RegularButton):

    def SetAppearance(self, Container):
        self.config(background=Container.GetSpecialColor(),  # regular color
                    activebackground=Container.GetDarkColor(),  # while pressed color
                    foreground=Container.GetBackgroundOppositeColor(),  # regular color
                    activeforeground=Container.GetBackgroundOppositeColor(),  # while pressed color
                    font=Container.GetRegularFont())  # font


class DefaultRadiobutton(tk.Radiobutton):

    def SetAppearance(self, Container):
        pass


class RegularRadiobutton(DefaultRadiobutton):

    def __init__(self, master, *args, **kwargs):

        DefaultRadiobutton.__init__(self, master,
                                    borderwidth=0,  # size of border
                                    *args, **kwargs)

    def SetAppearance(self, Container):
        self.config(bg=Container.GetBackgroundColor(),  # background color
                    activebackground=Container.GetBackgroundColor(),  # while pressed color
                    selectcolor=Container.GetDarkColor(),
                    fg=Container.GetBackgroundOppositeColor(),  # text color
                    activeforeground=Container.GetBackgroundOppositeColor(),  # while pressed text color
                    font=Container.GetRegularFont())  # font


class DefaultSpinbox(tk.Spinbox):

    def SetAppearance(self, Container):
        pass


class RegularSpinbox(DefaultSpinbox):

    def __init__(self, master, *args, **kwargs):
        DefaultSpinbox.__init__(self, master,
                                bd=0,
                                width=3,
                                buttondownrelief='ridge',
                                buttonuprelief='ridge',
                                *args, **kwargs)

    def SetAppearance(self, Container):
        self.config(background=Container.GetTrailingColor(),
                    activebackground=Container.GetTrailingColor(),
                    foreground=Container.GetBackgroundOppositeColor(),
                    buttonbackground=Container.GetTrailingColor(),
                    font=Container.GetRegularFont()
                    )


class DefaultCheckbutton(tk.Checkbutton):

    def SetAppearance(self, Container):
        pass

    def SetValue(self, value):
        if value:
            self.select()
        elif value is False:
            self.deselect()


class RegularCheckbutton(DefaultCheckbutton):

    def SetAppearance(self, Container):
        self.config(bg=Container.GetBackgroundColor(),  # background color
                    activebackground=Container.GetBackgroundColor(),  # while pressed color
                    selectcolor=Container.GetDarkColor(),
                    fg=Container.GetBackgroundOppositeColor(),  # text color
                    activeforeground=Container.GetBackgroundOppositeColor(),  # while pressed text color
                    font=Container.GetRegularFont())  # font


# # # # # # # # # # # # # # # #
# C U S T O M   W I D G E T S #
# # # # # # # # # # # # # # # #


class SettingLine():

    def __init__(self, master, name, desc, grid_row):

        self.Label = NameDescFrame(master, name, desc)
        self.Label.grid(pady=DefaultPad / 2, padx=DefaultPad / 2, row=grid_row, column=0)

        self.elements = [self.Label]

    def SetAppearance(self, Container):
        for element in self.elements:
            element.SetAppearance(Container)

    def GridSettingElement(self, element, row):
        element.grid(pady=DefaultPad / 2, padx=DefaultPad / 2, row=row, column=1)


class AppearanceColorLine(SettingLine):

    def __init__(self, master, name, desc, grid_row, color):

        SettingLine.__init__(self, master, name, desc, grid_row)
        self.ColorPicker = AppearanceColorPicker(master, color, name)
        self.GridSettingElement(self.ColorPicker, grid_row)

        self.elements = self.elements + [self.ColorPicker]

    def ChangeColor(self, color):
        self.ColorPicker.ChangeColor(color)

    def SaveChanges(self):
        return self.ColorPicker.SaveChanges()


class AppearanceEntryLine(SettingLine):

    def __init__(self, master, name, desc, text, grid_row):
        SettingLine.__init__(self, master, name, desc, grid_row)

        self.EntryStr = tk.StringVar()
        self.EntryStr.set(text)

        self.Entry = RegularEntry(master, textvariable=self.EntryStr)
        self.GridSettingElement(self.Entry, grid_row)

        self.elements = self.elements + [self.Entry]

    def GetValue(self):
        return self.EntryStr.get()

    def SetValue(self, value):
        self.EntryStr.set(value)


class AppearanceSpinboxLine(SettingLine):

    def __init__(self, master, name, desc, value, min, max, grid_row):
        SettingLine.__init__(self, master, name, desc, grid_row)

        self.Value = tk.StringVar()
        self.Value.set(value)

        self.Spinbox = RegularSpinbox(master, from_=min, to=max, textvariable=self.Value)
        self.GridSettingElement(self.Spinbox, grid_row)

        self.elements = self.elements + [self.Spinbox]

    def GetValue(self):
        return int(self.Value.get())

    def SetValue(self, value):
        self.Value.set(str(value))


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

    def __init__(self, master, name, desc, *args, **kwargs):

        RegularFrame.__init__(self, master, *args, **kwargs)

        NameLabel = RegularLabel(self, text=name)
        NameLabel.grid(row=0, column=0)
        DescLabel = SmallLabel(self, text=desc, wraplength=175)
        DescLabel.grid(row=1, column=0, padx=DefaultPad)

        self.elements = [NameLabel, DescLabel]

    def SetAppearance(self, Container):
        RegularFrame.SetAppearance(self, Container)
        for element in self.elements:
            element.SetAppearance(Container)

# # # # # # # # # # # # # # # # # #
# P U B L I C   F U N C T I O N S #
# # # # # # # # # # # # # # # # # #


def LinesListToString(list):
    # takes list of lines, and converts it to one string with '\n' between lines
    finalstr = ""
    for line in list:
        finalstr = finalstr + line + "\n"
    return finalstr[:-1]


def SendToClipboard(type, date):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(type, date)
    win32clipboard.CloseClipboard()


def SendStringToClipboard(string):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, string)
    win32clipboard.CloseClipboard()


def SendImageToClipboard(image):
    output = BytesIO()
    image.save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    SendToClipboard(win32clipboard.CF_DIB, data)


# # # # # # # # # # # # #
# A P I   C L A S S E S #
# # # # # # # # # # # # #

class DefaultAPI():

    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.__ApiJson = None

    def GetJsonDate(self):
        if self.__ApiJson is None:
            self.__ApiJson = self.__GenerateJsonData()
        return self.__ApiJson

    def __GenerateJsonData(self):
        request = requests.request("GET", self.url, headers=self.headers)
        return request.json()


class FortnitePublicAPI(DefaultAPI):

    def __init__(self):

        DefaultAPI.__init__(self,
                            url='https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game',
                            headers={})
        self.__BattleRoyaleNewsItems = None
        self.__SaveTheWorldNewsItems = None
        self.__PlaylistItems = None

    def __GenerateItems(self, dicts_list, item_class):
        ItemsDict = []
        for dict in dicts_list:
            Item = item_class(dict)
            ItemsDict.append(Item)
        return ItemsDict

    def GetBattleRoyaleNews(self):
        return self.GetJsonDate()['battleroyalenews']['news']['messages']

    def GetBattleRoyaleNewsItems(self):
        if self.__BattleRoyaleNewsItems is None:
            self.__BattleRoyaleNewsItems = self.__GenerateItems(
                self.GetBattleRoyaleNews(), FortniteNews)
        return self.__BattleRoyaleNewsItems

    def GetSaveTheWorldNews(self):
        return self.GetJsonDate()['savetheworldnews']['news']['messages']

    def GetSaveTheWorldNewsItems(self):
        if self.__SaveTheWorldNewsItems is None:
            self.__SaveTheWorldNewsItems = self.__GenerateItems(
                self.GetSaveTheWorldNews(), FortniteNews)
        return self.__SaveTheWorldNewsItems

    def GetPlayList(self):
        return self.GetJsonDate()['playlistimages']['playlistimages']['images']

    def GetPlayListItems(self):
        if self.__PlaylistItems is None:
            self.__PlaylistItems = self.__GenerateItems(self.GetPlayList, FortnitePlaylist)
        return self.__PlaylistItems


# # # # # # # # # # # # # #
# A P I   E L E M E N T S #
# # # # # # # # # # # # # #

class FortniteAPIelement():

    def __init__(self, Dict):
        self.Dict = Dict

    def GetDict(self):
        return self.Dict


class FortniteNews(FortniteAPIelement):

    # local variables
    __ImagePIL = None

    def GetImageUrl(self):
        return self.GetDict()['image']

    def __GenerateImagePIL(self):
        Request = requests.get(self.GetImageUrl())
        Bytes = BytesIO(Request.content)
        return Image.open(Bytes).convert("RGBA")

    def GetImagePIL(self):
        if self.__ImagePIL is None:
            self.__ImagePIL = self.__GenerateImagePIL()
        return self.__ImagePIL

    def GetIfHidden(self):
        if self.GetAdspace == 'NEW!':
            return True
        return bool(self.GetDict()['hidden'])

    def GetType(self):
        return self.GetDict()['_type']

    def GetAdspace(self):
        if 'adspace' in self.GetDict():
            if self.GetDict()['adspace'] != '':
                return self.GetDict()['adspace']
        return None  # else...

    def GetTitle(self):
        return self.GetDict()['title']

    def GetBody(self):
        return self.GetDict()['body']

    def GetIfSpotlight(self):
        return bool(self.GetDict()['spotlight'])


class FortnitePlaylist(FortniteAPIelement):

    def GetImageUrl(self):
        return self.GetDict()['image']

    def GetType(self):
        return self.GetDict()['_type']

    def GetName(self):
        return self.GetDict()['playlistname']


# # # # # # # # # # # # # #
# M A I N   P R O G R A M #
# # # # # # # # # # # # # #

if __name__ == '__main__':
    root = ProgramGUI()
    root.mainloop()
