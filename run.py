import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.expected_conditions import presence_of_element_located


with open("./config.json") as json_file:
    import json
    data = json.load(json_file)
    elements = data["elements"]


def login(driver, wait):
    wait.until(presence_of_element_located((By.XPATH, elements["loginInput"])))
    wait.until(presence_of_element_located(
        (By.XPATH, elements["passwordInput"])))
    wait.until(presence_of_element_located(
        (By.XPATH, elements["loginButton"])))

    login_input = driver.find_element_by_xpath(elements["loginInput"])
    password_input = driver.find_element_by_xpath(elements["passwordInput"])
    login_button = driver.find_element_by_xpath(elements["loginButton"])

    login_input.send_keys(data["username"])
    password_input.send_keys(data["password"])
    time.sleep(1)

    login_button.click()


def close_popup(driver, wait):
    wait.until(presence_of_element_located((By.XPATH, elements["popUp"])))
    driver.find_element_by_xpath(elements["popUp"]).click()


def open_profile(driver, wait):
    wait.until(presence_of_element_located(
        (By.XPATH, elements["profileLink"])))
    driver.find_element_by_xpath(elements["profileLink"]).click()


def load_list(driver, wait, num):
    wait.until(presence_of_element_located((By.XPATH, elements["list"])))

    current_count = 0

    while current_count < num:
        wait.until(presence_of_element_located((By.XPATH, elements["list"])))
        current_list = driver.find_elements_by_xpath(elements["list"])

        current_count = len(current_list)

        xpath = elements["list"] + f"[{current_count}]"
        wait.until(presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element_by_xpath(xpath)

        print(current_count)
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(1)
        # current_count += 1


def open_list(driver, wait, xpath):
    wait.until(presence_of_element_located((By.XPATH, xpath)))
    driver.find_element_by_xpath(xpath).click()


def get_ids(driver, wait, category):
    xpath_link = elements[category + "Link"]
    xpath_num = elements[category + "Num"]

    wait.until(presence_of_element_located((By.XPATH, xpath_link)))
    num = int(driver.find_element_by_xpath(xpath_num).text)

    open_list(driver, wait, xpath_link)
    load_list(driver, wait, num)

    list_elements = driver.find_elements_by_xpath(elements["list"])
    user_list = list()
    for i in range(len(list_elements)):
        print(i)
        xpath_id = elements["list"] + \
            f"[{str(i + 1)}]" + "/div/div/div[2]/div/a"
        user_name = driver.find_element_by_xpath(xpath_id).text
        user_list.append(user_name)

    return user_list


def unfollow(ids):
    pass


def main():
    with webdriver.Chrome() as driver:
        wait = WebDriverWait(driver, 10)
        driver.maximize_window()
        driver.get("https://instagram.com")

        login(driver, wait)
        close_popup(driver, wait)
        open_profile(driver, wait)

        followers_list = get_ids(driver, wait, "followers")
        driver.back()
        following_list = get_ids(driver, wait, "following")

        not_following = list()
        for id in following_list:
            if id not in followers_list:
                not_following.append(id)

        with open("./ids.txt", "w") as f:
            for id in not_following:
                f.write(id + "\n")


if __name__ == "__main__":
    main()
