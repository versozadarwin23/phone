try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

import os
import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from appium import webdriver
import itertools
from xlrd import open_workbook
from future.utils import iteritems
from past.builtins import xrange
from multiprocessing import Process
import random
try:
    urlretrieve('https://raw.githubusercontent.com/versozadarwin23/phone/main/phone.py', 'C:/Users/user/Desktop/phone/phone.py')
except:
    pass
input_file = "phone.xlsx"
sheet_names = ["Phones", "Apps", "Comments", "Timeline", "Friends", "Reactions"]
sheet = ""
filter_variables_dict = ""
all_data = []
category = ""
number = 1
profile_id = ""
deviceID = ""
comment_length = [1]
chunkList = []
numberOfElements = 15
caption = ""
post = ""
friendList = []
device = []
driver = ''
login = ""


def convert_sheet_to_dict(file_path=input_file, sheet=sheet, filter_variables_dict=None):
    global keys
    if file_path is not None:
        keys = [sheet.cell(0, col_index).value for col_index in xrange(sheet.ncols)]

    found_row_dict_list = []
    for column_index, key in enumerate(keys):
        if filter_variables_dict is not None:
            for column_name, column_value in iteritems(filter_variables_dict):
                if key == column_name:
                    for row_index in xrange(sheet.nrows):
                        if not (column_name is None and column_value is None):
                            if sheet.cell(row_index, column_index).value == column_value:
                                found_row_dict = {
                                    keys[col_index_internal]: sheet.cell(row_index, col_index_internal).value
                                    for col_index_internal in xrange(sheet.ncols)}
                                found_row_dict_list.append(found_row_dict)
                        else:
                            found_row_dict = {
                                keys[col_index_internal]: sheet.cell(row_index, col_index_internal).value
                                for col_index_internal in xrange(sheet.ncols)}
                            found_row_dict_list.append(found_row_dict)
        elif filter_variables_dict == {} or filter_variables_dict is None:
            filter_variables_dict = {}
            for row_index in xrange(sheet.nrows):
                found_row_dict = {keys[col_index_internal]: sheet.cell(row_index, col_index_internal).value
                                  for col_index_internal in xrange(sheet.ncols)}
                found_row_dict_list.append(found_row_dict)
            del found_row_dict_list[0]
    result_dict_list = []
    if len(found_row_dict_list) > 1 and len(filter_variables_dict) > 1:
        for a, b in itertools.combinations(found_row_dict_list, len(filter_variables_dict)):
            if a == b:
                result_dict_list.append(a)
    else:
        result_dict_list = found_row_dict_list

    return result_dict_list


class XlToDict:

    @staticmethod
    def fetch_data_by_column_by_sheet_name_multiple(file_name, filter_variables_dict=None, sheet_names=None):

        if sheet_names is None:
            sheet_names = sheet_names
        workbook = open_workbook(filename=file_name)
        if sheet_names is None:
            sheet_names = workbook.sheet_names()

        for sheet_name in sheet_names:
            sheet = workbook.sheet_by_name(sheet_name)
            all_data.append(convert_sheet_to_dict(sheet=sheet, filter_variables_dict=filter_variables_dict))
        return all_data


myxlobject = XlToDict()
c = myxlobject.fetch_data_by_column_by_sheet_name_multiple(file_name=input_file, sheet_names=sheet_names,
                                                           filter_variables_dict=None)

phones_sheet = all_data[0]
apps_sheet = all_data[1]
comments_sheet = all_data[2]
timeline_sheet = all_data[3]
friends_sheet = all_data[4]
reactions_sheet = all_data[5]


def fetch_random_comment_by_category(category=category, number=number):
    comment_list = []
    comment = ""
    for x in comments_sheet:
        if x["Category"] == category:
            comment_list.append(x["Comment"])

    random_items = random.sample(population=comment_list, k=number)
    for z in random_items:
        comment = comment + " " + z
    return comment


def fetch_allPostTimeline_by_category(category=category):
    post_list = []
    f = {}
    for x in timeline_sheet:
        if x["Category"] == category:
            f["caption"] = fetch_random_comment_by_category(category=x["Caption"], number=1)
            f["link"] = x["Link"]
            post_list.append(f)
    return post_list


def timeline_post(category=category):
    post_timeline = []
    for x in timeline_sheet:
        if x["Category"] == category:
            caption = fetch_random_comment_by_category(category=x["Caption"], number=1)
            post = caption
            post_timeline.append(post)
    return post_timeline


def fetch_friends_by_profile(profile_id=profile_id):
    friends_list = []
    for x in friends_sheet:
        if x["profile"] == profile_id:
            friends_list.append(x["friends"])
    return friends_list


def fetch_appName_by_deviceID(deviceID=deviceID):
    appName_list = []
    for x in apps_sheet:
        if x["deviceID"] == deviceID:
            appName_list.append(x)
    return appName_list


def get_reaction_by_link(link):
    reaction = ''
    for x in reactions_sheet:
        if x["Link"] == link:
            reaction = x["Reaction"]
    return reaction


def airplane_mode_off(device):
    try:
        subprocess.check_output("adb -s " + " " + device["udid"] + " " + "shell settings put global airplane_mode_on 0",shell=True)
    except:
        pass
    try:
        subprocess.check_output("adb -s " + " " + device["udid"] + " " + "shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false", shell=True)
    except:
        pass

def airplane_mode_on(device):
    try:
        subprocess.check_output("adb -s " + " " + device["udid"] + " " + "shell settings put global airplane_mode_on 1",shell=True)
    except:
        pass
    try:
        subprocess.check_output("adb -s " + " " + device["udid"] + " " + "shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true", shell=True)
    except:
        pass

def device_tasks(device):
    fb_apps = dict(
        platformName=device["platformName"],
        automationName=device["automationName"],
        uiautomator2ServerLaunchTimeout='96000',
        platformVersion=device["platformVersion"],
        deviceName=device["deviceName"],
        skipServerInstallation=True,
        ignoreUnimportantViews=True,
        skipDeviceInitialization=True,
        deviceReadyTimeout='999999',
        skipLogcatCapture=True,
        adbExecTimeout='999999',
        udid=device["udid"],
        chromeOptions={"w3c": False, "args": ['--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"']},
        browserName="Chrome",
        chromedriverExecutable="C:/Users/USER/Desktop/phone/chromedriver/" + device["chromedriver"] + ".exe",
        newCommandTimeout='96000',
    )
    while True:
        try:
            time.sleep(5)
            driver = webdriver.Remote("http://localhost:4723/wd/hub", fb_apps)
            time.sleep(10)
            break
        except:
            pass
    apps = fetch_appName_by_deviceID(deviceID=device["deviceID"])
    try:
        subprocess.check_output("adb -s " + " " + device["udid"] + " " + "shell settings put global stay_on_while_plugged_in 3", shell=True)
    except:
        pass
    for x in apps:
        if x["signup"] == "yes":
            if device["platformVersion"] == "5.1":
                try:
                    airplane_mode_off(device)
                    time.sleep(20)
                except:
                    pass
            while True:
                try:
                    driver.get("https://free.facebook.com/")
                    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "email")))
                    break
                except:
                    try:
                        driver.quit()
                    except:
                        pass
                    try:
                        device_tasks(device)
                    except:
                        pass

            while True:
                try:
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys(
                        x["username"])
                except:
                    try:
                        device_tasks(device)
                    except:
                        pass
                try:
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "pass"))).send_keys(
                        x["password"])
                except:
                    pass
                try:
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "login"))).click()
                    break
                except:
                    pass
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Not now"))).click()
            except:
                pass
            # try:
            #     WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[action="/zero/optin/write/?action=confirm&page=dialtone_optin_page"]'))).click()
            # except:
            #     pass
            try:
                time.sleep(10)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Continue"]')))
                print(x["deviceID"] + " " + x["profile"] + " " + x["username"] + " " + x["password"] + " " +  "We'll send a confirmation code to your phone so that you can confirm your identity.")
                continue
            except:
                pass
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Get started')))
                print(x["deviceID"] + " " + x["profile"] + " " + x["username"] + " " + x["password"] + " " +  "your account has been locked")
                continue
            except:
                pass
            try:
                driver.get("https://free.facebook.com/home.php")
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.LINK_TEXT, "Edit profile"))).click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Timeline'))).click()
                ind = driver.current_url.index("%")
                edited_link = driver.current_url.replace(driver.current_url[ind:], "")
                url = edited_link.replace('profile.php?v=timeline&lst=', '')
                print(x["deviceID"] + " " + x["profile"] + " " + x["username"] + " " + x["password"] + " " + url)
            except:
                pass

            # check if block or wrong password
            try:
                driver.get('https://free.facebook.com/profile_picture?_rdc=1&_rdr')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'pic')))
            except:
                try:
                    driver.delete_all_cookies()
                except:
                    pass

            if x["report"] == "yes":
                for report_group in x["report_link"].split(" "):
                    while True:
                        try:
                            driver.get(report_group)
                            break
                        except:
                            pass

                    while True:
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.LINK_TEXT, 'More'))).click()
                            break
                        except:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="RESOLVE_PROBLEM"]'))).click()
                                break
                            except:
                                pass

                    try:
                        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="RESOLVE_PROBLEM"]'))).click()
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
                    except:
                        pass


                    if x["Harassment"] == "yes":
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="harassment_or_bullying"]'))).click()
                                break
                            except:
                                try:
                                    WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="harassment"]'))).click()
                                except:
                                    pass
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
                                break
                            except:
                                pass
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
                        except:
                            pass
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
                                break
                            except:
                                pass

                    if x["Hate speech"] == "yes":
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="hate_speech"]'))).click()
                                break
                            except:
                                pass
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
                                break
                            except:
                                pass
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
                        except:
                            pass
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
                                break
                            except:
                                pass

                    if x["False information"] == "yes":
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="false_news"]'))).click()
                                break
                            except:
                                pass

                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
                                break
                            except:
                                pass
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="misinformation_politics"]'))).click()
                        except:
                            pass

                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
                                break
                            except:
                                pass
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
                        except:
                            pass
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
                                break
                            except:
                                pass
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
                        except:
                            pass

                    if x["Terrorism"] == "yes":
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="terrorism"]'))).click()
                        except:
                            pass
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
                        except:
                            pass
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
                        except:
                            pass
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
                        except:
                            pass

                    if x["Unauthorized sales"] == "yes":
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="unauthorized_sales"]'))).click()
                                break
                            except:
                                pass
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
                                break
                            except:
                                pass
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
                        except:
                            pass
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
                                break
                            except:
                                pass

                    if x["Violence"] == "yes":
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="violence"]'))).click()
                                break
                            except:
                                pass
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
                                break
                            except:
                                pass
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
                        except:
                            pass
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
                                break
                            except:
                                pass

                    if x["Spam"] == "yes":
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="spam"]'))).click()
                                break
                            except:
                                pass
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
                                break
                            except:
                                pass
                        try:
                            WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
                        except:
                            pass
                        while True:
                            try:
                                WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
                                break
                            except:
                                pass


            if x["post photo"] == "yes":
                try:
                    driver.get('https://free.facebook.com/')
                except:
                    pass

                # Post Timeline photo
                try:
                    subprocess.check_output("adb -s " + " " + device["udid"] + " " + "push" + " " + x[
                        "photo"] + " " + "/storage/emulated/0/Download")
                except:
                    pass
                try:
                    WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.NAME, 'view_photo'))).click()
                except:
                    pass
                try:
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'file1'))).send_keys(
                        "//storage//emulated//0//Download//" + x["photo_name"])
                except:
                    pass
                try:
                    WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.NAME, 'add_photo_done'))).click()
                except:
                    pass
                try:
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'view_post'))).click()
                except:
                    pass

            # Like Page
            if x["Like Page"] == "yes":
                for like_page in x["Like Page_Link"].split(" "):
                    while True:
                        try:
                            driver.get(like_page)
                            break
                        except:
                            pass
                    try:
                        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Like'))).click()
                        print(x["deviceID"] + " " + x["profile"] + " " + like_page + " " + "Like Page Done")
                    except:
                        pass

                    try:
                        WebDriverWait(driver, 3).until(
                            EC.visibility_of_element_located((By.LINK_TEXT, 'Follow'))).click()
                        print(x["deviceID"] + " " + x["profile"] + " " + like_page + " " + "Follow Page Done")
                    except:
                        pass

            # Join Group
            if x["Join Group"] == "yes":
                for join_group in x["Group_Link"].split(" "):
                    while True:
                        try:
                            driver.get(join_group)
                            break
                        except:
                            pass
                    try:
                        WebDriverWait(driver, 6).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Join Group"]'))).click()
                        print(x["deviceID"] + " " + x["profile"] + " " + join_group + " " + "Group Done")
                    except:
                        pass

            # vote
            if x["Vote"] == "yes":
                for join_group in x["Vote_Link"].split(" "):
                    while True:
                        try:
                            driver.get(join_group)
                            time.sleep(5)
                            break
                        except:
                            pass
                    while True:
                        try:
                            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, x["Vote_Name"]))).click()
                            print(x["deviceID"] + " " + x["profile"] + " " + "Vote Done")
                            break
                        except:
                            pass

            # comment
            if x["Comment"] == "yes":
                options = random.choice([1, 1, 2, 2, 3, 3])
                comment = fetch_random_comment_by_category(category=x["category"], number=options)
                for comments in x["comment link"].split(" "):
                    driver.get(comments)
                    try:
                        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'composerInput'))).send_keys(comment)
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[value="Comment"]'))).click()
                        print(x["deviceID"] + " " + x["profile"] + " " + comments + " " + "Comment done")
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.LINK_TEXT, 'Back to home')))
                        print(x["deviceID"] + " " + x["profile"] + " " + "Your account is restricted right now")
                        break
                    except:
                        pass

            # share Post
            if x["share"] == "yes":
                post_list = x["links_to_share"].split(' ')
                for g in post_list:
                    try:
                        driver.get(g)
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Share"))).click()
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "view_post"))).click()
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[title="Your account is restricted right now"]')))
                        print(x["deviceID"] + " " + x["profile"] + " " + "Your account is restricted right now")
                        break
                    except:
                        pass

            # Post Timeline without caption
            if x["timeline post"] == "yes":
                post_timeline = timeline_post(category=x["category"])
                for g in post_timeline:
                    try:
                        driver.get("https://free.facebook.com/home.php")
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, "xc_message"))).send_keys(g)
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "view_post"))).click()
                        print(x["deviceID"] + " " + x["profile"] + " " + g + " " + "Timeline Post Done")
                    except:
                        pass
            # reaction
            if x["reaction"] == "yes":
                for o in x["links_to_react"].split(" "):
                    reaction = get_reaction_by_link(link=o)
                    try:
                        driver.get(o)
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.LINK_TEXT, reaction))).click()
                        print(x["deviceID"] + " " + x["profile"] + " " + o + " " + reaction + " " + "React Done")
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, '[title="Your account is restricted right now"]')))
                        print(x["deviceID"] + " " + x["profile"] + " " + "Your account is restricted right now")
                        break
                    except:
                        pass

            if x["add friends"] == "yes":
                friendList = fetch_friends_by_profile(profile_id=x["profile"])
                for y in friendList:
                    try:
                        driver.get(y)
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.LINK_TEXT, "Add friend"))).click()
                    except:
                        pass
            if x["friends confirm"] == "yes":
                for y in range(1000):
                    try:
                        driver.get("https://free.facebook.com/friends/center/requests/")
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.LINK_TEXT, 'Back to home')))
                        break
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.LINK_TEXT, "Confirm"))).click()
                        driver.get("https://free.facebook.com/friends/center/requests/")
                    except:
                        try:
                            driver.refresh()
                        except:
                            pass
                        pass
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.LINK_TEXT, "See People You May Know")))
                        break
                    except:
                        pass

            try:
                driver.delete_all_cookies()
            except:
                pass

            if device["platformVersion"] == "5.1":
                try:
                    airplane_mode_on(device)
                    time.sleep(10)
                except:
                    pass

if __name__ == "__main__":  # confirms that the code is under main function
    for i in phones_sheet:
        proc = Process(target=device_tasks, args=(i,))
        proc.start()
        time.sleep(10)
