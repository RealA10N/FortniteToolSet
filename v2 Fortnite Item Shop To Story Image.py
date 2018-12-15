import requests  # TO GET API
from PIL import Image, ImageDraw, ImageFont  # TO EDIT IMAGES
from io import BytesIO  # TO LOAD IMAGE FROM API
import os
from random import shuffle


# input: the dictionary item form the api
# parses back: item info
class ItemShopInfo:

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
        if self.image_already_saved == False:
            self.transparent_image = self.generate_transparent_image()
        return self.transparent_image

    def generate_transparent_image(self):
        transparent_image = Image.open(BytesIO(requests.get(self.item_dict['item']['images']['transparent']).content)).resize(
            (512, 512)).convert("RGBA")
        self.image_already_saved = True
        return transparent_image

    def get_featured_image(self):
        if self.featured_image_already_saved == False:
            self.featured_image = self.generate_featured_transparent_image()
        return self.featured_image

    def generate_featured_transparent_image(self):
        featured_image = Image.open(BytesIO(requests.get(self.item_dict['item']['images']['featured']['transparent']).content)).resize(
            (1024, 1024)).convert("RGBA")
        self.featured_image_already_saved = True
        return featured_image

# input: folder of background images
# 'apply_rarity' returns image (big or small) with background and the skin on it (without the text)
class RaritySet:

    def __init__(self, assets_path):
        self.assets_path = assets_path
        self.background_assets_path = self.assets_path + "\\Background Images"

    def apply_rarity(self, rarity, size, image=None, featured_image=None):
            try:
                working_image = Image.open(self.build_image_path(rarity, size)).convert("RGBA")
            except FileNotFoundError:
                working_image = Image.open(self.build_image_path('common', size)).convert("RGBA")

            if size == (1, 1):
                try:
                    return Image.alpha_composite(working_image, image)
                except ValueError:
                    item_error_image = Image.open(assets_folder_path + '\\Additional files\\ItemErrorImage.png')
                    Image.alpha_composite(working_image, item_error_image)

            elif size == (1, 2):
                working_w, working_h = working_image.size
                featured_image = featured_image.resize((working_h, working_h))
                featured_im_w, featured_im_h = featured_image.size
                cropping_size = int((featured_im_w - working_w)/2)
                featured_image = featured_image.crop((cropping_size, 0, featured_im_w-cropping_size, working_h))

                try:
                    return Image.alpha_composite(working_image, featured_image)
                except ValueError:
                    item_error_image = Image.open(assets_folder_path + '\\Additional files\\ItemErrorImage.png')
                    Image.alpha_composite(working_image, item_error_image)

    def build_image_path(self, rarity, size):
        return self.background_assets_path + '\\' + rarity + ' ' + str(size[0]) + '_' + str(size[1]) + ' background.png'


class GenericItem:
    assets_folder_path = os.getcwd() + '\\Item Shop Generator Assets'
    item_name_font = ImageFont.truetype("BurbankBigRegular-Black.otf", 60)
    item_name_color = '#ffffff'
    item_cost_font = ImageFont.truetype("BurbankBigRegular-Black.otf", 50)
    item_cost_color = '#ffffff'
    space_between_vbuck_image_text = 43
    item_shadow_box_one_line_1on1 = Image.open(assets_folder_path + '\\Additional files\\ItemShopShadowBoxOneLine.png')
    item_shadow_box_two_lines_1on1 = Image.open(assets_folder_path + '\\Additional files\\ItemShopShadowBoxTwoLines.png')
    item_shadow_box_one_line_1on2 = Image.open(assets_folder_path + '\\Additional files\\ItemShop1on2ShadowBoxOneLine.png')
    item_shadow_box_two_lines_1on2 = Image.open(assets_folder_path + '\\Additional files\\ItemShop1on2ShadowBoxTwoLines.png')
    item_outline_box_1on1 = Image.open(assets_folder_path + '\\Additional files\\ItemShopOutlineBox_BottomOnly.png')
    item_outline_box_1on2 = Image.open(assets_folder_path + '\\Additional files\\ItemShop_1on2_OutlineBox_BottomOnly.png')
    vbucks_image = Image.open(assets_folder_path + '\\Additional files\\icon_vbucks.png').resize((40, 40))

    def __init__(self, item_dict):
        self.item_shop_info = ItemShopInfo(item_dict)
        self.final_image_1on1 = None
        self.final_image_1on2 = None
        self.actual_slot_count = self.get_default_slot_count()

    def get_font_width_from_variable(self, variable, font):
        width = font.getsize(variable)[0]  # 0 to get first index, and not list with w and h
        return width

    def draw_centered_text_lines(
            self,
            canvas,
            lines_list,
            lines_font,
            lines_color,
            starting_drawing_height,
            canvas_width,
            lines_width_shift=0,
            jump_between_lines=10):
        for line_num in range(len(lines_list)):
            line_height = starting_drawing_height + line_num * jump_between_lines
            line_width = self.get_font_width_from_variable(lines_list[line_num], lines_font)
            canvas.text(
                (((canvas_width - line_width) / 2) + lines_width_shift, line_height),
                lines_list[line_num],
                font=lines_font,
                fill=lines_color)

    def word_list_to_line_list(self, words_list, max_line_ch):
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

    def string_to_word_list(self, input_string):
        current_word = ''
        words_list = []
        for i in input_string:
            if i == ' ':
                words_list.append(current_word)
                current_word = ''
            else:
                current_word = current_word + i
        if input_string[-1] != ' ':
            words_list.append(current_word)
        return words_list

    def get_description_string(self):
        return ("| Progress | Possessed Item: " +
                self.item_shop_info.get_name() + ' | ' +
                self.item_shop_info.get_rarity() + ' ' +
                self.item_shop_info.get_type() + '.')

    def draw_item_info(self, current_item_image):
        cur_image_w, cur_image_h = current_item_image.size
        if self.get_font_width_from_variable(self.item_shop_info.get_name(), self.item_name_font) + 20 < cur_image_w:
            if cur_image_h == 512:
                current_item_image = Image.alpha_composite(current_item_image, self.item_shadow_box_one_line_1on1)
            elif cur_image_h == 1126:
                current_item_image = Image.alpha_composite(current_item_image, self.item_shadow_box_one_line_1on2)
            current_item_draw_canvas = ImageDraw.Draw(current_item_image)
            item_name_starting_height = cur_image_h - 112
            self.draw_centered_text_lines(
                current_item_draw_canvas,
                [self.item_shop_info.get_name()],
                self.item_name_font,
                self.item_name_color,
                item_name_starting_height,
                cur_image_w)
        else:
            if cur_image_h == 512:
                current_item_image = Image.alpha_composite(current_item_image, self.item_shadow_box_two_lines_1on1)
            elif cur_image_h == 1126:
                current_item_image = Image.alpha_composite(current_item_image, self.item_shadow_box_two_lines_1on2)
            current_item_draw_canvas = ImageDraw.Draw(current_item_image)
            item_name_jumps = 45
            item_name_starting_height = cur_image_h - 112 - item_name_jumps
            self.draw_centered_text_lines(
                current_item_draw_canvas,
                self.word_list_to_line_list((self.string_to_word_list(self.item_shop_info.get_name())), 18),
                    self.item_name_font,
                    self.item_name_color,
                    item_name_starting_height,
                    cur_image_w,
                    0,
                    item_name_jumps)

        # DRAW PRICE
        item_cost_starting_height = cur_image_h - 62
        item_cost_width = self.get_font_width_from_variable(self.item_shop_info.get_cost(), self.item_cost_font)
        vbucks_image_paste_loction = (
        int((cur_image_w - item_cost_width - self.space_between_vbuck_image_text) / 2), item_cost_starting_height)
        current_item_image.paste(
            self.vbucks_image,
            vbucks_image_paste_loction,
            self.vbucks_image)
        self.draw_centered_text_lines(
            current_item_draw_canvas,
            [self.item_shop_info.get_cost()],
            self.item_cost_font,
            self.item_cost_color,
            item_cost_starting_height,
            cur_image_w,
            int(self.space_between_vbuck_image_text / 2))
        if cur_image_h == 512:
            return Image.alpha_composite(current_item_image, self.item_outline_box_1on1)
        elif cur_image_h == 1126:
            return Image.alpha_composite(current_item_image, self.item_outline_box_1on2)

    def craft_1on1_item_image(self):
        # CREATING IMAGE WITH BACKGROUND
        rarity_set = RaritySet(self.assets_folder_path)
        current_item_image = rarity_set.apply_rarity(
            self.item_shop_info.get_rarity(),
            (1, 1),
            self.item_shop_info.get_transparent_image())
        return current_item_image

    def craft_1on2_item_image(self):
        rarity_set = RaritySet(self.assets_folder_path)
        current_item_image = rarity_set.apply_rarity(
            self.item_shop_info.get_rarity(),
            (1, 2),
            featured_image=self.item_shop_info.get_featured_image())
        return current_item_image

    def generate_final_item_images(self):
        if self.item_shop_info.get_if_image_featured():
            self.final_image_1on2 = self.draw_item_info(self.craft_1on2_item_image())
        self.final_image_1on1 = self.draw_item_info(self.craft_1on1_item_image())

    def get_default_slot_count(self):
        if self.item_shop_info.get_if_image_featured():
            return 2
        else:
            return 1

    def update_actual_slot_count(self, update_value=1):
        self.actual_slot_count = update_value

    def get_actual_slot_count(self):
        return self.actual_slot_count

    def get_actual_image(self):
        if self.get_actual_slot_count() == 2:
            return self.final_image_1on2
        elif self.get_actual_slot_count() == 1:
            return self.final_image_1on1


# class that represents items list
class GenericItemsContainer:

    def __init__(self, generic_items_list):
        self.items_list = generic_items_list
        if if_shuffle:
            shuffle(self.items_list)
        self.slot_count = self.count_items_slots()

    def get_items_count(self):
        return len(self.items_list)

    def count_items_slots(self):
        slot_count = 0
        for item in self.items_list:
            slot_count += item.get_default_slot_count()
        return slot_count

    def get_items_slot_count(self):
        return self.slot_count


# class that represents item placement table
class ItemsPlacementTable:

    def __init__(self, rows, columns, default_value=None):
        self.table = self.generate_table_list(rows, columns, default_value)
        self.rows = rows
        self.columns = columns
        self.table_size = rows*columns

    def generate_table_list(self, rows, columns, default_value=None):
        list = []
        temp_list = []
        for i in range(rows):
            for ii in range(columns):
                temp_list.append(default_value)
            list.append(temp_list)
            temp_list = []
        return list

    def legal_table_entry_index(self, entry_index):
        return entry_index <= self.table_size and entry_index >= 0

    def legal_table_entry_cordinates(self, row, column):
        return self.legal_table_entry_index(self.coordinates_to_index(row, column))

    def coordinates_to_index(self, row, column):
        return (row*self.columns)+column

    def index_to_coordinates(self, index):
        row = index // self.columns
        column = index % self.columns
        return (row, column)

    def check_if_entry_empty(self, row, column):
        return self.table[row][column] == None

    def check_legal_row(self, row):
        return row < self.rows

    def check_legal_column(self, column):
        return column < self.columns

    def find_place(self):
        for index in range(self.table_size):
            row, column = self.index_to_coordinates(index)
            if self.check_if_entry_empty(row, column):
                return index
        return -1

    def do_place_item(self, item, next_empty_index):
        row, column = self.index_to_coordinates(next_empty_index)
        self.table[row][column] = item
        if item.get_default_slot_count() == 2:
            if self.check_legal_row(row+1):
                self.table[row+1][column] = True
            else:
                item.update_actual_slot_count(1)

    def place_item(self, item):
        placement_status = True
        next_empty_index = self.find_place()
        if self.legal_table_entry_index(next_empty_index):
            self.do_place_item(item, next_empty_index)
        else:
            placement_status = False
        return placement_status

    def check_if_entry_image(self, row, column):
        return self.table[row][column] != None and self.table[row][column] != True

    def get_placed_items(self):
        placed_items_list = []
        for index in range(self.table_size):
            row, column = self.index_to_coordinates(index)
            if self.check_if_entry_image(row, column):
                placed_items_list.append((index, self.table[row][column]))
        return placed_items_list

def get_api_request(request_url, request_headers):
    return requests.request("GET", request_url, headers=request_headers)

##########################
#    GENERATING IMAGE    #
##########################

assets_folder_path = os.getcwd() + '\\Item Shop Generator Assets'
api_url = 'https://api.gamingsdk.com/client/game/fortnite/scope/store/'
api_headers = {'Authorization': 'c738e77d4212930fd8a1721fd9511c15'}
print("| Progress | Downloading \"Store Info\" from API.")
api_list = get_api_request(api_url, api_headers)
print("| Progress | Info downloaded and saved successfully: " + str(api_list.json()['items']))
if input("|  Random  | Whould you like to shuffle the image? 'y' for yes: ") == 'y':
    if_shuffle = True
else:
    if_shuffle = False

generic_items_list = []
for item_dict in api_list.json()['items']:
    generic_item = GenericItem(item_dict)
    generic_item.generate_final_item_images()
    generic_items_list.append(generic_item)
    print(generic_item.get_description_string())

items_container = GenericItemsContainer(generic_items_list)
table = ItemsPlacementTable(4, 3)
for item in items_container.items_list:
    table.place_item(item)

item_shop_canvas = Image.open(assets_folder_path + '\\Additional files\\ItemShopStoryTemplate.png')
pasting_starting_position = (500, 75)
pasting_jumps = (300, 300)
for (index, item) in table.get_placed_items():
    row, column = table.index_to_coordinates(index)
    item_image = item.get_actual_image()
    if item.get_actual_slot_count() == 1:
        item_image = item_image.resize((250, 250))
    elif item.get_actual_slot_count() == 2:
        item_image = item_image.resize((250, 550))
    item_pasting_location = (pasting_starting_position[1] + column * pasting_jumps[1],
                             pasting_starting_position[0] + row * pasting_jumps[0])
    item_shop_canvas.paste(item_image, item_pasting_location)

item_shop_canvas.save("LastItemShopUpload.png")
item_shop_canvas.show()

'''
item_shop_canvas = Image.open(assets_folder_path + '\\Additional files\\ItemShopStoryTemplate.png')
items_in_row = 3
pasting_starting_position = (500, 75)
pasting_jumps = (300, 300)
for current_item_image, current_item_number in zip(normal_items_images_list, range(len(normal_items_images_list))):
    current_item_image_resized = current_item_image.resize((250, 250))
    current_item_table = table_value(current_item_number, items_in_row)
    item_pasting_location = (
        pasting_starting_position[1] + current_item_table[1] * pasting_jumps[1],
        pasting_starting_position[0] + current_item_table[0] * pasting_jumps[0])
    item_shop_canvas.paste(current_item_image_resized, item_pasting_location)

item_shop_canvas.save("LastItemShopUpload.png")
item_shop_canvas.show()
'''
