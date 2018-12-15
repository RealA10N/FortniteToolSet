import requests  # TO GET API
from PIL import Image, ImageDraw, ImageFont  # TO EDIT IMAGES
from io import BytesIO  # TO LOAD IMAGE FROM API
import sys
import os
import subprocess

class NewsInfo:

    def __init__(self, request_list, news_num=0):
        self.request_list = request_list
        self.image = None
        self.title = ''
        self.body = ''
        self.time = ''
        self.get_news(news_num)

    def get_news(self, news_num):
        original_news_dictionary = self.request_list.json()['entries'][news_num]
        try:
            self.image = Image.open(BytesIO(requests.get(original_news_dictionary['image']).content))
        except OSError:
            self.image = Image.open(assets_folder_path + "\\NewsErrorImage.png")
        self.title = original_news_dictionary['title']
        self.body = original_news_dictionary['body']
        self.time = original_news_dictionary['time']


def get_api_request(request_url, request_headers):
    return requests.request("GET", request_url, headers=request_headers)


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


##########################
#    GENERATING IMAGE    #
##########################

assets_folder_path = os.getcwd() + '\\News Generator Assets'
final_image_folder = os.getcwd() + '\\News Final Images'
api_url = 'https://api.gamingsdk.com/client/game/fortnite/scope/news/type/br/language/en/'
api_headers = {'Authorization': 'c738e77d4212930fd8a1721fd9511c15'}
print("| Progress | Downloading \"News\" from API.")
api_list = get_api_request(api_url, api_headers)
print("| Progress | Info downloaded and saved successfully.")
if len(sys.argv) == 1:
    wanted_index = input("|  INPUT   | Please enter the index of the news you want to generate (0 for latest): ")
else:
    wanted_index = int(sys.argv[1])
wanted_news_info = NewsInfo(api_list, int(wanted_index))

# SETTING UP CANVAS
news_canvas = Image.open(assets_folder_path + "\\FortniteNewsStoryTemplate.png")
new_card_canvas = Image.open(assets_folder_path + "\\FortniteNewsStoryTemplate onlycard.png")
print("| Progress | Background image drawn successfully.")

# PASTING IMAGE ON BACKGROUND IMAGE
wanted_image = wanted_news_info.image.resize((900, 450))  # RESIZE IMAGE TO 900 BY 450
news_canvas.paste(wanted_image, (50, 638))
news_canvas.paste(new_card_canvas, (0, 0), new_card_canvas)
news_draw_canvas = ImageDraw.Draw(news_canvas)
print("| Progress | News image processed successfully.")

# DRAW TITLE
title_font = ImageFont.truetype("BurbankBigRegular-Black.otf", 75)
title_color = "#5e0000"
title_starting_height = 1110
title_starting_wight = 70
draw_left_text_lines(
    news_draw_canvas,
    [wanted_news_info.title],
    title_font,
    title_color,
    title_starting_height,
    title_starting_wight)
print("| Progress | Title drawn successfully.")


# DRAW BODY AND SHADOW
news_body_lines = word_list_to_line_list(string_to_word_list(wanted_news_info.body), 48)
body_font = ImageFont.truetype("BurbankBigCondensed-Bold.otf", 55)
body_color = '#323232'
body_starting_height = 1180
body_starting_width = 70
body_jumps_height = 42
draw_left_text_lines(
    news_draw_canvas,
    news_body_lines,
    body_font,
    body_color,
    body_starting_height,
    body_starting_width,
    body_jumps_height)


print("| Progress | Body drawn successfully.")
final_image_location = final_image_folder + "\\News - " + wanted_news_info.title + ".png"
news_canvas.save(final_image_location)
open_command = r'explorer /select,"' + final_image_location + r'"'
subprocess.Popen(open_command)
news_canvas.show()
