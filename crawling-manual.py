from dotenv import load_dotenv
from datetime import datetime, timedelta
from src import IBKCrawler
import schedule
import argparse
import logging
import json
import time
import os

# 로깅 설정
logging.basicConfig(filename="new_crawl.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def main(args):
    with open(os.path.join(args.config_path, 'config.json')) as f:
        config = json.load(f)

    load_dotenv()
    login_id = os.getenv('login_id')
    login_pw = os.getenv('login_pw')
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 2, 5)
    delta = timedelta(days=1)

    current_date = start_date
    while current_date <= end_date:
        ibkcrawler = IBKCrawler(config)
        ibkcrawler.set_env()
        ibkcrawler.click_url()
        ibkcrawler.login(login_id, login_pw)
        print(f'로그인 성공')

        current_year = str(current_date.year)
        current_month = str(current_date.month).zfill(2)
        current_day = str(current_date.day).zfill(2)

        file_s_date = f"{current_year}-{current_month}-{current_day}"
        file_e_date = f"{current_month}-{current_day}"
        print(f'시작 날짜: {file_s_date}, 종료 날짜: {file_e_date}')

        ibkcrawler.download_file(file_s_date, file_e_date)
        print(f'파일 다운로드 성공')

        ibkcrawler.rename_file(current_year, current_month, current_day)
        current_date += delta
        print(f'current_date: {current_date}')
    ibkcrawler.quit()

if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument('--config_path', type=str, default='./config')
    cli_args = cli_parser.parse_args()
    '''                                                                                                                                                                                                              schedule.every().day.at("00:10").do(main, cli_args)                                                                                                                                                              while True:                                                                                                                                                                                                          schedule.run_pending()                                                                                                                                                                                           time.sleep(3)'''
    main(cli_args)     