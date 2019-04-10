from ConsoleFunctions import ConsolePrintFunctions
from FortniteApiCommands import FortniteNewsAPI
import os
from PIL import Image, ImageDraw, ImageFont


class NewsFunctions:

    def __init__(self, news, assets_folder_path):
        self.news = news
        self.assets_folder_path = assets_folder_path

    def generate_story_image(self, canvas):
        wip_canvas = self.__paste_news_image(
            canvas, pasting_position=(50, 638), news_image_size=(900, 450))
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

        ad_space_image_path = self.assets_folder_path + "\\FortniteNewsStory " + self.news.get_ad_space() + \
            ".png"

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


# if __name__ == "__main__" will print regular text.
# if __name__ != "__main__" will print text with the script name in front.
def get_print_text(text):
    if __name__ == "__main__":
        return text
    else:
        return __name__ + ' | ' + text


def craft_news_image(news, assets_folder, console=ConsolePrintFunctions()):

    # setting up canvas
    news_canvas = Image.open(assets_folder + "\\FortniteNewsStoryTemplate.png")
    console.print_replaceable_line(get_print_text(
        "Drawing news image for '" + news.get_title() + "'!"))

    newsfunctions = NewsFunctions(news, assets_folder)
    newsfunctions.generate_story_image(news_canvas)
    console.print_replaceable_line(get_print_text(
        "Generated '" + news.get_title() + "' news image successfully!\n"))
    return news_canvas


def give_proper_file_name(file_name):

    invalid_char_list = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_char_list:
        file_name = file_name.replace(char, '')
    return file_name


def generate_all_news(saving_p, assets_p, api=FortniteNewsAPI()):
    for news in api.get_news_list():
        final_image_name = "News Image - " + give_proper_file_name(news.get_title()) + ".png"
        final_image_path = os.path.join(saving_p, final_image_name)
        craft_news_image(news, assets_p).save(final_image_path)
        if not args.quiet:
            os.startfile(final_image_path)


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description='Generate an image (one or more) of the current Fortnite battle royale news feed. Created by RealA10N (;')
    parser.add_argument('-sp', '--saving_path', type=str, metavar='',
                        help='Changes the default saving path of the generated news images')
    parser.add_argument('-i', '--news_index', type=int, metavar='',
                        help='The index of the final generated news image')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Generate all the avalible news images')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help="Run quietly, without fancy prints and opening the result image(s)")
    return parser.parse_args()


if __name__ == "__main__":

    args = get_args()

    console = ConsolePrintFunctions()
    console.start_script_clock()
    if not args.quiet:
        console.print_one_line_title(
            "Fortnite News Generator. // Created by @RealA10N", "single heavy square")
        print()  # to go down one line
    print(get_print_text('Downloading \"News Info\" from API...'))

    assets_folder_path = os.getcwd() + '\\NewsGeneratorAssets'

    if args.saving_path is None:
        final_image_folder = os.path.join(os.getcwd(), 'NewsFinalImages')
    else:
        final_image_folder = args.saving_path

    # makes "NewsFinalImages" folder if it is not found.
    if not os.path.exists(final_image_folder):
        os.makedirs(final_image_folder)

    news_api = FortniteNewsAPI()
    if args.all:
        generate_all_news(final_image_folder, assets_folder_path, news_api)
        quit()

    select_index_news_list = []
    for news in news_api.get_news_list():
        select_index_news_list.append(get_news_print_title(news))

    if args.news_index is None:
        news_index = console.select_by_index(select_index_news_list,
                                             "Please select the image that you want to make by index:")
        print()  # to go down one line
        wanted_news = news_api.get_news_list()[int(news_index)]
    else:
        wanted_news = news_api.get_news_list()[args.news_index]

    final_image_name = "Generated News Image - " + \
        give_proper_file_name(wanted_news.get_title()) + ".png"
    final_image_location = final_image_folder + "\\" + final_image_name

    craft_news_image(wanted_news, assets_folder_path, console).save(final_image_location)
    if not args.quiet:
        os.startfile(final_image_location)
        console.print_replaceable_line(get_print_text("Final Image saved!        \n"))
        console.end_script_clock()
