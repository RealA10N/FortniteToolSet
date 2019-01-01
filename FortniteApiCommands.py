import requests  # TO GET API
from PIL import Image, ImageDraw, ImageFont  # TO EDIT IMAGES
from io import BytesIO  # TO LOAD IMAGE FROM API


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
        if self.get_if_featured() == True and self.get_type() == 'outfit':
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
        featured_image = Image.open(BytesIO(requests.get(self.item_dict['item']['images']['featured']['transparent']).content)).resize(
            (1024, 1024)).convert("RGBA")
        self.featured_image_already_saved = True
        return featured_image


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


class FortniteApi:

    def __init__(self):
        self.__api_url = "https://api.gamingsdk.com/client/game/fortnite/scope/store/"
        self.__api_headers = {'Authorization': 'c738e77d4212930fd8a1721fd9511c15'}

    def __get_api_request(self, request_url, request_headers):
        return requests.request("GET", request_url, headers=request_headers)

    def get_item_shop_json(self):
        itemshop_api = JsonReader(self.__api_url, self.__api_headers)
        return itemshop_api.get_json_data()['items']

'''
api = \
    JsonReader('https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game')

__database = Database(api.get_json_data())
x = __database.find_value_by_key(['battleroyalenews', 'messages'])
for news in x[0]:
    y = NewsInfo(news)
    y.test_all_functions()
    print('------')
'''