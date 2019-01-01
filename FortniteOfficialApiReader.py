import requests


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

    def get_json_date(self):
        return self.__json_data

    def __stop_condition(self, database, search_key):
        if (type(database) is dict) or (type(database) is list):
            return False
        else:
            return True


    def find_value_by_key(self, database, search_key):

        # NOTHING IS FOUND
        if self.__stop_condition(database, search_key):
            return []

        # MATCH FOUND
        if search_key in database:
            return [database[search_key]]

        found_elements_list = []

        if type(database) is dict:
            for element in database:
                found_elements_list += self.find_value_by_key(database[element], search_key)
        else:
            for element in database:
                found_elements_list += self.find_value_by_key(element, search_key)

        return found_elements_list


fortnite_json_api = \
    JsonReader('https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game')

x = fortnite_json_api.get_json_date()
x = fortnite_json_api.find_value_by_key(fortnite_json_api.find_value_by_key(fortnite_json_api.find_value_by_key(x, 'battleroyalenews'), 'messages'), 'adspace')
print(x)
