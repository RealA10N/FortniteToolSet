import requests  # TO GET API
from PIL import Image, ImageDraw, ImageFont  # TO EDIT IMAGES
from io import BytesIO  # TO LOAD IMAGE FROM API
import autoit  # TO CONTROL FILE SELECTION WINDOW
import time # TO CONTROL SLEEPING TIME
import datetime  # TO CHECK COMPUTER TIME
import os  # TO CONTROL THE FOLDERS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewsInfo:

    def __init__(self, request_list, news_num=0):
        self.request_list = request_list
        self.image = None
        self.title = ''
        self.body = ''
        self.time = ''
        self.get_news(news_num)

    def get_news(self, news_num):
        original_news_dictionary = self.request_list.json()['entries'][news_num]
        self.image = Image.open(BytesIO(requests.get(original_news_dictionary['image']).content))  # image output: .jpeg 1024 on 512
        self.title = original_news_dictionary['title']
        self.body = original_news_dictionary['body']
        self.time = original_news_dictionary['time']


def calculate_time(hours=0, minutes=10, seconds=0):
    time_to_add = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    time_now = datetime.datetime.today()
    time_goal = time_to_add + time_now
    return str(time_goal)[0:-7]


def get_api_request(request_url):
    return requests.get(str(request_url))


def check_new_news(old_api_list, new_api_list):
    new_news_indexes = []
    checking_news_index = 0
    while NewsInfo(old_api_list, 0).title != NewsInfo(new_api_list, checking_news_index).title:
        new_news_indexes.append(checking_news_index)
        checking_news_index += 1
    return new_news_indexes


def string_to_word_list(input_string):
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


def word_list_to_line_list(words_list, max_line_ch):
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


def get_font_width_from_variable(variable, font):
    return font.getsize(variable)[0]  # 0 to get first index, and not list with w and h


def draw_centered_text_lines(canvas, lines_list, lines_font, lines_color, starting_drawing_hight, lines_width_shift=0,
                             jump_between_lines=10):
    for line_num in range(len(lines_list)):
        line_hight = starting_drawing_hight + line_num * jump_between_lines
        line_width = get_font_width_from_variable(lines_list[line_num], lines_font)
        canvas.text((((1000 - line_width) / 2) + lines_width_shift, line_hight), lines_list[line_num], font=lines_font,
                    fill=lines_color)


def select_file_chrome_window(title, file_path):
    autoit.win_wait_active(title)
    autoit.control_send(title,"Edit1",file_path)
    autoit.control_click(title,"Button1")


def console_to_typing_box(element_xpath, console_string):
    element = driver.find_element_by_xpath(element_xpath)
    username_input = input(console_string)
    element.send_keys(username_input)


def instagram_login(input_username, input_password):
    #Entering login details
    element_username_xpath = "//input[@name='username']" #Username
    element_username = driver.find_element_by_xpath(element_username_xpath)
    element_username.send_keys(input_username)
    time.sleep(0.5)
    element_password_xpath = "//input[@name='password']" #Password
    element_password = driver.find_element_by_xpath(element_password_xpath)
    element_password.send_keys(input_password)
    print("Progress: Checking info. Please wait...")
    time.sleep(0.5)
    driver.find_element_by_xpath(element_password_xpath).send_keys(Keys.RETURN)
    time.sleep(3)

    try:
        element_2fa_xpath = "//input[@name='verificationCode']" #2fa
        console_to_typing_box(element_2fa_xpath, "Please enter Instagram 2fa code: ")
        time.sleep(1)
        driver.find_element_by_xpath(element_2fa_xpath).send_keys(Keys.RETURN)
        print("Logging in. Please wait...")
        time.sleep(3)
    except:
        print("Logged succecfuly, without 2fa.")

    try:  # this pop up is not showing all the time.
        element_saveinfo_xpath = "//button[@class='GAMXX']"  # to ignore the pop up of saving login info to browser
        element_saveinfo = driver.find_element_by_xpath(element_saveinfo_xpath)
        element_saveinfo.click()
        time.sleep(3)
    except:
        print('No "saveinfo" pop-up was found')

    try:  # this pop up is not showing all the time.
        element_notification_popup_xpath = "//button[@class='aOOlW   HoLwm ']"  # to ignore the pop up of push notipications.
        element_notification_popup = driver.find_element_by_xpath(element_notification_popup_xpath)
        element_notification_popup.click()
        time.sleep(3)
    except:
        print('No "notification" pop-up was found')


##########################
#         START          #
##########################


print("|  Credit  | This script was made by RealA10N! (:")
print("|  Status  | Running.")

#Chrome window settings
mobile_settings = {"deviceMetrics":{"width":1000,"height":2000}, "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"} #info from http://chromedriver.chromium.org/mobile-emulation
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('mobileEmulation', mobile_settings)
driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_options)
driver.set_window_size(1, 2)

#Loading instagram
print("Proggress: Loading Instagram login page.")
driver.get("https://www.instagram.com/accounts/login/")
#ig_username = input("IG Username: ")
#ig_password = input("IG Password: ")
#instagram_login(ig_username, ig_password)
input("Type something when you ready. ")
#Close Window
time.sleep(2)
#driver.close()


##########################
# INSTAGRAM STORY UPLOAD #
##########################
def story_upload(path):
    try:  # this pop up is not showing all the time.
        element_saveinfo_xpath = "//button[@class='GAMXX']"  # to ignore the pop up of saving login info to browser
        element_saveinfo = driver.find_element_by_xpath(element_saveinfo_xpath)
        element_saveinfo.click()
        time.sleep(3)
    except:
        print('No "saveinfo" pop-up was found')

    try:  # this pop up is not showing all the time.
        element_notification_popup_xpath = "//button[@class='aOOlW   HoLwm ']"  # to ignore the pop up of push notipications.
        element_notification_popup = driver.find_element_by_xpath(element_notification_popup_xpath)
        element_notification_popup.click()
        time.sleep(3)
    except:
        print('No "notification" pop-up was found')

    element_new_story_button_xpath = "//button[@class='mTGkH']"  # Clicking on the "New story" button
    element_new_story_button = driver.find_element_by_xpath(element_new_story_button_xpath)
    element_new_story_button.click()
    time.sleep(3)

    select_file_chrome_window('Open', path)
    time.sleep(3)

    element_upload_button_xpath = "//button[@class='u34XU']"  # Uploading the story!
    element_upload_button = driver.find_element_by_xpath(element_upload_button_xpath)
    element_upload_button.click()
    time.sleep(10)


story_upload('C:\\Users\\RealA\\PycharmProjects\\FortniteToInstagram\\test1.png')
story_upload('C:\\Users\\RealA\\PycharmProjects\\FortniteToInstagram\\test2.png')