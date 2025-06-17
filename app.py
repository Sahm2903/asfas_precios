from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

app = Flask(__name__)

@app.route('/scraper',methods=['GET'])
def run_scraper():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.petroperu.com.pe/productos/lista-de-precios-en-nuestras-plantas/")

    indicador = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH,"//*[@id='objContents']/ul/li[1360]/div[1]/div[2]/a/span"))
    )
    indicador_text = indicador.text.strip()

    time.sleep(2)

    indicador_1 = WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.XPATH,"//*[@id='objContents']/ul/li[1360]/div[1]/div[2]/a"))
    )
    url = indicador_1.get_attribute("href")
    driver.quit()

    if indicador_text == "27-May-2025":
        return jsonify({"message": "Sin cambios", "url": url})
    else:
        return jsonify({"message": "CAMBIOO!!!", "url": url})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
