from FortniteApiCommands import *
from ConsoleFunctions import *


class ItemsContainer:

    def __init__(self, table_size):
        self.__table_width, self.__table_height = table_size
        self.__items_tables = []
        self.__current_item_index = 0
        self.__num_item_one_table = self.__table_width * self.__table_height

    def append_item(self, item):
        c_table, c_row, c_column = self.__index_to_table_value(self.__current_item_index)  # c = current
        self.__current_item_index += 1

        if len(self.__items_tables) == c_table:
            self.__add_table((self.__table_width, self.__table_height), None)

        if self.__items_tables[c_table][c_row][c_column] is None:  # if the place is empty
            if item.get_if_image_featured():
                if c_row == self.__table_height:  # if its the last line
                    self.__items_tables[c_table][c_row][c_column] = item.get_icon_info_image()
                else:  # if the item is featured and not the last one
                    self.__items_tables[c_table][c_row][c_column] = item.get_default_info_image()
                    self.__items_tables[c_table][c_row + 1][c_column] = 'taken'
            else:  # if the item not featured
                self.__items_tables[c_table][c_row][c_column] = item.get_icon_info_image()
        else:  # if the place is taken
            self.append_item(item)  # run the function for the next place in the table

    def __index_to_table_value(self, index):
        table_index = index // self.__num_item_one_table
        one_table_index = index - (table_index * self.__num_item_one_table)
        row = one_table_index // self.__table_width
        column = one_table_index % self.__table_width
        return (table_index, row, column)

    def __table_value_to_index(self, table_value):
        return (table_value[0] * self.__table_width) + table_value[1]

    def __add_table(self, table_size, value=None):
        final_list = []
        temp_list = []
        for i in range(table_size[1]):
            for ii in range(table_size[0]):
                temp_list.append(value)
            final_list.append(temp_list)
            temp_list = []
        self.__items_tables.append(final_list)

console = ConsolePrintFunctions()
console.print_one_line_title("Fortnite Item Shop Generator. // Created by @RealA10N", "single heavy square")

fortnite_api = FortniteItemShopAPI()
items_list = fortnite_api.get_items_json_list()

items_container = ItemsContainer((3, 4))

for item_dict in items_list:
    item_class = DrawingShopItem(item_dict)
    items_container.append_item(item_class)
