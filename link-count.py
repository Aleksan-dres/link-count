import os

import json

import requests

from dotenv import load_dotenv

from urllib.parse import urlparse


def is_shorten_link(url):

    link = urlparse(url)
    return link.netloc == "vk.cc" and len(link.path) == 7 


def shorten_link(vk_token, url):

    payload = {
        "access_token": vk_token,
        "v": "5.199",
        "url": url
    }

    response = requests.get(
        "https://api.vk.ru/method/utils.getShortLink", params=payload)
    response.raise_for_status()

    return response.json()["response"]["short_url"]


def count_clicks(vk_token, link):
    count_link = urlparse(link)
    path_link = count_link.path
    replacement = path_link.replace("/", "")

    payload = {
        "access_token": vk_token,
        "v": "5.199",
        "key": replacement
    }

    response = requests.get(
        "https://api.vk.ru/method/utils.getLinkStats", params=payload)

    response.raise_for_status()

    return response.json()


def main():

    load_dotenv()
    vk_token = os.environ["VK_TOKEN_API"]
    url = input("Введите ссылку:")

    if is_shorten_link(url): 
        print("Это короткая ссылка")
        click_stats = count_clicks(vk_token,url) 
        print("Статистика кликов",click_stats)
    else: 
        print("Это длинная ссылка.") 
        short_url = shorten_link(vk_token, url)
        print("Короткая ссылка:", short_url)
        click_stats = count_clicks(vk_token,short_url) 
        print("Статистика кликов", click_stats)


if __name__ == '__main__':
    main() 
