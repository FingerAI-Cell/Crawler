from dotenv import load_dotenv
from datetime import datetime, timedelta
from src import IBKCrawler
from apscheduler.schedulers.background import BackgroundScheduler
import argparse
import json
import time
import os 

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
    current_year = str(now.year)
    current_month = str(now.month).zfill(2)
    current_day = str(now.day).zfill(2)
    
    start_date = f"{current_year}-{current_month}-{current_day}"
    end_date = f"{current_year}-{current_month}-{current_day}"
    print(f'시작 날짜: {start_date}:{now.hour}')
    ibkcrawler.download_file(start_date, end_date)
    print(f'파일 다운로드 성공')
    
    ibkcrawler.rename_file(current_year, current_month, current_day)
    ibkcrawler.quit()

if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument('--config_path', type=str, default='./config')
    cli_args = cli_parser.parse_args()
    scheduler = BackgroundScheduler()
    scheduler.add_job(main, 'interval', hours=1, args=[cli_args])
    scheduler.start() 
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()
