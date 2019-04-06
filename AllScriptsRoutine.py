import os
from ConsoleFunctions import ConsolePrintFunctions
from SendEmail import SendEmail
from JsonFileManager import ToolSetSettingsJson


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
final_images_dir = os.path.join(base_folder_path, 'RoutineFinalImages')
delete_dir_content(final_images_dir)

# v3_ItemShopToStoryImage script
console.script_open("GenerateItemShopImage")
itemshop_path = os.path.join(base_folder_path, 'GenerateItemShopImage.py')
os.system("%s -q -sp %s" % (itemshop_path, final_images_dir))

# v2_NewsIoStoryImage script
console.script_open("GenerateNewsImage")
news_path = os.path.join(base_folder_path, 'GenerateNewsImage.py')
os.system("%s -q -a -sp %s" % (news_path, final_images_dir))

# FortniteFeaturedSkinToStory script
console.script_open("GenerateFeaturedImage")
featured_path = os.path.join(base_folder_path, 'GenerateFeaturedImage.py')
os.system("%s -q -a -sp %s" % (featured_path, final_images_dir))

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
