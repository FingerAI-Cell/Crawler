from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time
import os

# 로깅 설정
logging.basicConfig(filename="crawler.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

class Crawler():
    def __init__(self, config):
        self.config = config 

    def __set_service(self):
        self.service = Service(ChromeDriverManager().install())
    
    def __set_option(self):
        self.chrome_options = Options()
        # self.chrome_options.add_argument("--headless")  # Headless 모드 비활성화 (문제 해결 후 다시 활성화 가능)
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")  # 스크린샷 해상도 설정
        self.chrome_options.add_argument("--enable-logging")
        self.chrome_options.add_argument("--remote-debugging-port=9222")
        self.chrome_options.add_argument("--v=1")

        self.chrome_options.add_experimental_option('prefs', {
            "profile.default_content_settings.popups": 0,
            "download.default_directory": self.config['download_path'],  # 다운로드 경로 지정
            "download.prompt_for_download": False,  # 다운로드 시 경로 묻지 않음
            "directory_upgrade": True,
            "safebrowsing.enabled": True,
            "safebrowsing.disable_download_protection": True,  # 파일 다운로드 보호 비활성화
            "profile.default_content_settings.automatic_downloads": 1,
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1
        })

        # ChromeDriver에서 로그 활성화
        self.chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL', 'browser': 'ALL'})

    def __set_driver(self):
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
    
    def set_env(self):
        self.__set_service()
        self.__set_option()
        self.__set_driver()

    def click_url(self, wait_time=3):
        self.driver.get(self.config['page_url'])
        time.sleep(wait_time)

    def click_button(self, element, wait_time=3):
        try:
            element.click()
            logging.info(f"Element clicked: {element}")
            time.sleep(wait_time)
        except Exception as e:
            logging.error(f"Failed to click element {element}: {e}")

    def quit(self):
        self.driver.quit()

class IBKCrawler(Crawler):
    def __init__(self, config):
        super().__init__(config)
    
    def login(self, login_id, login_passwd):
        email_field = self.driver.find_element(By.ID, 'username')  # 해당 selector 수정 필요
        password_field = self.driver.find_element(By.ID, 'password')  # 해당 selector 수정 필요
        login_button = self.driver.find_element(By.NAME, 'action')  # NAME 속성으로 선택
        
        email_field.send_keys(login_id)  
        password_field.send_keys(login_passwd)
        self.click_button(login_button)
    
    def download_file(self, start_date, end_date, wait_time=1):
        download_page_button = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/div[2]/div')
        self.click_button(download_page_button)   

        # start_date_field = self.driver.find_element(By.XPATH, '//input[@type="date"]')
        start_date_field = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[3]/div/div[3]/input')
        start_date_field.clear()
        start_date_field.send_keys(f"{start_date}")   # "09-03"
        time.sleep(wait_time)  # 작은 지연 시간 추가   

        # end_date_field = self.driver.find_element(By.XPATH, '(//input[@type="date"])[2]')
        end_date_field = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[3]/div/div[4]/input')
        end_date_field.clear()
        end_date_field.send_keys(f"{end_date}")
        time.sleep(wait_time)  # 작은 지연 시간 추가

        file_download_button = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[3]/div/button')
        self.click_button(file_download_button)
    
    def rename_file(self, year, month, day):
        download_date = str(year) + str(month).zfill(2) + str(day).zfill(2)
        old_file = f"aianalyst_ibks-log_{download_date}-{download_date}.xlsx"
        new_file = f"ibk-convlog_{download_date}.xlsx"
        try:
            os.rename(os.path.join(self.config['download_path'], old_file), os.path.join(self.config['download_path'], new_file))
            logging.info(f"파일 이름이 {old_file}에서 {new_file}으로 변경되었습니다.")
        except FileNotFoundError:
            logging.error(f"파일 {old_file}을(를) 찾을 수 없습니다.")
        except Exception as e:
            logging.error(f"파일 이름 변경 중 오류가 발생했습니다: {e}")
