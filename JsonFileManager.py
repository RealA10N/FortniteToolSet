import json


class ToolSetSettingsJson:

    def __init__(self):
        file_path = 'ToolSetSettings.json'
        self.__json = self.__generate_json_data(file_path)

    def __generate_json_data(self, file_path):
        with open(file_path) as file:
            return json.loads(file.read())

    def get_json_data(self):
        return self.__json

    def get_addressee_email(self):
        return self.__json['addressee_email']['value']

    def get_sender_email(self):
        return self.__json['sender_email']['value']

    def get_sender_password(self):
        return self.__json['sender_password']['value']

    def get_fnbrco_api_key(self):
        return self.get_json_data()['item_shop_api']['choose_api']['fnbr.co']['api_key']

    def __if_using_x_api(self, api_name):
        return bool(self.get_json_data()['item_shop_api']['choose_api'][api_name]['use_this_api'])

    def if_using_fnbrco_api(self):
        return self.__if_using_x_api('fnbr.co')
