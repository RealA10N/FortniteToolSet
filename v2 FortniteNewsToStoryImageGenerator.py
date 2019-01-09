from ConsoleFunctions import *
from FortniteApiCommands import *
import os
from PIL import *
import subprocess


class FortniteDatabase:

    def __init__(self, database):
        self.__database = database
        self.__news_dict = None
        self.__news_list = []

    def __generate_news_dict(self):
        self.__news_dict = self.__database.find_value_by_key(['battleroyalenews', 'messages'])[0]

    def __generate_news_list(self):
        if self.__news_dict is None:
            self.__generate_news_dict()
        for news in self.__news_dict:
            self.__news_list.append(NewsInfo(news))

    def get_news_list(self):
        if self.__news_list == []:
            self.__generate_news_list()
        return self.__news_list

    def get_news_dict(self):
        if self.__news_dict is None:
            self.__generate_news_dict()
        return self.__news_dict


class NewsFunctions:

    def __init__(self, news):
        self.news = news

    def generate_story_image(self, canvas):
        wip_canvas = self.__paste_news_image(canvas, pasting_position=(50, 638), news_image_size=(900, 450))
        wip_drawing_canvas = ImageDraw.Draw(wip_canvas)
        self.__draw_text(wip_drawing_canvas)
        self.__paste_card_image(wip_canvas)
        return wip_canvas

    def __paste_news_image(self, canvas, pasting_position, news_image_size=None):
        wip_news_image = self.news.get_image()
        if news_image_size is not None:
            wip_news_image = wip_news_image.resize(news_image_size)
        canvas.paste(wip_news_image, pasting_position)
        return canvas

    def __draw_text(self, drawing_canvas):
        title_font = ImageFont.truetype("BurbankBigRegular-Black.otf", 75)
        title_color = "#5e0000"
        title_starting_height = 1110
        title_starting_wight = 70
        draw_left_text_lines(
            drawing_canvas,
            [self.news.get_title()],
            title_font,
            title_color,
            title_starting_height,
            title_starting_wight)

        # DRAW BODY AND SHADOW
        news_body_lines = word_list_to_line_list(string_to_word_list(self.news.get_body_text()), 48)
        body_font = ImageFont.truetype("BurbankBigCondensed-Bold.otf", 55)
        body_color = '#323232'
        body_starting_height = 1180
        body_starting_width = 70
        body_jumps_height = 42
        draw_left_text_lines(
            drawing_canvas,
            news_body_lines,
            body_font,
            body_color,
            body_starting_height,
            body_starting_width,
            body_jumps_height)

    def __paste_card_image(self, canvas):
        if self.news.get_ad_space() is None:
            return canvas

        ad_space_image_path = assets_folder_path + "\\FortniteNewsStory " + self.news.get_ad_space() + ".png"

        try:
            ad_space_image = Image.open(ad_space_image_path).convert("RGBA")
            return canvas.paste(ad_space_image, (0, 0), ad_space_image)
        except FileNotFoundError:
            return canvas

def get_news_print_title(news):
    if news.get_ad_space() is None:
        return news.get_title() + ' - ' + news.get_body_text()
    return '*' + news.get_ad_space() + '* ' + news.get_title() + ' - ' + news.get_body_text()


def draw_left_text_lines(
        canvas,
        lines_list,
        lines_font,
        lines_color,
        starting_drawing_hight,
        starting_drawing_width,
        jump_between_lines=0):
    for line_num in range(len(lines_list)):
        line_height = starting_drawing_hight + line_num * jump_between_lines
        line_width = starting_drawing_width
        canvas.text((line_width, line_height), lines_list[line_num], font=lines_font,
                    fill=lines_color)


def word_list_to_line_list(words_list, max_line_ch):
    lines_list = []
    current_line = ''
    approved_line = ''
    for word in words_list:
        current_line = current_line + word + ' '
        if len(current_line) < max_line_ch:
            approved_line = current_line
        else:
            approved_line = approved_line[0:-1]
            lines_list.append(approved_line)
            current_line = word + ' '
            approved_line = word + ' '
    approved_line = approved_line[0:-1]
    lines_list.append(approved_line)
    return lines_list


def string_to_word_list(input_string):
    current_word = ''
    words_list = []
    for i in input_string:
        if i == ' ':
            words_list.append(current_word)
            current_word = ''
        else:
            current_word = current_word + i
    if input_string[-1] != ' ':
        words_list.append(current_word)
    return words_list


console = ConsolePrintFunctions()
console.print_one_line_title("Fortnite News Generator. // Created by @RealA10N", "single heavy square")
print()  # to go one line down.

api = \
    JsonReader('https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game')

assets_folder_path = os.getcwd() + '\\News Generator Assets'
final_image_folder = os.getcwd() + '\\News Final Images'

# makes "News Final Images" folder if it is not found.
if not os.path.exists(final_image_folder):
    os.makedirs(final_image_folder)

database = Database(api.get_json_data())
fortnite_database = FortniteDatabase(database)

select_index_news_list = []
for news in fortnite_database.get_news_list():
    select_index_news_list.append(get_news_print_title(news))

wanted_index = console.select_by_index(select_index_news_list, "Please select the image that you want to make by index:")
wanted_news = fortnite_database.get_news_list()[int(wanted_index)]
print()

# SETTING UP CANVAS
news_canvas = Image.open(assets_folder_path + "\\FortniteNewsStoryTemplate.png")
new_card_canvas = Image.open(assets_folder_path + "\\FortniteNewsStoryTemplate onlycard.png")
console.print_replaceable_line("Background image drawn successfully.")

newsfunctions = NewsFunctions(wanted_news)
newsfunctions.generate_story_image(news_canvas)
console.print_replaceable_line("Body drawn successfully.")

final_image_name = "Generated News Image - " + wanted_news.get_title() + ".png"
final_image_location = final_image_folder + "\\" + final_image_name
news_canvas.save(final_image_location)
os.startfile(final_image_location)

console.print_replaceable_line("Final Image saved! Press ENTER to exit.")
input()
