import requests  # TO GET API
from PIL import Image, ImageDraw, ImageFont  # TO EDIT IMAGES
from io import BytesIO  # TO LOAD IMAGE FROM API
import os

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


class CraftItemFinalImage:
    assets_folder_path = os.getcwd() + '\\ItemsAssets'
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
        self.current_item = ItemShopInfo(item_dict)

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

    def draw_item_info(self, current_item_image):
        cur_image_w, cur_image_h = current_item_image.size
        if self.get_font_width_from_variable(self.current_item.get_name(), self.item_name_font) + 20 < cur_image_w:
            if cur_image_h == 512:
                current_item_image = Image.alpha_composite(current_item_image, self.item_shadow_box_one_line_1on1)
            elif cur_image_h == 1126:
                current_item_image = Image.alpha_composite(current_item_image, self.item_shadow_box_one_line_1on2)
            current_item_draw_canvas = ImageDraw.Draw(current_item_image)
            item_name_starting_height = cur_image_h - 112
            self.draw_centered_text_lines(
                current_item_draw_canvas,
                [self.current_item.get_name()],
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
                self.word_list_to_line_list((self.string_to_word_list(self.current_item.get_name())), 18),
                    self.item_name_font,
                    self.item_name_color,
                    item_name_starting_height,
                    cur_image_w,
                    0,
                    item_name_jumps)

        # DRAW PRICE
        item_cost_starting_height = cur_image_h - 62
        item_cost_width = self.get_font_width_from_variable(self.current_item.get_cost(), self.item_cost_font)
        vbucks_image_paste_loction = (
        int((cur_image_w - item_cost_width - self.space_between_vbuck_image_text) / 2), item_cost_starting_height)
        current_item_image.paste(
            self.vbucks_image,
            vbucks_image_paste_loction,
            self.vbucks_image)
        self.draw_centered_text_lines(
            current_item_draw_canvas,
            [self.current_item.get_cost()],
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
            self.current_item.get_rarity(),
            (1, 1),
            self.current_item.get_transparent_image())
        return current_item_image

    def craft_1on2_item_image(self):
        rarity_set = RaritySet(self.assets_folder_path)
        current_item_image = rarity_set.apply_rarity(
            self.current_item.get_rarity(),
            (1, 2),
            featured_image=self.current_item.get_featured_image())
        return current_item_image


def get_api_request(request_url, request_headers):
    return requests.request("GET", request_url, headers=request_headers)


def table_value(item_num, max_in_row):
    row = item_num // max_in_row
    column = item_num % max_in_row
    return (row, column)

def generate_table_list(items_in_row, num_of_rows, deafult_value=None):
    list = []
    temp_list = []
    for i in range(num_of_rows):
        for ii in range(items_in_row):
            temp_list.append(deafult_value)
        list.append(temp_list)
        temp_list = []
    return list


##########################
#    GENERATING IMAGE    #
##########################

assets_folder_path = os.getcwd() + '\\ItemsAssets'
api_url = 'https://api.gamingsdk.com/client/game/fortnite/scope/store/'
api_headers = {'Authorization': 'c738e77d4212930fd8a1721fd9511c15'}
print("| Progress | Downloading \"Store Info\" from API.")
api_list = get_api_request(api_url, api_headers)
print("| Progress | Info downloaded and saved successfully: " + str(api_list.json()['items']))

normal_items_images_list = []
featured_items_images_list = []
rarity_set = RaritySet(assets_folder_path)

for item_dict in api_list.json()['items']:
    current_item = ItemShopInfo(item_dict)
    final_image = CraftItemFinalImage(item_dict)
    if current_item.get_if_image_featured() == True:
        wip_image = final_image.draw_item_info(final_image.craft_1on2_item_image())
        featured_items_images_list.append(wip_image)
    else:
        wip_image = final_image.draw_item_info(final_image.craft_1on1_item_image())
        normal_items_images_list.append(wip_image)
    print("| Progress | Possessed Item: " +
          current_item.get_name() + ' | ' +
          current_item.get_rarity() + ' ' +
          current_item.get_type() + '.')

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

last_item_num = current_item_number

for current_item_image, current_item_number in zip(featured_items_images_list, range(len(normal_items_images_list), len(featured_items_images_list) + len(normal_items_images_list))):
    current_item_image_resized = current_item_image.resize((250, 550))
    current_item_table = table_value(current_item_number, items_in_row)
    item_pasting_location = (
        pasting_starting_position[1] + current_item_table[1] * pasting_jumps[1],
        pasting_starting_position[0] + current_item_table[0] * pasting_jumps[0])
    item_shop_canvas.paste(current_item_image_resized, item_pasting_location)

item_shop_canvas.save("LastItemShopUpload.png")
item_shop_canvas.show()
