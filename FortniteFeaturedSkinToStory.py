import FortniteApiCommands
import ConsoleFunctions
import os
from PIL import Image


def build_image_path(rarity):
    return background_assets_path + '\\FeaturedSkinToStory ' + rarity + '.png'

def generate_print_title(item):
    return item.get_name() +  ' | ' + item.get_rarity() + ' '+ item.get_type()


console = ConsoleFunctions.ConsolePrintFunctions()
console.print_one_line_title("Fortnite Featured Image Generator. // Created by @RealA10N", "single heavy square")
print()  # to go one line down.

console.print_replaceable_line('Loading "Fortnite API" data...')
background_assets_path = os.getcwd() + '\\FeaturedSkinToStoryAssets'
fortnite_api = FortniteApiCommands.FortniteItemShopAPI()
items_info_list = fortnite_api.get_item_shop_json()["items"]
featured_items = []
console.print_replaceable_line('Searching for "Featured" items only...')

for item in items_info_list:
    item_info = FortniteApiCommands.ShopInfo(item)
    if item_info.get_if_image_featured():
        featured_items.append(item_info)

console.print_replaceable_line('All data loaded successfully!\n\n')
titles_list = []
for item in featured_items:
    titles_list.append(generate_print_title(item))

selected_index = console.select_by_index(titles_list, 'Please select the image that you want to make by index:')
selected_item = featured_items[int(selected_index)]

try:
    background_image = Image.open(build_image_path(selected_item.get_rarity())).convert("RGBA")
except FileNotFoundError:
    background_image = Image.open(build_image_path("Common")).convert("RGBA")

print("\nWant to offset the featured image? enter the number of pixels:")
offset = int(input())

wip_image_w, wip_image_h = background_image.size
featured_image = selected_item.get_featured_image()
featured_image = featured_image.resize((wip_image_h, wip_image_h))
featured_im_w, featured_im_h = featured_image.size
cropping_size = int((featured_im_w - wip_image_w)/2)
featured_image = featured_image.crop((cropping_size - offset, 0, featured_im_w - cropping_size - offset, wip_image_h))
finished_image = Image.alpha_composite(background_image, featured_image)

overlay_text_image = Image.open(background_assets_path + "\\FeaturedSkinToStory Overlay.png")
finished_image = Image.alpha_composite(finished_image, overlay_text_image)

saving_name = "LastFeaturedSkinToStory.png"
finished_image.save(saving_name)
os.startfile(saving_name)
input("\nImage generated and saved successfully! Press 'ENTER' to exit.")
