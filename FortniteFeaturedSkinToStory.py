import FortniteApiCommands
import ConsoleFunctions
import os
from PIL import Image

class GenerateFeaturedImage:

    def __init__(self, assets_folder):

        self.assets_folder = assets_folder

        self.image = None
        self.rarity = None
        self.offset = 0

        self.background_image = None

    def __build_image_path(self, rarity):
        return self.assets_folder + '\\FeaturedSkinToStory ' + rarity + '.png'

    def set_image(self, image):
        self.image = image

    def __check_valid_rarity(self, rarity):
        if rarity in ["legendary", "epic", "rare", "uncommon", "common"]:
            return True
        else: return False

    def set_rarity(self, rarity):
        self.rarity = rarity

    def set_image_offset(self, offset):
        self.offset = int(offset)

    def get_requested_image(self):

        # check if rarity is valid
        if not self.__check_valid_rarity(self.rarity):
            raise Exception('rarity is not valid')

        # open background (rarity) image
        self.background_image = Image.open(self.__build_image_path(self.rarity)).convert("RGBA")

        # get image sizes
        wip_image_w, wip_image_h = self.background_image.size
        image_w, image_h = self.image.size

        # paste image on background rarity image
        self.image = self.image.resize((wip_image_h, wip_image_h))
        image_w, image_h = self.image.size  # update image sizes after resize
        cropping_size = int((image_w - wip_image_w) / 2)
        self.image = self.image.crop(
            (cropping_size - self.offset, 0, image_w - cropping_size - self.offset, wip_image_h))
        finished_image = Image.alpha_composite(self.background_image, self.image)

        # paste overlay image on wip image
        overlay_text_image = Image.open(self.assets_folder + "\\FeaturedSkinToStory Overlay.png")
        finished_image = Image.alpha_composite(finished_image, overlay_text_image)

        return finished_image


def generate_print_title(item):
    return item.get_name() + ' | ' + item.get_rarity() + ' ' + item.get_type()


if __name__ == "__main__":

    # print credits
    console = ConsoleFunctions.ConsolePrintFunctions()
    console.print_one_line_title("Fortnite Featured Image Generator. // Created by @RealA10N", "single heavy square")
    print()  # to go one line down.

    # getting info from api
    console.print_replaceable_line('Loading "Fortnite API" data...')
    fortnite_api = FortniteApiCommands.FortniteItemShopAPI()
    items_info_list = fortnite_api.get_item_shop_json()["items"]

    # searching featured only items
    console.print_replaceable_line('Searching for "Featured" items only...')
    featured_items = []
    for item in items_info_list:
        item_info = FortniteApiCommands.ShopInfo(item)
        if item_info.get_if_image_featured():
            featured_items.append(item_info)
    console.print_replaceable_line('All data loaded successfully!\n\n')

    # print all skins list, and let the user select one of them
    titles_list = []
    for item in featured_items:
        titles_list.append(generate_print_title(item))
    selected_index = console.select_by_index(titles_list, 'Please select the image that you want to make by index:')
    selected_item = featured_items[int(selected_index)]

    # create a "GenerateFeaturedImage" class
    background_assets_path = os.getcwd() + '\\FeaturedSkinToStoryAssets'
    generate_image = GenerateFeaturedImage(background_assets_path)

    # give all the needed info to the "GenerateFeaturedImage" class
    generate_image.set_image(selected_item.get_featured_image())
    generate_image.set_rarity(selected_item.get_rarity())

    # ask the user to select an offset number and transfer the info
    print("\nWant to offset the featured image? enter the number of pixels:")
    generate_image.set_image_offset(input())

    # generate, save and open final image
    saving_name = "LastFeaturedSkinToStory.png"
    generate_image.get_requested_image().save(saving_name)
    os.startfile(saving_name)

    input("\nImage generated and saved successfully! Press 'ENTER' to exit.")
