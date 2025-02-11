from dotenv import load_dotenv
from datetime import datetime
from src import IBKCrawler
import schedule
import argparse
import logging
import json
import time
import os 

# 로깅 설정
logging.basicConfig(filename="selenium.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def main(args):
    with open(os.path.join(args.config_path, 'config.json')) as f:
        config = json.load(f)

    load_dotenv()
    login_id = os.getenv('login_id')
    login_pw = os.getenv('login_pw')

    ibkcrawler = IBKCrawler(config)
    ibkcrawler.set_env()
    ibkcrawler.click_url()
    ibkcrawler.login(login_id, login_pw)
    print(f'로그인 성공')

    now = datetime.now()
    current_year = now.year
    current_month = now.month 
    current_day = now.day - 1
    
    start_date = f"{current_year}-{current_month}-{current_day}"
    end_date = f"{current_year}-{current_month}-{current_day}"
    print(f'시작 날짜: {start_date}, 종료 날짜: {end_date}')
    ibkcrawler.download_file(start_date, end_date)
    print(f'파일 다운로드 성공')
    
    ibkcrawler.rename_file(current_year, current_month, current_day)
    ibkcrawler.quit()

if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument('--config_path', type=str, default='./config')
    cli_args = cli_parser.parse_args()
    
    schedule.every().day.at("00:10").do(main, cli_args)
    '''while True:
        schedule.run_pending()
        time.sleep(3)'''
    main(cli_args)
