import selenium.common.exceptions
from imap_tools import MailBox, AND
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from configparser import ConfigParser
import os.path
from concurrent.futures import ThreadPoolExecutor
import signal
from functools import partial
from threading import Event
from urllib.request import urlopen
import time

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

progress = Progress(
    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn()

)

done_event = Event()


def handle_sigint(signum, frame):
    done_event.set()


signal.signal(signal.SIGINT, handle_sigint)


def copy_url(task_id: TaskID, url: str, path: str) -> None:
    """Copy data from a url to a local file."""
    response = urlopen(url)
    # This will break if the response doesn't contain content length
    progress.update(task_id, total=int(response.info()["Content-length"]))
    test_list = url.split('?', 1)
    extension = test_list[0][-3:]
    with open(path+"."+extension, "wb") as dest_file:
        progress.start_task(task_id)
        for data in iter(partial(response.read, 32768), b""):
            dest_file.write(data)
            progress.update(task_id, advance=len(data))
            if done_event.is_set():
                return


def pop(em_file):
    with open(em_file, 'r+') as f:  # open file in read / write mode
        firstLine = f.readline()  # read the first line and throw it out
        data = f.read()  # read the rest
        f.seek(0)  # set the cursor to the top of the file
        f.write(data)  # write the data back
        f.truncate()  # set the file size to the current size
        return firstLine


if __name__ == '__main__':
    print("Initializing Program:\nPlease Wait 5 seconds:", end="")
    cp = ConfigParser()
    cp.read("scripts/config.ini")
    config = cp["CONFIGURATIONS"]
    res = config["resolution"]
    path_name = config["folder_path"]
    mail = pop("scripts/emails.txt")
    options = Options()
    options.headless = "True" == config["headless"]
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    alta = webdriver.Chrome(options=options)
    alta.get('https://altaregistrazione.net/')
    time.sleep(3)
    mail_slot = alta.find_element(by="xpath",
                                  value="/html/body/div/div/main/div/div[4]/div/div/div[2]/div[1]/form/div[1]/div/div[1]/div/input")
    password_slot = alta.find_element(by="xpath",
                                      value="/html/body/div/div/main/div/div[4]/div/div/div[2]/div[1]/form/div[2]/div/div[1]/div/input")
    confirm_password_slot = alta.find_element(by="xpath",
                                              value="/html/body/div/div/main/div/div[4]/div/div/div[2]/div[1]/form/div[3]/div/div[1]/div/input")
    one_day_button = alta.find_element(by="xpath",
                                       value="/html/body/div/div/main/div/div[4]/div/div/div[2]/div[1]/form/div[4]/div/div[1]/div/div/div[2]/div[1]/div/div/div")
    register = alta.find_element(by="xpath", value="/html/body/div/div/main/div/div[4]/div/div/div[2]/div[2]/button")

    mail_slot.send_keys(mail)
    password_slot.send_keys("123456")
    confirm_password_slot.send_keys("123456")

    one_day_button.click()
    register.click()
    print("Logging In:\nPlease Wait 30 seconds:", end="")
    time.sleep(15)
    mailbox = MailBox('imap.gmail.com').login(config["email"], config["token"])
    uid = 0
    urls = []
    for msg in mailbox.fetch():
        uid = msg.uid
        soup = BeautifulSoup(msg.html, 'html.parser')

        urls = []
        for link in soup.find_all('a'):
            urls.append(link.get('href'))
    mailbox.delete(uid)
    alta.get(urls[0])
    time.sleep(3)
    alta.get("https://altadefinizionecommunity.online/")
    time.sleep(4)
    remove_popup = alta.find_element(By.XPATH, '/html/body/div/div[3]/div/div/div[2]/div[1]/button/span/i')
    remove_popup.click()

    if res != "4K":
        alta.find_element(By.XPATH, '/html/body/div/div/span/header/div/div[5]/button').click()
        time.sleep(1)
        alta.find_element(By.XPATH, '/html/body/div/div[3]/div/div/a[1]').click()
        time.sleep(1)
        alta.find_element(By.XPATH,
                          '/html/body/div/div[1]/main/div/div[4]/div[2]/div[2]/div/div[5]/div[3]/div[4]/div/div[1]/div[1]/div[1]/input').send_keys(
            res + Keys.ENTER)
        time.sleep(1)
        alta.find_element(By.XPATH, '/html/body/div/div[3]/div/div[3]').click()
        time.sleep(1)
        alta.find_element(By.XPATH,
                          '/html/body/div/div[1]/main/div/div[4]/div[2]/div[2]/div/div[5]/div[4]/button').click()
    time.sleep(1)
    with open("film_list.txt") as file:
        film_list = file.read().splitlines()
    dictionary = {}
    if len(film_list) != 0 and config["headless"] == "True":
        print("Starting Downloads:\nPlease Wait 15 seconds:", end="")
        with progress:
            with ThreadPoolExecutor() as pool:
                for film_name in film_list:
                    alta.get("https://altadefinizionecommunity.online/")
                    time.sleep(3)
                    see_search_bar = alta.find_element(By.XPATH, '/html/body/div/div/span/header/div/button[3]')
                    see_search_bar.click()
                    write_search = alta.find_element(By.XPATH,
                                                     '/html/body/div/div/span/header/div/div/div[1]/div/div[1]/input[1]')
                    write_search.send_keys(film_name + Keys.ENTER)
                    time.sleep(4)
                    try:
                        film_box = alta.find_element(By.XPATH,
                                                     '/html/body/div/div/main/div/div[4]/div[2]/div[1]/div/div[2]/div/div[3]/div')
                        film_box.click()
                        time.sleep(1)
                        film_player = alta.find_element(By.XPATH,
                                                        '/html/body/div/div[3]/div/div/div[2]/div[1]/div/button')
                        film_player.click()
                        time.sleep(1)
                        wrong_url = alta.current_url
                        film_page_url = wrong_url.replace("/cd/", "/play/")
                        alta.get(film_page_url)
                        time.sleep(3)
                        video_link = alta.find_element(by="xpath",
                                                       value="/html/body/div/div/main/div/div[4]/div[5]/div[2]/div/video").get_property(
                            "src")
                        dest_path = os.path.join(path_name, film_name)
                        task_id = progress.add_task("download", filename=film_name, start=False)
                        pool.submit(copy_url, task_id, video_link, dest_path)
                    except selenium.common.exceptions.NoSuchElementException:
                        pass
                    time.sleep(3)
                alta.quit()
    else:
        while True:
            time.sleep(1)
