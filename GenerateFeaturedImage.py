from FortniteApiCommands import ShopInfo, FortniteItemShopAPI
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
        else:
            return False

    def set_setting_by_api_item(self, item):
        self.set_image(item.get_featured_image())
        self.set_rarity(item.get_rarity())

    def set_rarity(self, rarity):
        self.rarity = rarity

    def set_image_offset(self, offset):
        self.offset = int(offset)

    def __generate_item_save_name(self, item):
        saving_name = item.get_name() + " - " + item.get_rarity() + ' ' + item.get_type()
        return saving_name

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


def search_featured_only(shop_api_class):
    items_list = shop_api_class.get_items_json_list()
    featured_items = []
    for item in items_list:
        item_info = ShopInfo(item)
        if item_info.get_if_image_featured():
            featured_items.append(item_info)
    return featured_items


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description='Generate an image (one or more) of the selected skin from the item shop. Created by RealA10N (;')
    parser.add_argument('-sp', '--saving_path', type=str, metavar='',
                        help='Changes the default saving folder path of the generated featured images')
    parser.add_argument('-i', '--selected_skin_index', type=int, metavar='',
                        help='The index of the final generated featured image')
    parser.add_argument('-o', '--offset', type=int, metavar='',
                        help='The offset pixels numbers of the featured image (default is 0)')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Generate all the avalible featured images')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help="Run quietly, without fancy prints and opening the result image(s)")
    return parser.parse_args()


def save_image(featured_class, item_class):
    saving_name = "%s Featured Image.png" % item_class.get_name()
    saving_path = os.path.join(final_saving_folder, saving_name)
    featured_class.get_requested_image().save(saving_path)
    print("'%s' skin featured image generated and saved successfully!" %
          item_class.get_name())
    if not args.quiet:
        os.startfile(saving_path)


def generate_all_images(featured_list, assets_p, final_image_p):
    print()  # go down one line
    for item in featured_list:
        featured_class = GenerateFeaturedImage(assets_p)
        featured_class.set_setting_by_api_item(item)
        save_image(featured_class, item)


def regular_main():

    # print all skins list, and let the user select one of them
    if args.selected_skin_index is None:
        titles_list = []
        for item in featured_items:
            titles_list.append(generate_print_title(item))
        print()  # to go down one line
        selected_index = console.select_by_index(
            titles_list, 'Please select the image that you want to make by index:')
        selected_item = featured_items[int(selected_index)]
    else:
        selected_item = featured_items[args.selected_skin_index]

    # create a "GenerateFeaturedImage" class
    generate_image = GenerateFeaturedImage(background_assets_path)
    # give all the needed info to the "GenerateFeaturedImage" class
    generate_image.set_setting_by_api_item(selected_item)

    # ask the user to select an offset number and transfer the info
    if args.offset is None:
        print("\nWant to offset the featured image? enter the number of pixels:")
        generate_image.set_image_offset(input())
    else:
        generate_image.set_image_offset(args.offset)

    # generate, save and open final image
    print()  # go down one line
    save_image(generate_image, selected_item)


if __name__ == "__main__":

    args = get_args()

    # print credits
    console = ConsoleFunctions.ConsolePrintFunctions()
    if not args.quiet:
        console.print_one_line_title(
            "Fortnite Featured Image Generator. // Created by @RealA10N", "single heavy square")
        print()  # to go one line down.

    # getting info from api
    console.print_replaceable_line('Loading "Fortnite API" data...')
    fortnite_api = FortniteItemShopAPI()

    background_assets_path = os.path.join(os.getcwd(), 'FeaturedSkinToStoryAssets')
    if args.saving_path is None:
        final_saving_folder = os.path.join(os.getcwd(), 'FeaturedFinalImages')
        if not os.path.exists(final_saving_folder):
            os.makedirs(final_saving_folder)
    else:
        final_saving_folder = args.saving_path

    # searching featured only items
    console.print_replaceable_line('Searching for "Featured" items only...')
    featured_items = search_featured_only(fortnite_api)
    console.print_replaceable_line('All data loaded successfully!')

    if args.all:
        generate_all_images(featured_items, background_assets_path, final_saving_folder)
    else:
        regular_main()

    if not args.quiet:
        input("Press 'ENTER' to exit.")