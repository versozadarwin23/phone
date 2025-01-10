from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains
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
    global apps, element, dawssw_text, dawdsadwadasdwadwaferfgregre
    fb_apps = dict(
        platformName=device["platformName"],
        automationName=device["automationName"],
        uiautomator2ServerLaunchTimeout='96000',
        platformVersion=device["platformVersion"],
        deviceName=device["deviceName"],
        # unicodeKeyboard=True,
        # resetKeyboard=True,
        skipServerInstallation=True,
        ignoreUnimportantViews=True,
        skipDeviceInitialization=True,
        deviceReadyTimeout='999999',
        skipLogcatCapture=True,
        adbExecTimeout='999999',
        autoWebview=False,
        udid=device["udid"],
        # chromeOptions={"w3c": False},
        chromeOptions={"w3c": False, "args": ['--user-agent="Mozilla/5.0 (Linux; Android 13; V2053) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"']},
        browserName="Chrome",
        chromedriverExecutable="C:/Users/USER/Desktop/phone/chromedriver/" + device["chromedriver"] + ".exe",
        newCommandTimeout='96000',
    )
    while True:
        try:
            driver = webdriver.Remote("http://localhost:4723/wd/hub", fb_apps)
            break
        except:
            pass
    try:
        apps = fetch_appName_by_deviceID(deviceID=device["deviceID"])
    except:
        pass
    try:
        subprocess.check_output("adb -s " + " " + device["udid"] + " " + "shell settings put global stay_on_while_plugged_in 3", shell=True)
    except:
        pass
    for x in apps:
        try:
            airplane_mode_off(device)
            time.sleep(5)
        except:
            pass

        while True:
            try:
                driver.get("https://m.facebook.com/")
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "email")))
                break
            except:
                try:
                    subprocess.check_output("adb -s " + " " + device["udid"] + " " + "shell am force-stop io.appium.uiautomator2.server", shell=True)
                    subprocess.check_output("adb -s " + " " + device["udid"] + " " + "shell am force-stop io.appium.uiautomator2.server.test", shell=True)
                    device_tasks(device)
                except:
                    pass

        while True:
            try:
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys(x["username"])
            except:
                try:
                    subprocess.check_output(
                        "adb -s " + " " + device["udid"] + " " + "shell am force-stop io.appium.uiautomator2.server",
                        shell=True)
                    subprocess.check_output("adb -s " + " " + device[
                        "udid"] + " " + "shell am force-stop io.appium.uiautomator2.server.test", shell=True)
                    device_tasks(device)
                except:
                    pass
            try:
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "pass"))).send_keys(x["password"])
            except:
                try:
                    subprocess.check_output(
                        "adb -s " + " " + device["udid"] + " " + "shell am force-stop io.appium.uiautomator2.server",
                        shell=True)
                    subprocess.check_output("adb -s " + " " + device[
                        "udid"] + " " + "shell am force-stop io.appium.uiautomator2.server.test", shell=True)
                    device_tasks(device)
                except:
                    pass
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Log in"]'))).click()
                break
            except:
                try:
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'login'))).click()
                    break
                except:
                    pass

        try:
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Save"]'))).click()
            time.sleep(15)
        except:
            print(x["deviceID"] + " " + x["username"] + " " + "Login Error")
            continue

        try:
            webview = driver.contexts[1]
            driver.switch_to.context(webview)
            driver.switch_to.context('NATIVE_APP')
            time.sleep(0.3)
        except:
            pass
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'com.android.chrome:id/positive_button'))).click()
            time.sleep(3)
            webview = driver.contexts[1]
            driver.switch_to.context(webview)
            driver.switch_to.context('CHROMIUM')
        except:
            webview = driver.contexts[1]
            driver.switch_to.context(webview)
            driver.switch_to.context('CHROMIUM')

        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Make a Post on Facebook"]')))
        except:
            print(x["deviceID"] + " " + x["username"] + " " + "Login Error")
            continue


        # if x["report"] == "yes":
        #     for report_group in x["report_link"].split(" "):
        #         while True:
        #             try:
        #                 driver.get(report_group)
        #                 break
        #             except:
        #                 pass
        #
        #         while True:
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.LINK_TEXT, 'More'))).click()
        #                 break
        #             except:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="RESOLVE_PROBLEM"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #
        #         try:
        #             WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="RESOLVE_PROBLEM"]'))).click()
        #         except:
        #             pass
        #         try:
        #             WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
        #         except:
        #             pass
        #
        #
        #         if x["Harassment"] == "yes":
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="harassment_or_bullying"]'))).click()
        #                     break
        #                 except:
        #                     try:
        #                         WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="harassment"]'))).click()
        #                     except:
        #                         pass
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
        #             except:
        #                 pass
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #
        #         if x["Hate speech"] == "yes":
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="hate_speech"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
        #             except:
        #                 pass
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #
        #         if x["False information"] == "yes":
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="false_news"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="misinformation_politics"]'))).click()
        #             except:
        #                 pass
        #
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
        #             except:
        #                 pass
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
        #             except:
        #                 pass
        #
        #         if x["Terrorism"] == "yes":
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="terrorism"]'))).click()
        #             except:
        #                 pass
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
        #             except:
        #                 pass
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
        #             except:
        #                 pass
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
        #             except:
        #                 pass
        #
        #         if x["Unauthorized sales"] == "yes":
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="unauthorized_sales"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
        #             except:
        #                 pass
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #
        #         if x["Violence"] == "yes":
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="violence"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
        #             except:
        #                 pass
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #
        #         if x["Spam"] == "yes":
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="spam"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Submit"]'))).click()
        #                     break
        #                 except:
        #                     pass
        #             try:
        #                 WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="yes"]'))).click()
        #             except:
        #                 pass
        #             while True:
        #                 try:
        #                     WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Report"]'))).click()
        #                     break
        #                 except:
        #                     pass


        #if x["Meme"] == "yes":
            # for memess in x["Meme_Link"].split(" "):
            #     try:
            #         driver.get(memess)
            #     except:
            #         pass
            #     time.sleep(5)
            #
            #     #push meme photo to device
            #     # try:
            #         # subprocess.check_output("adb -s " + " " + device["udid"] + " " + "push" + " " + x["photo"] + " " + "/storage/emulated/0/Download")
            #     # except:
            #     #     pass
            #     try:
            #         WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Post a photo"]'))).send_keys("//storage//emulated//0//Download//" + x["photo_name"])
            #     except:
            #         pass

        # Like Page
        if x["Like Page"] == "yes":
            for like_page in x["Page_Link"].split(" "):
                while True:
                    try:
                        driver.get(like_page)
                        time.sleep(5)
                        break
                    except:
                        pass

                try:
                    WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Like"]'))).click()
                    print(x["deviceID"] + " " + x["profile"] + " " + like_page + " " + "Like Page Done")
                except:
                    try:
                        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="See more"]'))).click()
                    except:
                        pass
                    try:
                        webview = driver.contexts[1]
                        driver.switch_to.context(webview)
                        driver.switch_to.context('NATIVE_APP')
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@text='Like']"))).click()
                        print(x["deviceID"] + " " + x["profile"] + " " + like_page + " " + "Like Page Done")
                    except:
                        pass
                    try:
                        webview = driver.contexts[1]
                        driver.switch_to.context(webview)
                        driver.switch_to.context('CHROMIUM')
                    except:
                        pass


                try:
                    WebDriverWait(driver, 0.3).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Follow"]'))).click()
                    print(x["deviceID"] + " " + x["profile"] + " " + like_page + " " + "Follow Page Done")
                except:
                    try:
                        WebDriverWait(driver, 0.3).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="See more"]'))).click()
                    except:
                        pass

                    try:
                        webview = driver.contexts[1]
                        driver.switch_to.context(webview)
                        driver.switch_to.context('NATIVE_APP')
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 0.5).until(EC.presence_of_element_located(
                            (By.XPATH, "//android.widget.Button[@text='Follow']"))).click()
                        print(x["deviceID"] + " " + x["profile"] + " " + like_page + " " + "Follow Page Done")
                    except:
                        pass
                    try:
                        webview = driver.contexts[1]
                        driver.switch_to.context(webview)
                        driver.switch_to.context('CHROMIUM')
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
            for votess in x["Vote_Link"].split(" "):
                actions = ActionChains(driver)
                while True:
                    try:
                        driver.get(votess)
                        break
                    except:
                        continue
                while True:
                    try:
                        time.sleep(5)
                        votek = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, 'div[style="width:80px; color:#1763cf;"]')))
                        time.sleep(5)
                        break
                    except:
                        pass
                while True:
                    try:
                        actions.click(votek).perform()
                        time.sleep(5)
                        break
                    except:
                        pass
                while True:
                    try:
                        scrowls = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[style="color:#65676b;"]')))
                        time.sleep(5)
                        break
                    except:
                        pass
                if len(scrowls) > 5:
                    while True:
                        try:
                            element_to_scroll_to = scrowls[5]
                            time.sleep(5)
                            break
                        except:
                            pass

                    # Scroll to the element
                    actions = ActionChains(driver)
                    actions.move_to_element(element_to_scroll_to).perform()
                else:
                    print("There are less than 10 elements with the specified style.")
                while True:
                    try:
                        webview = driver.contexts[1]
                        driver.switch_to.context(webview)
                        driver.switch_to.context('NATIVE_APP')
                        time.sleep(0.3)
                        break
                    except:
                        pass
                time.sleep(5)
                kjk = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//android.view.View[@text='MARTIN ROMUALDEZ']")))
                actions.click(kjk).perform()
                print(x["deviceID"] + " " + x["profile"] + " " + "Vote Done")
                while True:
                    try:
                        webview = driver.contexts[1]
                        driver.switch_to.context(webview)
                        driver.switch_to.context('CHROMIUM')
                        time.sleep(0.3)
                        break
                    except:
                        pass

        # comment
        if x["Comment"] == "yes":
            # options = random.choice([1, 1, 2, 2, 3, 3])
            comment = fetch_random_comment_by_category(category=x["category"])
            for comments in x["comment link"].split(" "):
                actions = ActionChains(driver)
                while True:
                    try:
                        driver.get(comments)
                        break
                    except:
                        pass

                while True:
                    try:
                        time.sleep(5)
                        comms = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-mcomponent="MInputBox"]')))
                        time.sleep(0.3)
                        actions.send_keys_to_element(comms, comment).perform()
                        time.sleep(0.3)
                        break
                    except:
                        pass

                while True:
                    try:
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Post a comment"]'))).click()
                        break
                    except:
                        try:
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[value="Comment"]'))).click()
                            break
                        except:
                            pass
                while True:
                    try:
                        element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[style="color:#65676b;"]')))
                        time.sleep(0.5)
                        print(x["deviceID"] + " " + x["profile"] + " " + comments + " " + "Comment done")
                        break
                    except:
                        pass

        # reaction
        if x["reaction"] == "yes":
            for o in x["links_to_react"].split(" "):
                reaction = get_reaction_by_link(link=o)
                actions = ActionChains(driver)
                while True:
                    try:
                        driver.get(o)
                        time.sleep(5)
                        break
                    except:
                        pass

                try:
                    webview = driver.contexts[1]
                    driver.switch_to.context(webview)
                    driver.switch_to.context('NATIVE_APP')
                    time.sleep(0.3)
                except:
                    pass

                try:
                    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, 'com.android.chrome:id/positive_button'))).click()
                    time.sleep(3)
                    webview = driver.contexts[1]
                    driver.switch_to.context(webview)
                    driver.switch_to.context('CHROMIUM')
                except:
                    webview = driver.contexts[1]
                    driver.switch_to.context(webview)
                    driver.switch_to.context('CHROMIUM')

                try:
                    dawdsadwadasdwadwaferfgregre = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[aria-label="Like button double tap and hold for more reactions."]')))[0]
                except:
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    except:
                        pass

                time.sleep(0.3)
                try:
                    actions.move_to_element(dawdsadwadasdwadwaferfgregre).perform()
                except:
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    except:
                        pass
                try:
                    time.sleep(0.3)
                    dawssw = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[style="color:#4b4c4f;"]')))[0]
                    time.sleep(0.3)
                    dawssw_text = dawssw.text
                except:
                    pass

                try:
                    holdss = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='" + dawssw_text + "like, double tap and hold for more reactions'")))
                except:
                    continue

                time.sleep(0.3)
                touch_input = PointerInput(interaction.POINTER_TOUCH, 'touch')
                time.sleep(0.3)
                actions.w3c_actions = ActionBuilder(driver, mouse=touch_input)
                time.sleep(0.3)
                try:
                    actions.w3c_actions.pointer_action.click_and_hold(holdss)
                except:
                    pass
                time.sleep(0.3)
                actions.perform()
                time.sleep(3)
                actions.reset_actions()
                time.sleep(0.5)

                webview = driver.contexts[1]
                driver.switch_to.context(webview)
                driver.switch_to.context('NATIVE_APP')

                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@text='" + reaction + "']"))).click()
                    print(x["deviceID"] + " " + x["profile"] + " " + o + " " + reaction + " " + "React Done")
                except:
                    try:
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.view.View[@text='" + reaction + "']"))).click()
                        print(x["deviceID"] + " " + x["profile"] + " " + o + " " + reaction + " " + "React Done")
                    except:
                        pass
                webview = driver.contexts[1]
                driver.switch_to.context(webview)
                driver.switch_to.context('CHROMIUM')

        if x["upvote"] == "yes":
            actions = ActionChains(driver)
            action = TouchAction(driver)
            for u in x["upvote_link"].split(" "):
                reaction = get_reaction_by_link(link=u)
                while True:
                    try:
                        driver.get(u)
                        driver.set_page_load_timeout(120)
                        break
                    except:
                        pass
                scrowlssssss = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[aria-label="Like button double tap and hold for more reactions."]')))[1]
                actions.move_to_element(scrowlssssss).perform()

                webview = driver.contexts[1]
                driver.switch_to.context(webview)
                driver.switch_to.context('NATIVE_APP')

                dawdsafwqfqwdqw = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@text='Like button double tap and hold for more reactions.']")))

                touch_input = PointerInput(interaction.POINTER_TOUCH, 'touch')
                actions.w3c_actions = ActionBuilder(driver, mouse=touch_input)
                time.sleep(0.2)
                actions.w3c_actions.pointer_action.click_and_hold(dawdsafwqfqwdqw)
                time.sleep(0.2)
                actions.perform()
                time.sleep(0.2)

                webview = driver.contexts[1]
                driver.switch_to.context(webview)
                driver.switch_to.context('NATIVE_APP')
                try:
                    time.sleep(0.1)
                    WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH, "//android.view.View[@text='" + reaction + "']"))).click()
                    print(x["deviceID"] + " " + x["profile"] + " " + u + " " + reaction + " " + "React Done")
                except:
                    time.sleep(0.1)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@text='" + reaction + "']"))).click()
                    print(x["deviceID"] + " " + x["profile"] + " " + u + " " + reaction + " " + "React Done")

                webview = driver.contexts[1]
                driver.switch_to.context(webview)
                driver.switch_to.context('CHROMIUM')

        # share Post
        if x["share"] == "yes":
            post_list = x["links_to_share"].split(' ')
            actionsdawdaw = ActionChains(driver)
            for g in post_list:
                driver.get('https://www.facebook.com/composer/')
                time.sleep(10)
                # Wait for all elements to be visible
                whats_on_your_mind_click = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[style="color:#666666;"]')))
                whats_on_your_mind = whats_on_your_mind_click[0]
                actionsdawdaw.send_keys_to_element(whats_on_your_mind, g).perform()
                time.sleep(0.3)
                driver.hide_keyboard()
                time.sleep(5)
                whats_on_your_mind_clicks = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[style="color:#666666;"]')))
                whats_on_your_mind_clear = whats_on_your_mind_clicks[0]
                actiondawdaws = ActionChains(driver)
                time.sleep(0.3)
                actiondawdaws.click(whats_on_your_mind_clear).perform()
                time.sleep(0.3)
                while True:
                    try:
                        subprocess.check_output("adb -s " + " " + device["udid"] + " " + "shell input keyevent --longpress 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67", shell=True)
                        time.sleep(0.3)
                        driver.hide_keyboard()
                        break
                    except:
                        pass
                time.sleep(0.3)
                postss_click = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[style="color:#1877f2;"]')))
                time.sleep(0.3)
                actionsdawdaw.click(postss_click[0]).perform()
                print(x["deviceID"] + " " + x["profile"] + " " + g + " " + "Share Done")
                time.sleep(0.3)

        # Post Timeline without caption
        if x["timeline post"] == "yes":
            post_timeline = timeline_post(category=x["category"])
            for g in post_timeline:
                try:
                    driver.get("https://mbasic.facebook.com/home.php")
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
                    driver.get("https://mbasic.facebook.com/friends/center/requests/")
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.LINK_TEXT, 'Back to home')))
                    break
                except:
                    pass
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.LINK_TEXT, "Confirm"))).click()
                    driver.get("https://mbasic.facebook.com/friends/center/requests/")
                except:
                    try:
                        driver.refresh()
                    except:
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
            try:
                subprocess.check_output("adb -s " + " " + device["udid"] + " " + "shell am force-stop io.appium.uiautomator2.server",shell=True)
                subprocess.check_output("adb -s " + " " + device["udid"] + " " + "shell am force-stop io.appium.uiautomator2.server.test",shell=True)
                device_tasks(device)
            except:
                pass
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
