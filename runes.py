import io
from selenium import webdriver
from PIL import Image

def get_runes(champ, lane, dark_mode):
    google_chrome_options = webdriver.chrome.options.Options()
    google_chrome_options.headless = True
    google_chrome_options.add_argument('--window-size=568,300')
    web_driver = webdriver.Chrome(
        executable_path="/usr/bin/chromedriver",
        options=google_chrome_options
    )
    url = f"https://op.gg/champion/{champ}/statistics/{lane}"
    web_driver.get(url)
    element = web_driver.find_element_by_class_name('perk-page-wrap')
    element = element.screenshot_as_png
    web_driver.close()

    img = Image.open(io.BytesIO(element))
    if dark_mode is True:
        img = img.convert("RGBA")
        data = img.getdata()

        new_data = []
        for item in data:
            if item[0] == 245 and item[1] == 245 and item[2] == 245:
                new_data.append((0, 0, 255, 0))
            else:
                new_data.append(item)
        
        img.putdata(new_data)
    
    return img
