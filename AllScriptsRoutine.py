import os
from ConsoleFunctions import *
from SendEmail import SendEmail, EmailSendingDetails
from FortniteApiCommands import *

# importing scripts
from v3_ItemShopToStoryImage import *
from v2_NewsToStoryImage import craft_news_image, get_news_database, give_proper_file_name
from FortniteFeaturedSkinToStory import GenerateFeaturedImage, search_featured_only


def delete_dir_content(dir_path):
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        os.unlink(file_path)


def generate_item_save_name(item):
    saving_name = item.get_name() + " - " + item.get_rarity() + ' ' + item.get_type()
    return saving_name


# print title
console = ConsolePrintFunctions()
console.print_one_line_title(os.path.basename(__file__) + " // Created by @RealA10N", "single heavy square")

base_folder_path = os.getcwd()
final_images_dir = base_folder_path + '\\RoutineFinalImages'
delete_dir_content(final_images_dir)

# v3_ItemShopToStoryImage script
console.script_open("v3_ItemShopToStoryImage")
itemshop_assets_path = os.path.join(base_folder_path, 'ItemsAssets')

console.print_replaceable_line('Downloading itemshop info from api...')
itemshop_api = FortniteItemShopAPI()
items_list = itemshop_api.get_items_json_list()
console.print_replaceable_line('Downloaded itemshop info from api.\n')

items_container = ItemsContainer((3, 4))
for item_dict in items_list:
    item_class = DrawingShopItem(item_dict)
    console.print_replaceable_line(item_class.get_description_string())
    items_container.append_item(item_class)
console.print_replaceable_line('All items possessed successfully.\n')

canvas_path = os.path.join(itemshop_assets_path, 'Additional files', 'ItemShopStoryTemplate.png')

photo_index = 1
for table in items_container.get_tables_list():
    item_shop_canvas = Image.open(canvas_path)
    paste_images_on_canvas(item_shop_canvas, table, (75, 500), (300, 300))
    file_name = 'LastItemShop(' + str(photo_index) + ').png'
    image_saving_path = os.path.join(final_images_dir, file_name)
    item_shop_canvas.save(image_saving_path)
    console.regular_print("File '" + file_name + "' is now saved in the 'ItemShopFinalImages' folder.")
    photo_index += 1


# v2_NewsIoStoryImage script
console.script_open("v2_NewsIoStoryImage")
news_assets_path = base_folder_path + r'\NewsGeneratorAssets'
news_database = get_news_database()
for news in news_database.get_news_list():
    final_image_name = "News Image - " + give_proper_file_name(news.get_title()) + ".png"
    final_image_path = final_images_dir + '\\' + final_image_name
    craft_news_image(news, news_assets_path).save(final_image_path)
print()  # to go down one line

# FortniteFeaturedSkinToStory script
console.script_open("FortniteFeaturedSkinToStory")
featured_assets_path = base_folder_path + r'\FeaturedSkinToStoryAssets'
featured_items = search_featured_only(itemshop_api)

# generate the images. NEEDS TO BE IMPROVED!
for item in featured_items:
    generate_image = GenerateFeaturedImage(featured_assets_path)
    generate_image.set_image(item.get_featured_image())
    generate_image.set_rarity(item.get_rarity())
    saving_name = generate_item_save_name(item)
    saving_path = final_images_dir + '\\' + saving_name + '.png'
    generate_image.get_requested_image().save(saving_path)
    print('FortniteFeaturedSkinToStory | Saved featured image of "' + generate_item_save_name(item) + '"!')


# send email
console.script_open('SendEmail')
email_details = EmailSendingDetails('ToolSetSettings.txt')
email = SendEmail()
email.add_recipient_address(email_details.get_email_to_send_to())
email.set_subject('Your Instagram Routine!')
email.add_body('Sent automatically by a bot. Created by @RealA10N')
for image in os.listdir(final_images_dir):
    file_path = os.path.join(final_images_dir, image)
    email.add_file(file_path)

console.regular_print('Connecting to google servers...')
email.login(email_details.get_sender_username(), email_details.get_sender_password())
email.send_mail()
email.server_quit()
console.regular_input('Files are sent successfully!')
