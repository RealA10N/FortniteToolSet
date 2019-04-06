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
        return self.get_json_data()['item_shop_api']['all_apis_settings']['fnbr.co']['api_key']

    def get_default_api_name(self):
        return self.get_json_data()['item_shop_api']['default_api_name']

    def get_if_using_fnbrco_api(self):
        return self.get_default_api_name() == 'fnbr.co'
