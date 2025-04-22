import os 

import argparse

import json

import requests

from dotenv import load_dotenv

from urllib.parse import urlparse


def is_shorten_link(vk_token,url):
    count_link = urlparse(url)
    path_link = count_link.path
    replacement = path_link.replace("/", "")
    
    payload = {
        "access_token": vk_token,
        "v": "5.199",
        "key": replacement
    }

    response = requests.get("https://api.vk.ru/method/utils.getLinkStats", params=payload)

    response.raise_for_status() 

    short_link = response.json()
   
    return "response" in short_link


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

    return response.json()["response"]["stats"][0]["views"]


def main():

    load_dotenv()
    vk_token = os.environ["VK_TOKEN_API"] 

    
    parser = argparse.ArgumentParser(description='Определяет длинная или короткая ссылка, если короткая то выведется сумма кликов по ней ') 
    parser.add_argument('-url', help='URL to process') 
    args = parser.parse_args() 
    
    url = args.url
    
    
    if is_shorten_link(vk_token,url): 
        click_stats = count_clicks(vk_token,url) 
        print("Статистика кликов",click_stats)
    else: 
         
         short_url = shorten_link(vk_token, url)
         print( short_url)
         

if __name__ == '__main__':
    main() 
