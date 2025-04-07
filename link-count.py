import os

import json

import requests

from dotenv import load_dotenv

from urllib.parse import urlparse


def is_shorten_link(url):

    sifting = urlparse(url)
    return sifting.netloc == "vk.cc"


def shorten_link(VK_TOKEN, long_url):

    payload = {
        "access_token": VK_TOKEN,
        "v": "5.199",
        "url": long_url
    }

    response = requests.get(
        "https://api.vk.ru/method/utils.getShortLink", params=payload)

    if response.status_code != 200:
        raise Exception("Ошибка при создании ссылки")

    return response.json()["response"]["short_url"]


def count_clicks(VK_TOKEN, link):
    sifting = urlparse(link)
    shift = sifting.path
    replacement = shift.replace("/", "")

    payload = {
        "access_token": VK_TOKEN,
        "v": "5.199",
        "key": replacement
    }

    response = requests.get(
        "https://api.vk.ru/method/utils.getLinkStats", params=payload)

    if response.status_code != 200:
        raise Exception("Ошибка при создании ссылки")

    return response.json()


def main():

    load_dotenv()
    VK_TOKEN = os.getenv("VK_TOKEN_API")
    url = input("Введите ссылку:")

    try:
        if is_shorten_link(url):
            print("Это короткая ссылка.")
            short_url = url
        else:
            print("Это длинная ссылка.")
            short_url = shorten_link(VK_TOKEN, url)

        print("Короткая ссылка:", short_url)

        click_stats = count_clicks(VK_TOKEN, short_url)

        print("Статистика кликов:", click_stats)

    except KeyError:
        print("Вы ввели неправильную ссылку")


if __name__ == '__main__':
    main()
