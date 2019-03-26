from FortniteApiCommands import *
import ConsoleFunctions


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

        self.__items_tables[c_table][c_row][c_column] = item.get_icon_info_image()

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

    pasting_jumps = (400, 400)
    starting_position = (100, 862)

    row_index = 0
    for items_row in table:

        item_index = 0
        for item in items_row:

            if item is None: continue

            item = item.resize((300, 300))
            # paste on canvas
            pasting_location = (starting_position[0] + item_index * pasting_jumps[0],
                                starting_position[1] + row_index * pasting_jumps[1])
            canvas.paste(item, pasting_location)

            item_index += 1
        row_index += 1

    return canvas

print('''This script is still at work, and may not work as expected or will not work optimally.''')

console = ConsoleFunctions.ConsolePrintFunctions()
console.print_one_line_title(os.path.basename(__file__) + " // Created by @RealA10N", "single heavy square")

table = ItemsContainer((5, 3))
api = FortniteUpcomingAPI()
for item in api.get_upcoming_items_json():
    item_class = DrawingUpcomingInfo(item)
    table.append_item(item_class)
    #item_class.get_icon_info_image().save('F:\\Projects\\Programming\\FortniteToolSet\\TestImages\\' + item_class.get_info_class().get_name() + '.png')
    print(item_class.get_description_string())

for table in table.get_tables_list():
    canvas = Image.open(r'C:\Users\RealA\Desktop\!.png')
    paste_images_on_canvas(canvas, table)
    canvas.show()
