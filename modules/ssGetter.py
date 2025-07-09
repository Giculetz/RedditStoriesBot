import json
import os
import time
from io import BytesIO
from PIL import Image, ImageDraw
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def generate_reddit_post_screenshot(html_path, title_text, output_image_path):
    # Setare headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--window-size=1200,1000")  # destul de mare pt tot conținutul
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--disable-software-rasterizer")

    driver = webdriver.Chrome(options=chrome_options)

    html_abs_path = os.path.abspath(html_path).replace("\\", "/")
    driver.get(f"file:///{html_abs_path}")
    time.sleep(1)

    # Schimbă titlul
    title_elem = driver.find_element(By.CSS_SELECTOR, ".title")
    driver.execute_script(f"arguments[0].textContent = `{title_text}`", title_elem)
    time.sleep(0.5)

    # Găsește elementul .post
    post_elem = driver.find_element(By.CSS_SELECTOR, ".post")

    # Coordonatele elementului
    location = post_elem.location
    size = post_elem.size

    # Screenshot complet
    png = driver.get_screenshot_as_png()
    driver.quit()

    # Decupare la .post și conversie la RGBA pentru transparență
    image = Image.open(BytesIO(png)).convert("RGBA")
    left = int(location['x'])
    top = int(location['y'])
    right = int(location['x'] + size['width'])
    bottom = int(location['y'] + size['height'])
    cropped = image.crop((left, top, right, bottom))

    # Aplică mască circulară pt colțuri rotunjite (exactă)
    radius = 30  # pixelii de rotunjire
    mask = Image.new('L', cropped.size, 255)
    corner = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(corner)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

    # Adaugă colțurile rotunjite la mască
    mask.paste(corner.crop((0, 0, radius, radius)), (0, 0))
    mask.paste(corner.crop((radius, 0, radius * 2, radius)), (cropped.width - radius, 0))
    mask.paste(corner.crop((0, radius, radius, radius * 2)), (0, cropped.height - radius))
    mask.paste(corner.crop((radius, radius, radius * 2, radius * 2)), (cropped.width - radius, cropped.height - radius))

    # Aplică masca peste imaginea finală
    cropped.putalpha(mask)

    # Salvează imaginea PNG cu transparență
    cropped.save(output_image_path, format="PNG")

def ss_getter():
    html_path= 'RedditPostImage/Site/post.html'
    os.makedirs("temps/RedditImages", exist_ok=True)
    with open('stories.json', 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    for index,el in enumerate(data,start=1):
        print(f"se proceseaza {el['title']}")
        generate_reddit_post_screenshot(
            html_path,
            el['title'],
            f'temps/RedditImages/Story{index}.png'
        )
