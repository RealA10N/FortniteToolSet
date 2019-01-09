import requests  # TO GET API
from PIL import Image, ImageDraw, ImageFont  # TO EDIT IMAGES
from io import BytesIO  # TO LOAD IMAGE FROM API
import os.path

# input: the dictionary item form the api
# parses back: item info
class ShopInfo:

    def __init__(self, item_dict):
        self.item_dict = item_dict
        self.transparent_image = None
        self.image_already_saved = False
        self.featured_image = None
        self.featured_image_already_saved = False

    def get_itemid(self):
        return self.item_dict['itemid']

    def get_name(self):
        return self.item_dict['name']

    def get_cost(self):
        return self.item_dict['cost']

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
            self.featured_image = self.__generate_featured_transparent_image()
        return self.featured_image

    def __generate_featured_transparent_image(self):
        featured_image = Image.open(BytesIO(requests.get(
            self.item_dict['item']['images']['featured']['transparent']).content)).resize((1024, 1024)).convert("RGBA")
        self.featured_image_already_saved = True
        return featured_image


class DrawingItems:

    background_assets_path = os.getcwd() + "\\Items Assets\\Background Images"

    def __init__(self, name, rarity, cost, icon_image, featured_image=None):
        self.__name = name
        self.__rarity = rarity
        self.__cost = cost
        self.__icon_image = icon_image
        self.__featured_image = featured_image
        self.__background_1on1_image = None
        self.__background_1on2_image = None
        self.__final_1on1_image = None
        self.__final_1on2_image = None


    def __build_rarity_path(self, size):
        temp_path = self.background_assets_path\
               + '\\' + self.__rarity + ' ' + str(size[0]) + '_' + str(size[1]) + ' background.png'
        if os.path.isfile(temp_path):
            return temp_path
        else:
            return self.background_assets_path\
               + '\\' + "common" + ' ' + str(size[0]) + '_' + str(size[1]) + ' background.png'

    def __generate_1on1_image(self):
        wip_image = Image.open(self.__build_rarity_path((1, 1)))
        icon_image = self.__icon_image.resize(wip_image.size)  # resize icon image to wip image size
        self.__final_1on1_image = Image.alpha_composite(wip_image, icon_image)

    def get_1on1_image(self):
        if self.__final_1on1_image is None:
            self.__generate_1on1_image()
        return self.__final_1on1_image

    def __generate_1on2_image(self):
        featured_image = self.__featured_image
        wip_image = Image.open(self.__build_rarity_path((1, 2)))

        if featured_image == None:
            return None

        featured_image_size = featured_image.size
        wip_image_size = wip_image.size

        featured_image = featured_image.resize((wip_image_size[1], wip_image_size[1])) # resize featured image to wip image

        if featured_image_size[0] >= wip_image_size[0]:
            cropping_size = int((featured_image_size[0] - wip_image_size[0]) / 2)
            featured_image = featured_image.crop((cropping_size, 0, featured_image_size[0] - cropping_size, wip_image_size[1]))
        else:
            featured_image = featured_image.resize(wip_image_size)
        self.__final_1on2_image = Image.alpha_composite(wip_image.convert("RGBA"), featured_image.convert("RGBA"))

    def get_1on2_image(self):
        if self.__final_1on2_image is None:
            self.__generate_1on2_image()
        return self.__final_1on2_image


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
        news_image = Image.open(
            BytesIO(requests.get(self.database.find_value_by_key('image')[0]).content)).convert("RGBA")
        self.__image_already_saved = True
        self.__news_image = news_image

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


class JsonReader:

    def __init__(self, request_url, request_headers=None):
        self.__request_url = request_url
        self.__request_headers = request_headers
        self.__api_request = self.__create_api_request(request_url, request_headers)
        self.__json_data = self.__create_json_data(self.get_api_request())

    def __create_api_request(self, request_url, request_headers):
        return requests.request("GET", request_url, headers=request_headers)

    def __create_json_data(self, api_request):
        return api_request.json()

    def get_request_url(self):
        return self.__request_url

    def get_request_headers(self):
        return self.__request_headers

    def get_api_request(self):
        return self.__api_request

    def get_json_data(self):
        return self.__json_data


class FortniteItemShopAPI:

    def __init__(self):
        self.__api_url = "https://api.gamingsdk.com/client/game/fortnite/scope/store/"
        self.__api_headers = {'Authorization': 'c738e77d4212930fd8a1721fd9511c15'}
        self.__api_json_reader = None
        self.__api_json_data = None
        self.__api_date_string = None
        self.__api_update_id = None

    def __get_api_request(self, request_url, request_headers):
        return requests.request("GET", request_url, headers=request_headers)

    def __generate_json_reader(self):
        self.__api_json_reader = JsonReader(self.__api_url, self.__api_headers)

    def __generate_json_data(self):
        if self.__api_json_reader is None:
            self.__generate_json_reader()
        self.__api_json_data = self.__api_json_reader.get_json_data()

    def get_item_shop_json(self):
        self.__generate_json_data()
        return self.__api_json_data

    def get_json_reader(self):
        self.__generate_json_reader()
        return self.__api_json_reader

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
