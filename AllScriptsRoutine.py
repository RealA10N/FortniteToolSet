import os
from ConsoleFunctions import *

#importing scripts
from v2_ItemShopToStoryImage import get_final_item_shop_image


def script_open(name):
    # print("\nOpening " + name + "...")
    print("\n" + name + " | Opening...")


print('''
About the script:
this script will import the ItemShop, News and Featured scripts, and will run them all together.
THIS SCRIPT IS NOT READY YET AND IS UNDER WORK.
''')

# print title
console = ConsolePrintFunctions()
console.print_one_line_title(os.path.basename(__file__) + " // Created by @RealA10N", "single heavy square")

# v2_ItemShopToStoryImage script
script_open("v2_ItemShopToStoryImage")
base_folder_path = os.getcwd()
assets_folder_path = base_folder_path + '\\ItemsAssets'
final_image = get_final_item_shop_image(assets_folder_path)
final_image.show()
