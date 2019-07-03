import os
from PIL import Image
from FortniteApiCommands import delete_dir_content
from ConsoleFunctions import ConsolePrintFunctions
from JsonFileManager import ToolSetSettingsJson


class ItemsContainer:

    def __init__(self, table_size):
        self.__table_width, self.__table_height = table_size
        self.__items_tables = []
        self.__current_item_index = 0
        self.__num_item_one_table = self.__table_width * self.__table_height

    def append_item(self, item):
        c_table, c_row, c_column = self.__index_to_table_value(
            self.__current_item_index)  # c = current
        self.__current_item_index += 1

        if len(self.__items_tables) == c_table:
            self.__add_table((self.__table_width, self.__table_height), None)

        if self.__items_tables[c_table][c_row][c_column] is None:  # if the place is empty
            if item.info_class.get_if_image_featured():
                if c_row == self.__table_height - 1:  # if its the last line
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

    def get_tables_list(self):
        return self.__items_tables


def paste_images_on_canvas(canvas, table):

    pasting_jumps = (300, 300)

    row_index = 0
    for items_row in table:

        if 'taken' not in items_row:
            starting_position = (75 + (150 * items_row.count(None)), 410)
            while None in items_row:
                items_row.remove(None)  # remove all 'None' from items_row
        else:  # list has 'taken'
            starting_position = (75, 410)

        item_index = 0
        for item in items_row:

            # if item is not image
            if item == 'taken' or item is None:
                item_index += 1
                continue

            if item.size[0] == item.size[1]:  # check if its a 1on2
                item = item.resize((250, 250))
            else:
                item = item.resize((250, 550))

            # paste on canvas
            pasting_location = (starting_position[0] + item_index * pasting_jumps[0],
                                starting_position[1] + row_index * pasting_jumps[1])
            canvas.paste(item, pasting_location)

            item_index += 1
        row_index += 1

    return canvas


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description='Generate an image (one or more) of the current Fortnite item shop. Created by RealA10N (;')
    parser.add_argument('-sp', '--saving_path', type=str, metavar='',
                        help='Changes the default saving folder path of the generated item shop images')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help="Run quietly, without fancy prints and opening the result image(s)")
    return parser.parse_args()


if __name__ == "__main__":

    args = get_args()

    console = ConsolePrintFunctions()
    console.start_script_clock()
    if not args.quiet:
        console.print_one_line_title(
            "Fortnite Item Shop Generator. // Created by @RealA10N", "single heavy square")
        print()  # to go down one line

    base_folder_path = os.getcwd()
    assets_folder_path = os.path.join(base_folder_path, 'ItemsAssets')

    if args.saving_path is None:
        result_folder_path = os.path.join(base_folder_path, 'ItemShopFinalImages')
        delete_dir_content(result_folder_path)
    else:
        result_folder_path = args.saving_path

    console.print_replaceable_line('Downloading itemshop info from api...')
    settings = ToolSetSettingsJson()
    api = settings.get_api_class()
    console.print_replaceable_line('Downloaded itemshop info from api.\n')

    items_container = ItemsContainer((3, 4))
    for item_class in api.get_all_items_drawing_class_list():
        console.print_replaceable_line(item_class.get_description_string())
        items_container.append_item(item_class)
    console.print_replaceable_line('All items processed successfully.                    \n\n')

    canvas_path = os.path.join(assets_folder_path, 'Additional files', 'ItemShopStoryTemplate.png')

    photo_index = 1
    for table in items_container.get_tables_list():

        item_shop_canvas = Image.open(canvas_path)
        paste_images_on_canvas(item_shop_canvas, table)
        file_name = 'LastItemShop(' + str(photo_index) + ').png'
        image_saving_path = os.path.join(result_folder_path, file_name)
        item_shop_canvas.save(image_saving_path)
        if not args.quiet:
            os.startfile(image_saving_path)
            print("File '%s' is now opened and saved in the '%s' folder." %
                  (file_name, os.path.basename(result_folder_path)))
        else:
            print("File '%s' is now saved in the '%s' folder." %
                  (file_name, os.path.basename(result_folder_path)))
        photo_index += 1

    if not args.quiet:
        print()
        console.end_script_clock()
