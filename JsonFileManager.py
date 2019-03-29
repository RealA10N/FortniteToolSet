import json


class JsonDictReader:

    def __init__(self):
        file_path = 'ToolSetSettings.json'
        self.__json = self.__generate_json_data(file_path)

    def __generate_json_data(self, file_path):
        with open(file_path) as file:
            return json.loads(file.read())

    def get_json_date(self):
        return self.__json

    def get_dict_value(self, key):
        return self.__json[key]['value']

    def get_dict_description(self, key):
        return self.__json[key]['__description']


class ToolSetSettingsJson(JsonDictReader):

    def get_addressee_email(self):
        return self.get_dict_value('addressee_email')

    def get_sender_email(self):
        return self.get_dict_value('sender_email')

    def get_sender_password(self):
        return self.get_dict_value('sender_password')

    def get_fnbrco_api_key(self):
        return self.get_dict_value('fnbr.co_api_key')
