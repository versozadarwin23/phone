try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import pandas as pd
import random
import subprocess
from concurrent.futures import ThreadPoolExecutor

try:
    urlretrieve('https://raw.githubusercontent.com/versozadarwin23/phone/main/phone.py', 'C:/Program Files (x86)/phone/phone.py')
except:
    pass

# Load Excel sheet
input_file = "devices.xlsx"
sheet_names = ["Phones", "Apps", "Comments", "Timeline", "Friends", "Reactions"]

# Load the relevant sheets from the Excel file
df_phones = pd.read_excel(input_file, sheet_name=sheet_names[0])
df_apps = pd.read_excel(input_file, sheet_name=sheet_names[1])
df_comments = pd.read_excel(input_file, sheet_name=sheet_names[2])
df_timeline = pd.read_excel(input_file, sheet_name=sheet_names[3])
df_friends = pd.read_excel(input_file, sheet_name=sheet_names[4])
df_reactions = pd.read_excel(input_file, sheet_name=sheet_names[5])

# Example: Fetch device ID from the Phones sheet
device_ids = df_phones['deviceID'].tolist()
android_device_serials = df_phones['androidDeviceSerial'].tolist()
chromedrivers = df_phones['chromedriver'].tolist()

def fetch_random_comment_by_category(category, number):
    comment_list = [row["Comment"] for _, row in df_comments.iterrows() if row["Category"] == category]
    random_items = random.sample(population=comment_list, k=number)
    return " ".join(random_items)

def fetch_all_post_timeline_by_category(category):
    post_list = []
    for _, row in df_timeline.iterrows():
        if row["Category"] == category:
            f = {
                "caption": fetch_random_comment_by_category(category=row["Caption"], number=1),
                "link": row["Link"]
            }
            post_list.append(f)
    return post_list

def fetch_friends_by_profile(profile_id):
    return [row["friends"] for _, row in df_friends.iterrows() if row["profile"] == profile_id]

def fetch_app_name_by_device_id(device_id):
    return [row for _, row in df_apps.iterrows() if row["deviceID"] == device_id]

def get_reaction_by_link(link):
    for _, row in df_reactions.iterrows():
        if row["Link"] == link:
            return row["Reaction"]
    return ""

def airplane_mode_off(device):
    try:
        if device.get("androidDeviceSerial"):
            subprocess.check_output(
                f"adb -s {device['androidDeviceSerial']} shell settings put global airplane_mode_on 0", shell=True)
            subprocess.check_output(
                f"adb -s {device['androidDeviceSerial']} shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false",
                shell=True)
        else:
            print("Device serial number missing")
    except Exception as e:
        print(f"Error turning off airplane mode on {device.get('androidDeviceSerial', 'Unknown')}: {e}")

def airplane_mode_on(device):
    try:
        if device.get("androidDeviceSerial"):
            subprocess.check_output(
                f"adb -s {device['androidDeviceSerial']} shell settings put global airplane_mode_on 1", shell=True)
            subprocess.check_output(
                f"adb -s {device['androidDeviceSerial']} shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true",
                shell=True)
        else:
            print("Device serial number missing")
    except Exception as e:
        print(f"Error turning on airplane mode on {device.get('androidDeviceSerial', 'Unknown')}: {e}")

def handle_device_tasks(device_id, android_device_serial):
    global dawdsadwadasdwadwaferfgregre, dawssw_text, apps, dawdawghjj, dawssw
    apps = fetch_app_name_by_device_id(device_id=device_id)  # Fetch app details for the device
    for x in apps:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_experimental_option('androidPackage', 'com.android.chrome')
        options.add_experimental_option('androidDeviceSerial', android_device_serial)
        while True:
            try:
                driver = webdriver.Chrome(executable_path="C:/Program Files (x86)/phone/chromedriver/1.exe", options=options)
                break
            except:
                handle_device_tasks(device_id, android_device_serial)

        #show keyboard
        subprocess.check_output("adb -s " + " " + android_device_serial + " " + "shell ime set com.emoji.keyboard.touchpal/com.cootek.smartinput5.TouchPalIME",shell=True)

        #airplane mode on
        subprocess.check_output("adb -s " + " " + android_device_serial + " " + "shell settings put global airplane_mode_on 1",shell=True)
        subprocess.check_output("adb -s " + " " + android_device_serial + " " + "shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true",shell=True)
        time.sleep(5)

        # airplane mode off
        subprocess.check_output("adb -s " + " " + android_device_serial + " " + "shell settings put global airplane_mode_on 0", shell=True)
        subprocess.check_output("adb -s " + " " + android_device_serial + " " + "shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false",shell=True)
        time.sleep(5)

        while True:
            try:
                driver.get("https://m.facebook.com/")
                break
            except:
                handle_device_tasks(device_id, android_device_serial)

        while True:
            try:

                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "email")))
                break
            except:
                handle_device_tasks(device_id, android_device_serial)
        while True:
            try:
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys(x["username"])
                break
            except:
                while True:
                    try:
                        handle_device_tasks(device_id, android_device_serial)
                        break
                    except:
                        pass
        while True:
            try:
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "pass"))).send_keys(x["password"])
                break
            except:
                while True:
                    try:
                        handle_device_tasks(device_id, android_device_serial)
                        break
                    except:
                        pass
        while True:
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Log in"]'))).click()
                break
            except:
                while True:
                    try:
                        handle_device_tasks(device_id, android_device_serial)
                        break
                    except:
                        pass
        try:
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Save"]'))).click()
            time.sleep(15)
        except:
            pass

        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Make a Post on Facebook"]')))
        except:
            print(x["deviceID"] + " " + x["username"] + " " + "Login Error")
            continue

        if 'reaction' in x and x["reaction"] == "yes":
            for link in x.get("links_to_react", "").split(" "):
                reaction = get_reaction_by_link(link=link)
                actions = ActionChains(driver)
                while True:
                    try:
                        driver.get(link)
                        break
                    except:
                        while True:
                            try:
                                handle_device_tasks(device_id, android_device_serial)
                                break
                            except:
                                pass
                while True:
                    try:
                        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located(
                            (By.CSS_SELECTOR, '[aria-label="Like, button double tap and hold for more reactions."]')))
                        break
                    except:
                        pass

                try:
                    dawdsadwadasdwadwaferfgregre = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[aria-label="Like, button double tap and hold for more reactions."]')))[0]
                except:
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    except:
                        pass

                try:
                    actions.move_to_element(dawdsadwadasdwadwaferfgregre).perform()
                except:
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    except:
                        pass
                try:
                    dawssw = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[style="color:#4b4c4f;"]')))[0]
                    dawssw_text = dawssw.text
                except:
                    pass

                try:
                    holdss = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[aria-label='" + dawssw_text + "like, double tap and hold for more reactions'")))
                except:
                    continue

                while True:
                    try:
                        touch_input = PointerInput(interaction.POINTER_TOUCH, 'touch')
                        break
                    except:
                        pass

                while True:
                    try:
                        actions.w3c_actions = ActionBuilder(driver, mouse=touch_input)
                        break
                    except:
                        pass
                try:
                    actions.w3c_actions.pointer_action.click_and_hold(holdss)
                except:
                    continue

                actions.perform()
                time.sleep(3)
                actions.reset_actions()
                time.sleep(0.3)

                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='" + reaction + "']"))).click()
                    print(x["deviceID"] + " " + x["profile"] + " " + link + " " + reaction + " " + "React Done")
                    time.sleep(5)
                except:
                    continue

        if 'Comment' in x and x["Comment"] == "yes":
            actions = ActionChains(driver)
            for comments in x.get("comment_link", "").split(" "):
                send_comments = fetch_random_comment_by_category(category=x["category"], number=1)
                while True:
                    try:
                        driver.get(comments)
                        break
                    except:
                        handle_device_tasks(device_id, android_device_serial)

                while True:
                    try:
                        time.sleep(5)
                        comms = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-mcomponent="MInputBox"]')))
                        time.sleep(0.3)
                        actions.send_keys_to_element(comms, send_comments).perform()
                        time.sleep(0.3)
                        break
                    except:
                        handle_device_tasks(device_id, android_device_serial)

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
                        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[style="color:#65676b;"]')))
                        time.sleep(5)
                        print(x["deviceID"] + " " + x["profile"] + " " + comments + " " + "Comment done")
                        break
                    except:
                        pass

        if 'share' in x and x["share"] == "yes":
            for share in x.get("links_to_share", "").split(" "):
                subprocess.check_output(
                    "adb -s " + " " + android_device_serial + " " + "shell ime set com.emoji.keyboard.touchpal/com.cootek.smartinput5.TouchPalIME",
                    shell=True)
                actionsdawdaw = ActionChains(driver)
                driver.get('https://m.facebook.com/composer/')
                whats_on_your_mind_click = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[style="color:#666666;"]')))
                whats_on_your_mind = whats_on_your_mind_click[0]
                time.sleep(3)
                actionsdawdaw.send_keys_to_element(whats_on_your_mind, share).perform()
                time.sleep(3)
                try:
                    subprocess.check_output("adb -s" + " " + android_device_serial + " " + "shell input keyevent 4", shell=True)
                except:
                    pass
                subprocess.check_output("adb -s " + " " + android_device_serial + " " + "shell ime set com.wparam.nullkeyboard/.NullKeyboard", shell=True)

                time.sleep(5)
                whats_on_your_mind_clicks = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[style="color:#666666;"]')))
                whats_on_your_mind_clear = whats_on_your_mind_clicks[0]
                actiondawdaws = ActionChains(driver)
                actiondawdaws.click(whats_on_your_mind_clear).perform()
                while True:
                    try:
                        time.sleep(0.3)
                        subprocess.check_output("adb -s " + " " + android_device_serial + " " + "shell input keyevent --longpress 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67 67",shell=True)
                        break
                    except:
                        pass

                time.sleep(0.3)
                postss_click = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[style="color:#1877f2;"]')))
                time.sleep(0.3)
                actionsdawdaw.click(postss_click[0]).perform()
                print(x["deviceID"] + " " + x["profile"] + " " + share + " " + "Share Done")
        while True:
            try:
                driver.delete_all_cookies()
                break
            except:
                pass
        continue

def run_on_multiple_devices():
    # Use ThreadPoolExecutor to run tasks in parallel across multiple devices
    with ThreadPoolExecutor(max_workers=len(device_ids)) as executor:
        # Pass device_id and the corresponding serial number
        executor.map(lambda device_id: handle_device_tasks(device_id, android_device_serials[device_ids.index(device_id)]), device_ids)

# Call the function to run tasks across all devices
run_on_multiple_devices()
0
