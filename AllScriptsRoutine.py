import os
from ConsoleFunctions import *
from SendEmail import SendEmail
from FortniteApiCommands import *


# importing scripts
from v2_ItemShopToStoryImage import get_final_item_shop_image
from v2_NewsToStoryImage import craft_news_image, get_news_database


def script_open(name):
    print("\n" + name + " | Opening...")


def delete_dir_content(dir_path):
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        os.unlink(file_path)


print('''
About the script:
this script will import the ItemShop, News and Featured scripts, and will run them all together.
THIS SCRIPT IS NOT READY YET AND IS UNDER WORK.
''')

base_folder_path = os.getcwd()
final_images_dir = base_folder_path + '\\RoutineFinalImages'
delete_dir_content(final_images_dir)

# print title
console = ConsolePrintFunctions()
console.print_one_line_title(os.path.basename(__file__) + " // Created by @RealA10N", "single heavy square")

# v2_ItemShopToStoryImage script
script_open("v2_ItemShopToStoryImage")
itemshop_assets_folder_path = base_folder_path + r'\ItemsAssets'
final_image = get_final_item_shop_image(itemshop_assets_folder_path)
shop_image_path = final_images_dir + r"\ItemShopUpload.png"
final_image.save(shop_image_path)

# v2_NewsIoStoryImage script
script_open("v2_NewsIoStoryImage")
news_assets_folder_path = base_folder_path + r'\NewsGeneratorAssets'
news_database = get_news_database()
for news in news_database.get_news_list():
    final_image_name = "News Image - " + news.get_title() + ".png"
    final_image_path = final_images_dir + '\\' + final_image_name
    craft_news_image(news, news_assets_folder_path).save(final_image_path)

# FortniteFeaturedSkinToStory script
# add script here! (:

# send email
email = SendEmail()
email.add_recipient_address('downtown2u@gmail.com')
email.set_subject('Your Instagram Routine!')
email.add_body('Sent automatically by a bot. Created by @RealA10N')
for image in os.listdir(final_images_dir):
    file_path = os.path.join(final_images_dir, image)
    email.add_file(file_path)

email.login(input('enter your email: '), input('enter your password: '))
email.send_mail()
