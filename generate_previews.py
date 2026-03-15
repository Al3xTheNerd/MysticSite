from selenium import webdriver
from PIL import Image, ImageOps
from io import BytesIO
import time, requests
from atn import api_url, server_name, server_folder_name

from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict


"""
This file is an example of the API provided by the Item Listing Website.
Feel free to modify this however you see fit to achieve the results you desire.

Be aware, pings to the api are tracked, and if used excessively (more than 3 times per minute),
you access is liable to be revoked.
"""
import requests
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Item:
    id: int


def dictToItem(item: Dict[str, str]) -> Item:
    """Convert the raw JSON data of an item into an easy to use Object."""
    return Item(
            int(item["id"]))

def pullItemList() -> List[Item] | None:
    """Pull the list of Items from the Item List Website."""
    dataToPull = ["id"]
    headers = {
        "I-INCLUDED-INFO" : ";".join(dataToPull)
    }
    results = requests.get(
        f"{api_url}api/items",
        headers = headers)
    if results:
        return [dictToItem(item) for item in results.json()["data"]]
    return None


missingImages = {"icons" : [], "descriptions" : []}
items = pullItemList()



icon_file_list = [p.name for p in Path(f"/home/alexthenerd/{server_folder_name}/core/static/images/{server_name}_Icons").iterdir() if p.is_file()]
desc_file_list = [p.name for p in Path(f"/home/alexthenerd/{server_folder_name}/core/static/images/{server_name}_Descriptions").iterdir() if p.is_file()]

if items:
    for item in items:
        if f"{item.id}.png" not in icon_file_list:
            print(f"Missing Icon for {item.id}")
            missingImages["icons"].append(item.id)
        if f"{item.id}.png" not in desc_file_list:
            print(f"Missing Description for {item.id}")
            missingImages["descriptions"].append(item.id)

if len(missingImages["descriptions"]) > 0:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_window_size(2040, 1080)
    
    try:
        for itemID in missingImages["descriptions"]:
            browser.get(f"{api_url}rawitem/{itemID}")
            while True:
                script = '''return document.fonts.status;'''
                loaded = browser.execute_script(script)
                if loaded == 'loaded':
                    break
                time.sleep(.25)
            png = browser.get_screenshot_as_png()
            im = Image.open(BytesIO(png))
            imageSize = im.size
            invert_im = im.convert("RGB")
            invert_im = ImageOps.invert(invert_im)
            imageBox = invert_im.getbbox()
            cropped=im.crop(imageBox)
            cropped.save(f"/home/alexthenerd/{server_folder_name}/core/static/images/{server_name}_Descriptions/{itemID}.png")
    finally:
        browser.quit()
else:
    print("No missing descriptions, generation skipped.")
