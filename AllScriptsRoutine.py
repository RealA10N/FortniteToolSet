import os
from ConsoleFunctions import *
from SendEmail import SendEmail
from FortniteApiCommands import *
from JsonFileManager import ToolSetSettingsJson

# importing scripts
from FortniteFeaturedSkinToStory import GenerateFeaturedImage, search_featured_only


def delete_dir_content(dir_path):

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        os.unlink(file_path)


def generate_item_save_name(item):
    saving_name = item.get_name() + " - " + item.get_rarity() + ' ' + item.get_type()
    return saving_name


# print title
console = ConsolePrintFunctions()
console.print_one_line_title(os.path.basename(
    __file__) + " // Created by @RealA10N", "single heavy square")

base_folder_path = os.getcwd()
final_images_dir = base_folder_path + '\\RoutineFinalImages'
delete_dir_content(final_images_dir)

# v3_ItemShopToStoryImage script
console.script_open("v3_ItemShopToStoryImage")
itemshop_path = os.path.join(base_folder_path, 'v3_ItemShopToStoryImage.py')
os.system("%s -q -sp %s" % (itemshop_path, final_images_dir))

# v2_NewsIoStoryImage script
console.script_open("v2_NewsIoStoryImage")
news_path = os.path.join(base_folder_path, 'v2_NewsToStoryImage.py')
os.system("%s -q -a -sp %s" % (news_path, final_images_dir))

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
    print('FortniteFeaturedSkinToStory | Saved featured image of "' +
          generate_item_save_name(item) + '"!')


# send email
console.script_open('SendEmail')
json_settings = ToolSetSettingsJson()
email = SendEmail()
email.add_recipient_address(json_settings.get_addressee_email())
email.set_subject('Your Instagram Routine!')
email.add_body('Sent automatically by a bot. Created by @RealA10N')
for image in os.listdir(final_images_dir):
    file_path = os.path.join(final_images_dir, image)
    email.add_file(file_path)

console.regular_print('Connecting to google servers...')
email.login(json_settings.get_sender_email(), json_settings.get_sender_password())
email.send_mail()
email.server_quit()
console.regular_input('Files are sent successfully! Type anything to exit. ')
