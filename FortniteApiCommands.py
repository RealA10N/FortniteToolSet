import requests  # TO GET API
from PIL import Image, ImageDraw, ImageFont  # TO EDIT IMAGES
from io import BytesIO  # TO LOAD IMAGE FROM API
import os.path
from TxtFileManager import ValuesTxtFile


class FortniteItemInfo:

    def __init__(self, item_dict):
        self.item_dict = item_dict
        self.transparent_image = None
        self.image_already_saved = False
        self.featured_image = None
        self.featured_image_already_saved = False

    def get_itemid(self):
        pass

    def get_name(self):
        pass

    def get_cost(self):
        pass

    def get_type(self):
        pass

    def get_rarity(self):
        pass

    def get_if_featured(self):
        pass

    def get_if_featured_image(self):
        pass

    def get_transparent_image(self):
        pass

    def get_featured_image(self):
        pass


# input: the dictionary item form the api
# parses back: item info
class ShopInfo(FortniteItemInfo):

    def get_itemid(self):
        return self.item_dict['itemid']

    def get_name(self):
        return str(self.item_dict['name'])

    def get_cost(self):
        return str(self.item_dict['cost'])

    def get_type(self):
        return self.item_dict['item']['type']

    def get_rarity(self):
        return self.item_dict['item']['rarity']

    def get_if_featured(self):
        return bool(self.item_dict['featured'])

    def get_if_image_featured(self):
        if self.get_if_featured() and self.get_type() == 'outfit':
            try:
                self.get_featured_image()
                return True
            except OSError:
                return False
        else:
            return False

    def get_transparent_image(self):
        if not self.image_already_saved:
            self.transparent_image = self.__generate_transparent_image()
        return self.transparent_image

    def __generate_transparent_image(self):
        transparent_image = Image.open(BytesIO(requests.get(self.item_dict['item']['images']['transparent']).content)).resize(
            (512, 512)).convert("RGBA")
        self.image_already_saved = True
        return transparent_image

    def get_featured_image(self):
        if not self.featured_image_already_saved:
            self.featured_image = self.__generate_featured_image()
        return self.featured_image

    def __generate_featured_image(self):
        featured_image = Image.open(BytesIO(requests.get(
            self.item_dict['item']['images']['featured']['transparent']).content)).resize((1024, 1024)).convert("RGBA")
        self.featured_image_already_saved = True
        return featured_image


class UpcomingInfo(FortniteItemInfo):

    def get_itemid(self):
        return self.item_dict['id']

    def get_name(self):
        return str(self.item_dict['name'])

    def get_cost(self):
        return str(self.item_dict['price'])

    def get_type(self):
        return self.item_dict['type']

    def get_rarity(self):
        return self.item_dict['rarity']

    def get_if_featured(self):
        if self.item_dict['images']['featured'] == 'False':
            return False
        else: return True

    def get_if_image_featured(self):
        if self.get_if_featured() and self.get_type() == 'outfit':
            try:
                self.get_featured_image()
                return True
            except OSError:
                return False
        else:
            return False

    def get_transparent_image(self):
        if not self.image_already_saved:
            self.transparent_image = self.__generate_transparent_image()
        return self.transparent_image

    def __generate_transparent_image(self):
        transparent_image = Image.open(
            BytesIO(requests.get(self.item_dict['images']['icon']).content)).resize(
            (512, 512)).convert("RGBA")
        self.image_already_saved = True
        return transparent_image

    def get_featured_image(self):
        if not self.featured_image_already_saved:
            self.featured_image = self.__generate_featured_transparent_image()
        return self.featured_image

    def __generate_featured_transparent_image(self):
        featured_image = Image.open(BytesIO(requests.get(
            self.item_dict['images']['featured']).content)).resize((1024, 1024)).convert("RGBA")
        self.featured_image_already_saved = True
        return featured_image


# a class that will load all the needed assets and save them.
class Assets:

    def __init__(self):

        self.__failed_files = []
        self.__this_folder = os.getcwd()

    def load_item_assets(self):

        self.__assets_folder_path = os.path.join(self.__this_folder, 'ItemsAssets')
        self.__additional_assets_path = self.__assets_folder_path + "\\Additional files"
        self.__background_assets_path = self.__assets_folder_path + "\\Background Images"

        # load all images
        self.__pasting_image_resolution = (512, 512)
        self.__shadow_box_one_line = self.open_image(self.__additional_assets_path + '\\ItemShopShadowBoxOneLine.png')
        self.__shadow_box_two_lines = self.open_image(self.__additional_assets_path + '\\ItemShopShadowBoxTwoLines.png')
        self.__vbucks_image = self.open_image(self.__additional_assets_path + '\\icon_vbucks.png').resize((40, 40))
        self.__overlay_image = self.open_image(self.__additional_assets_path + '\\ItemShopOutlineBox_BottomOnly.png')
        self.__name_font = self.open_font("BurbankBigRegular-Black.otf", 60)
        self.__cost_font = self.open_font("BurbankBigRegular-Black.otf", 40)

        if len(self.__failed_files) > 0:
            self.raise_failed_error_string()

    def open_image(self, path):

        try:
            image = Image.open(path)
        except FileNotFoundError:
            file_name = os.path.basename(path)
            self.__failed_files.append(file_name)
            image = 'failed'
        return image

    def open_font(self, font_name, font_size):

        try:
            font = ImageFont.truetype(font_name, font_size)
        except OSError:
            self.__failed_files.append(font_name + '(size ' + font_size + ')')
            font = 'failed'
        return font

    def raise_failed_error_string(self):

        failed_files_string = ''
        for failed_file in self.__failed_files:
            failed_files_string = failed_files_string + failed_file + ', '
        failed_files_string = failed_files_string[:-2]  # remove last ', '

        input('''
ERROR | One or more assets file(s) not found:
''' + failed_files_string + '''
Please follow the "README.md" file instructions. Press any key to exit.''')
        quit()

    def get_item_assets_folder_path(self):
        return self.__assets_folder_path

    def get_item_additional_assets_path(self):
        return self.__additional_assets_path

    def get_item_background_assets_path(self):
        return self.__background_assets_path

    def get_item_pasting_image_resolution(self):
        return self.__pasting_image_resolution

    def get_item_shadow_image_one_line(self):
        return self.__shadow_box_one_line

    def get_item_shadow_image_two_lines(self):
        return self.__shadow_box_two_lines

    def get_item_vbucks_small_icon(self):
        return self.__vbucks_image

    def get_item_overlay_image(self):
        return self.__overlay_image

    def get_item_name_font(self):
        return self.__name_font

    def get_item_cost_font(self):
        return self.__cost_font


class DrawingInfo():

    assets = Assets()  # imports assets from "Assets" class
    assets.load_item_assets()

    def __init__(self):
        self.info_class = None
        self.__final_1on1_image = None
        self.__final_1on2_image = None

    def __build_rarity_path(self, size):
        temp_path = self.assets.get_item_background_assets_path()\
                    + '\\' + self.info_class.get_rarity() + ' ' + str(size[0]) + '_' + str(size[1]) + ' background.png'
        if os.path.isfile(temp_path):
            return temp_path
        else:
            return self.assets.get_item_background_assets_path()\
               + '\\' + "common" + ' ' + str(size[0]) + '_' + str(size[1]) + ' background.png'

    def __generate_1on1_image(self):
        if self.info_class.get_transparent_image() is None:
            self.__final_1on1_image = 'NoImage'
            return
        wip_image = Image.open(self.__build_rarity_path((1, 1)))
        icon_image = self.info_class.get_transparent_image().resize(wip_image.size)  # resize icon image to wip image size
        self.__final_1on1_image = Image.alpha_composite(wip_image, icon_image)

    def __get_1on1_background_image(self):
        if self.__final_1on1_image is None:
            self.__generate_1on1_image()
        return self.__final_1on1_image

    def __generate_1on2_image(self):
        wip_image = Image.open(self.__build_rarity_path((1, 2)))

        if self.info_class.get_if_image_featured() is False:
            self.__final_1on2_image = 'NoImage'
            return

        # resize featured image to wip image
        featured_image = self.info_class.get_featured_image().resize((wip_image.size[1], wip_image.size[1]))
        featured_image_size = featured_image.size  # saves image size after resizing.

        cropping_size = int((featured_image_size[0] - wip_image.size[0]) / 2)
        featured_image = featured_image.crop((cropping_size, 0, (featured_image_size[0] - cropping_size), wip_image.size[1]))
        featured_image = featured_image.resize(wip_image.size)
        self.__final_1on2_image = Image.alpha_composite(wip_image.convert("RGBA"), featured_image.convert("RGBA"))

    def __get_1on2_background_image(self):
        if self.__final_1on2_image is None:
            self.__generate_1on2_image()
        return self.__final_1on2_image

    def __get_default_background_image(self):

        # will return 1on2 if possible.
        # if not possible will return 1on1
        if self.info_class.get_if_image_featured():
             return self.__get_1on2_background_image()
        else:
             return self.__get_1on1_background_image()

    def __generate_info_image(self, base_image):

        # resize "base_image", so the width will match the "pasting_image" width
        multiplier = base_image.size[0] / self.assets.get_item_pasting_image_resolution()[0]
        base_image = base_image.resize((self.assets.get_item_pasting_image_resolution()[0],
                                        int(base_image.size[1] * multiplier)))

        wip_image = Image.new('RGBA', base_image.size, (0, 0, 0, 0))  # creates new transparent image
        pasting_offset = base_image.size[1] - self.assets.get_item_pasting_image_resolution()[1]  # calculating pasting offset

        # pasting "shadow" effect on images
        if self.assets.get_item_name_font().getsize(self.info_class.get_name())[0] + 30 < base_image.size[0]:  # checks if the name is fitting in one line.
            # if name is one line:
            more_then_one_line = False
            wip_image.paste(self.assets.get_item_shadow_image_one_line(),
                            (0, pasting_offset),
                            self.assets.get_item_shadow_image_one_line())
        else:
            # if name longer then one line:
            more_then_one_line = True
            wip_image.paste(self.assets.get_item_shadow_image_two_lines(),
                            (0, pasting_offset),
                            self.assets.get_item_shadow_image_two_lines())

        wip_image = Image.alpha_composite(base_image, wip_image)
        wip_canvas = ImageDraw.Draw(wip_image)

        # drawing name text on image
        if not more_then_one_line:
            name_starting_height = base_image.size[1] - 112
            draw_centered_text_lines(wip_canvas, [self.info_class.get_name()], self.assets.get_item_name_font(), "#ffffff",
                                     name_starting_height, base_image.size[0])
        else:
            jumps_between_lines = 45
            name_starting_height = base_image.size[1] - 112 - jumps_between_lines
            lines_list = word_list_to_line_list(self.info_class.get_name().split(' '), 18)
            draw_centered_text_lines(wip_canvas, lines_list, self.assets.get_item_name_font(), "#ffffff",
                                     name_starting_height, base_image.size[0], 0, jumps_between_lines)

        # drawing vbucks icon on image
        cost_starting_height = base_image.size[1] - 57
        space_between_vbucks_text = 43  # space between the vbucks icon and the price text
        cost_width = self.assets.get_item_cost_font().getsize(self.info_class.get_cost())[0]
        vbucks_image_pasting_location = (int((base_image.size[0] - cost_width - space_between_vbucks_text) / 2), cost_starting_height - 5)
        wip_image.paste(self.assets.get_item_vbucks_small_icon(), vbucks_image_pasting_location, self.assets.get_item_vbucks_small_icon())

        # drawing cost number on image
        draw_centered_text_lines(wip_canvas, [self.info_class.get_cost()], self.assets.get_item_cost_font(), "#ffffff", cost_starting_height, base_image.size[0], int(space_between_vbucks_text / 2))

        # pasting image overlay on top of wip image
        overlay_wip_image = Image.new('RGBA', base_image.size, (0, 0, 0, 0))  # creates new transparent image
        wip_image.paste(self.assets.get_item_overlay_image(), (0, pasting_offset), self.assets.get_item_overlay_image())
        wip_image = Image.alpha_composite(wip_image, overlay_wip_image)

        return wip_image.convert("RGB")

    def get_default_info_image(self):
        # will return 1on2 image if possible.
        return self.__generate_info_image(self.__get_default_background_image())

    def get_icon_info_image(self):
        # always will return 1on1 image.
        return self.__generate_info_image(self.__get_1on1_background_image())

    def get_description_string(self):
        return ("Processing Item: " +
                self.info_class.get_name() + ' | ' +
                self.info_class.get_rarity() + ' ' +
                self.info_class.get_type() + '.')


class DrawingShopInfo(DrawingInfo):

    def __init__(self, item_dict):
        DrawingInfo.__init__(self)
        self.info_class = ShopInfo(item_dict)



class DrawingUpcomingInfo(DrawingInfo):

    def __init__(self, item_dict):
        DrawingInfo.__init__(self)
        self.info_class = UpcomingInfo(item_dict)


class NewsInfo:

    def __init__(self, dict):
        self.dict = dict
        self.database = Database(self.dict)
        self.__image_already_saved = False
        self.__news_image = None

    def test_all_functions(self):
        print("get image:", self.get_image())
        print("get image url:", self.get_image_url())
        print("get if hidden:", self.get_if_hidden())
        print("get message type:", self.get_message_type())
        print("get type:", self.get_type())
        print("get ad space:", self.get_ad_space())
        print("get title:", self.get_title())
        print("get body text:", self.get_body_text())
        print("get if spotlight:", self.get_if_spotlight())

    def __generate_news_image(self):
        try:
            self.__news_image = Image.open(
                BytesIO(requests.get(self.database.find_value_by_key('image')[0]).content)).convert("RGBA")
        except OSError:
            self.__news_image = Image.new('RGBA', (900, 450), '#FFFFFF')
        self.__image_already_saved = True

    def get_image(self):
        if self.__image_already_saved is False:
            self.__generate_news_image()
        return self.__news_image

    def get_image_url(self):
        return self.database.find_value_by_key('image')[0]

    def get_if_hidden(self):
        return self.database.find_value_by_key('hidden')[0]

    def get_message_type(self):
        return self.database.find_value_by_key('messagetype')[0]

    def get_type(self):
        return self.database.find_value_by_key('_type')[0]

    def get_ad_space(self):
        if self.database.find_value_by_key('adspace') == []:
            return None
        return self.database.find_value_by_key('adspace')[0]

    def get_title(self):
        return self.database.find_value_by_key('title')[0]

    def get_body_text(self):
        return self.database.find_value_by_key('body')[0]

    def get_if_spotlight(self):
        return self.database.find_value_by_key('spotlight')[0]


class Database:

    def __init__(self, dict):
        self.database = dict

    def find_value_by_key(self, search_key, database=None):
        if database is None:
            database = self.database

        if type(search_key) is str:
            return self.__find_value_by_key(search_key, database)

        elif type(search_key) is list:
            wip_database = database
            for key in search_key:
               wip_database = self.__find_value_by_key(key, wip_database)
            return wip_database

        return []

    def __find_value_by_key(self, search_key, database=None):

        if database is None:
            database = self.database

        # NOTHING IS FOUND
        if self.__stop_condition(database, search_key):
            return []

        # MATCH FOUND
        if search_key in database:
            return [database[search_key]]

        found_elements_list = []

        if type(database) is dict:
            for element in database:
                found_elements_list += self.__find_value_by_key(search_key, database[element])
        else:
            for element in database:
                found_elements_list += self.__find_value_by_key(search_key, element)

        return found_elements_list

    def __stop_condition(self, database, search_key):
        if (type(database) is dict) or (type(database) is list):
            return False
        else:
            return True


class FortniteAPI:

    def __init__(self, api_url, api_headers):
        self.api_url = api_url
        self.api_headers = api_headers  # no headers with new api.
        self.api_json_data = None

    def generate_json_data(self):
        request = requests.request("GET", self.api_url, headers=self.api_headers)
        self.api_json_data = request.json()

    def get_json_data(self):
        if self.api_json_data is None:
            self.generate_json_data()
        return self.api_json_data


class FortniteItemShopAPI(FortniteAPI):

    def __init__(self):
        FortniteAPI.__init__(self,
                             api_url="https://fortnite-public-api.theapinetwork.com/prod09/store/get",
                             api_headers={})
        self.__items_json_list = None

    def get_item_shop_json(self):
        self.generate_json_data()
        return self.api_json_data

    def __generate_date(self):
        self.__api_date_string = self.get_item_shop_json()["date"]
        self.__api_date_tuple = (
            int(self.__api_date_string[0:2]),
            int(self.__api_date_string[3:5]),
            int(self.__api_date_string[6:8]))

    def get_date(self):
        if self.__api_date_string is None:
            self.__generate_date()
        return self.__api_date_tuple

    def __generate_update_id(self):
        self.__api_update_id = int(self.get_item_shop_json()["lastupdate"])

    def get_update_id(self):
        if self.__api_update_id is None:
            self.__generate_update_id()
        return self.__api_update_id

    def __generate_items_json_list(self):
        if self.api_json_data is None:
            self.generate_json_data()
        self.__items_json_list = self.api_json_data["items"]

    def get_items_json_list(self):
        if self.__items_json_list is None:
            self.__generate_items_json_list()
        return self.__items_json_list


class FortniteUpcomingAPI(FortniteAPI):

    def __init__(self):
        api_settings = ApiSettingsDetails('ToolSetSettings.txt')
        FortniteAPI.__init__(self,
                             api_url="https://fnbr.co/api/upcoming",
                             api_headers={'x-api-key': api_settings.get_fnbrco_api_key()})

    def get_upcoming_items_json(self):
        self.generate_json_data()
        return self.api_json_data['data']


class ApiSettingsDetails(ValuesTxtFile):

    def get_fnbrco_api_key(self):
        return self.get_value_by_key('fnbr.co Key')


def draw_centered_text_lines(
        canvas,
        lines_list,
        lines_font,
        lines_color,
        starting_drawing_height,
        canvas_width,
        lines_width_shift=0,
        jump_between_lines=10):
    for line_num in range(len(lines_list)):
        line_height = starting_drawing_height + (line_num * jump_between_lines)
        line_width = lines_font.getsize(lines_list[line_num])[0]
        line_starting_width = ((canvas_width - line_width) / 2) + lines_width_shift
        canvas.text(
            (line_starting_width, line_height),
            lines_list[line_num],
            font=lines_font,
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
