import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from pyquery import PyQuery as pq


class Crack_JD_Test():
    def __init__(self):
        self.url = 'https://account.aliyun.com/register/register.htm?spm=5176.8142029.388261.24.3dbd6d3e4CJEKC&oauth_callback=https%3A%2F%2Fwww.aliyun.com%2F%3Futm_content%3Dse_1000301881'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)

    def get_slider(self):
        self.browser.get(self.url)
        slider = self.wait.until(EC.presence_of_element_located((By.ID, 'nc_1__bg')))
        return slider

    def move_to_right(self, slider):
        ActionChains(self.browser).click_and_hold(slider).perform()
        ActionChains(self.browser).move_by_offset(xoffset=10, yoffset=0).perform()
        ActionChains(self.browser).release().perform()

c = Crack_JD_Test()
slider = c.get_slider()
c.move_to_right(slider)

