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

        self.__GenerateDarkColor()  # For smaller and less importent text
        self.__GenerateLightColor()  # For text that pops up

    def __GenerateDarkColor(self):
        self.DarkColor = self.DefaultColor.NewChangeColorLightning(0.6)

    def __GenerateLightColor(self):
        self.LightColor = self.DefaultColor.NewChangeColorLightning(1.4)

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

    def GetDefaultColor(self):
        return self.DefaultColor.get_hex_l()

    def SetDefaultColor(self, hex_color):
        self.DefaultColor = MyColor(hex_color)
        self.__GenerateDarkColor()
        self.__GenerateLightColor()

    def GetDiffrentColor(self):
        return self.DiffrentColor.get_hex_l()

    def SetDiffrentColor(self, hex_color):
        self.DiffrentColor = MyColor(hex_color)

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

        self.pages = [HomePage, AppearanceSettingsPage, AboutPage]  # all the pages list
        self.frames = {}
        self.LoadAllPages(parent=container, controller=self)
        self.CurrentPage = None
        self.ShowPage(HomePage)

        self.SetColors(DefaultColorPalette())

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
        # all icons are 64x64

        self.elements = [TextFrame, ToolSetLabel, TextLabel]

    def ShowMe(self):
        self.controller.SetTitle('About')


class AppearanceSettingsPage(DefaultPage):

    def __init__(self, parent, controller):
        DefaultPage.__init__(self, parent, controller)

        for column_num in range(2):  # range(2) -> (0, 1)
            self.grid_columnconfigure(column_num, weight=1)

        Title = BigLabel(self, text='Appearance')
        Title.grid(padx=DefaultPad, pady=DefaultPad, row=1, columnspan=2, sticky='n')

        self.SetColorPalette(DefaultColorPalette())

        # Background color
        BackgroundColorLabel = NameDescFrame(
            self, "Background Color", "Color for the background of the program.")
        BackgroundColorLabel.grid(pady=DefaultPad, row=2, column=0)
        self.BackgroundColorFrame = AppearanceColorPicker(
            self, self.ColorPalette.GetBackgroundColor())
        self.BackgroundColorFrame.grid(row=2, column=1)

        # Backgroud opposite color
        OppositeColorLabel = NameDescFrame(
            self, "Background Opposite Color", "Color for items on the background, like text.")
        OppositeColorLabel.grid(pady=DefaultPad, row=3, column=0)
        self.OppositeColorFrame = AppearanceColorPicker(
            self, self.ColorPalette.GetBackgroundOppositeColor())
        self.OppositeColorFrame.grid(row=3, column=1)

        # Trailing color
        TrailingColorLabel = NameDescFrame(
            self, "Trailing Color", "Color for elements like basic buttons, basic text fields, etc.")
        TrailingColorLabel.grid(pady=DefaultPad, row=4, column=0)
        self.TrailingColorFrame = AppearanceColorPicker(self, self.ColorPalette.GetTrailingColor())
        self.TrailingColorFrame.grid(row=4, column=1)

        # Diffrent color
        DiffrentColorLabel = NameDescFrame(
            self, "Diffrent Color", "Color with your personality! used in diffrent menus and special elements.")
        DiffrentColorLabel.grid(pady=DefaultPad, row=5, column=0)
        self.DiffrentColorFrame = AppearanceColorPicker(self, self.ColorPalette.GetDefaultColor())
        self.DiffrentColorFrame.grid(row=5, column=1)

        # Special color
        SpecialColorLabel = NameDescFrame(
            self, "Special Color", "Completly diffrent. for special feuters like 'Save' buttons, etc.")
        SpecialColorLabel.grid(pady=DefaultPad, row=6, column=0)
        self.SpecialColorFrame = AppearanceColorPicker(self, self.ColorPalette.GetDiffrentColor())
        self.SpecialColorFrame.grid(row=6, column=1)

        BottomButtonsFrame = RegularFrame(self)
        BottomButtonsFrame.grid(columnspan=2, padx=DefaultPad, pady=DefaultPad)

        SaveButton = SpecialButton(BottomButtonsFrame, text='Save changes',
                                   command=lambda: self.SaveChanges())
        SaveButton.grid(padx=DefaultPad / 2, row=0, column=0, sticky='e')

        BackDefaultbutton = RegularButton(BottomButtonsFrame, text='Back To Default')
        BackDefaultbutton.grid(padx=DefaultPad / 2, row=0, column=1, sticky='w')

        self.elements = [Title, BackgroundColorLabel, self.BackgroundColorFrame,
                         OppositeColorLabel, self.OppositeColorFrame,
                         TrailingColorLabel, self.TrailingColorFrame,
                         DiffrentColorLabel, self.DiffrentColorFrame,
                         SpecialColorLabel, self.SpecialColorFrame,
                         BottomButtonsFrame, SaveButton, BackDefaultbutton]

    def SetColorPalette(self, ColorPalette):
        self.ColorPalette = ColorPalette
        self.controller.SetColors(ColorPalette)

    def SaveChanges(self):
        NewColorPalette = MyColorPalette(
            BackgroundColor=self.BackgroundColorFrame.SaveChanges(),
            BackgroudOppositeColor=self.OppositeColorFrame.SaveChanges(),
            TrailingColor=self.TrailingColorFrame.SaveChanges(),
            DefaultColor=self.DiffrentColorFrame.SaveChanges(),
            DiffrentColor=self.SpecialColorFrame.SaveChanges(),
        )
        self.SetColorPalette(NewColorPalette)

    def ShowMe(self):
        self.controller.SetTitle('Appearance')


class AppearanceColorPicker(RegularFrame):

    def __init__(self, master, starting_value, *args, **kwargs):
        RegularFrame.__init__(self, master, *args, **kwargs)

        self.DefaultValue = starting_value
        self.NewValue = starting_value

        self.ColorLabel = ColorLabel(self)
        self.UpdateColorLabel()
        self.ColorLabel.grid(row=0, column=0)

        ChangeButton = RegularButton(
            self, text='Change', command=lambda: self.ChangeColor())
        ChangeButton.grid(row=0, column=1)

        ResetButton = RegularButton(self, text='Restore', command=lambda: self.RestoreColor())
        ResetButton.grid(row=0, column=2)

        self.elements = [ChangeButton, ResetButton]

    def UpdateColorLabel(self):
        self.ColorLabel.config(bg=self.NewValue)

    def ChangeColor(self):
        color_input = colorchooser.askcolor()[1]
        if color_input is not None:
            self.NewValue = color_input
            self.UpdateColorLabel()

    def RestoreColor(self):
        self.NewValue = self.DefaultValue
        self.UpdateColorLabel()

    def SaveChanges(self):
        self.DefaultValue = self.NewValue
        return self.NewValue


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


if __name__ == '__main__':
    root = ProgramGUI()
    root.mainloop()
