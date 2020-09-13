# -*- coding: utf-8 -*-

"""
    Script Name     : rakudasu.py
    Script Summary  :
    Author          :
    Change History  :
"""

# python3 rakudasu.py -s 9:00 -e 18:00 --debug

# ////////////////////////////////////////////////////////////////////////// #
#
#  モジュールインポート
#
# ////////////////////////////////////////////////////////////////////////// #
import os
import argparse
import time
import datetime
import traceback
import shutil
from selenium import webdriver
import chromedriver_binary
# ------------------------------
#  オリジナルモジュール
# ------------------------------

# ////////////////////////////////////////////////////////////////////////// #
#
#  グローバル変数
#
# ////////////////////////////////////////////////////////////////////////// #
login_url = "https://rakudasu.jp/login"
attendances_url = "https://rakudasu.jp/Attendances"

# ////////////////////////////////////////////////////////////////////////// #
#
#  関数
#
# ////////////////////////////////////////////////////////////////////////// #
# ========================================================================== #
#  関数名: check_args
# -------------------------------------------------------------------------- #
#  説明: コマンドライン引数の受け取り
#  返り値: dict
# ========================================================================== #
def check_args():
    # ---------------------
    # コマンドライン引数の受け取り
    # ---------------------
    parser = argparse.ArgumentParser(add_help=False)

    # 引数の追加
    parser.add_argument("-s", help="start time", required=True)
    parser.add_argument("-e", help="end time", required=True)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    try:
        result = {}
        result["start_time"] = args.s
        result["end_time"] = args.e
        result["debug"] = args.debug
        result["error_code"] = 1

        return result
    except Exception as e:
        if args.debug:
            print(f"引数指定に誤りがありそうです{e}")
        return 1

# ////////////////////////////////////////////////////////////////////////// #
#
#  Rakudasu クラス
#
# ////////////////////////////////////////////////////////////////////////// #
# -------------------------------------------------------------------------- #
#  クラス名    Rakudasu
#  説明        Rakudasu 操作用クラス
#  引数1       dict(コマンドライン引数)
# -------------------------------------------------------------------------- #
class Rakudasu:
    # [Dont Touch] インスタンス変数
    def __init__(self, args):
        self.def_name = "init"
        self.start_time = args["start_time"]
        self.end_time = args["end_time"]
        self.debugflag = args["debug"]
        self._error_code = args["error_code"]
        self.log_path = f'/home/rakudasu/Log/{datetime.datetime.now()}'

        self.driver = None

    # ////////////////////////////////////////////////////////////////////// #
    #
    #  基本処理
    #
    # ////////////////////////////////////////////////////////////////////// #
    # ====================================================================== #
    #  関数名: open_chrome
    # ---------------------------------------------------------------------- #
    #  説明: chrome ブラウザを開く
    #  返り値: int
    # ====================================================================== #
    def open_chrome(self):
        self.def_name = "open_chrome"
        description = f'Processing of "{self.def_name}" function is started.'
        self.write_log("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            options = webdriver.ChromeOptions()
            # ヘッドレスモード(これで実行しないと動かない)
            options.add_argument('--headless')
            # google-chrome-stableが動くために必要(google-chrome-stableを実行すると分かるはず)
            options.add_argument('--no-sandbox')
            # --disable-gpuで描画周りが安定するらしい
            options.add_argument('--disable-gpu')
            # ウィンドウサイズの指定
            options.add_argument('--window-size=1280,1024')

            driver = webdriver.Chrome(chrome_options=options)
            self.driver = driver

            # ログ作業後処理
            message = f'Chrome open completed.'
            self.write_log("INFO", f'[ OK ] {message}')

            return 0

        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.write_log("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.write_log("FATAL", f'open_chrome: {message}')
            return self._error_code

    # ====================================================================== #
    #  関数名: url_access
    # ---------------------------------------------------------------------- #
    #  説明: rakudasu ページにアクセス
    #  返り値: int
    # ====================================================================== #
    def url_access(self):
        self.def_name = "url_access"
        description = f'Processing of "{self.def_name}" function is started.'
        self.write_log("INFO", f'[ OK ] {description}')
        description = f'open rakudasu login page({login_url}).'
        self.write_log("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            self.driver.get("https://rakudasu.jp")
            self.driver.set_page_load_timeout(5)
            self.driver.save_screenshot('./screenshot/1_screen_login.png')

            # ログ作業後処理
            message = f'page open completed.'
            self.write_log("INFO", f'[ OK ] {message}')

            return 0
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.write_log("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.write_log("FATAL", f'url_access: {message}')
            return self._error_code

    # ====================================================================== #
    #  関数名: login
    # ---------------------------------------------------------------------- #
    #  説明: ログイン
    #  返り値: int
    # ====================================================================== #
    def login(self):
        self.def_name = "login"
        description = f'Processing of "{self.def_name}" function is started.'
        self.write_log("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            self.driver.get(login_url)
            self.driver.find_element_by_id("UserMail").send_keys("s-simai@y-i-group.co.jp")
            self.driver.find_element_by_id("UserPass").send_keys("shimai0913")
            time.sleep(0.5)
            self.driver.find_element_by_class_name("submitBtn").click()
            self.driver.set_page_load_timeout(5)
            self.driver.get(attendances_url)
            self.driver.set_page_load_timeout(5)
            self.driver.save_screenshot('./screenshot/2_screen_attendances.png')

            # ログ作業後処理
            message = f'Login completed.'
            self.write_log("INFO", f'[ OK ] {message}')
            message = f'cahge rakudasu attendances page({attendances_url}).'
            self.write_log("INFO", f'[ OK ] {message}')

            return 0
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.write_log("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.write_log("FATAL", f'login: {message}')
            return self._error_code

    # ====================================================================== #
    #  関数名: add_timedata
    # ---------------------------------------------------------------------- #
    #  説明: 出勤、退勤時間を入力
    #  返り値: int
    # ====================================================================== #
    def add_timedata(self):
        self.def_name = "add_time_data"
        description = f'Processing of "{self.def_name}" function is started.'
        self.write_log("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            # 今日の日付をクリック
            checkbox_list = self.driver.find_elements_by_name("checked_days")
            dt_now = datetime.datetime.now()
            today = dt_now.day
            box_day = checkbox_list[int(today) - 1]
            box_day.click()
            time.sleep(1)
            self.driver.save_screenshot('./screenshot/3_today_click.png')
            # 一括登録ボタンクリック
            self.driver.find_element_by_id("multi-registration-btn").click()
            time.sleep(1)
            self.driver.save_screenshot('./screenshot/4_all_submit_click.png')

            # 開始、終了、休憩時間を入力
            self.driver.find_element_by_class_name("work-type-9").click()
            time.sleep(1)
            self.driver.find_element_by_name("opening_time").click()
            self.driver.find_element_by_name("opening_time").clear()
            self.driver.find_element_by_name("opening_time").send_keys(self.start_time)
            self.driver.find_element_by_class_name("ui-timepicker-close").click()
            time.sleep(1)

            self.driver.find_element_by_name("closing_time").click()
            self.driver.find_element_by_name("closing_time").clear()
            self.driver.find_element_by_name("closing_time").send_keys(self.end_time)
            self.driver.find_element_by_class_name("ui-timepicker-close").click()
            time.sleep(1)

            self.driver.find_element_by_name("break_time").click()
            self.driver.find_element_by_name("break_time").clear()
            self.driver.find_element_by_name("break_time").send_keys("01:00")
            time.sleep(1)
            self.driver.find_element_by_class_name("ui-timepicker-close").click()

            time.sleep(1)
            self.driver.save_screenshot('./screenshot/5_add_timedata.png')

            # 申請ボタンクリック
            self.driver.find_element_by_id("multi-attendance-apply").click()
            time.sleep(3)
            self.driver.save_screenshot('./screenshot/6_submit_completed.png')

            # ログ作業後処理
            message = f'add time data completed.'
            self.write_log("INFO", f'[ OK ] {message}')
            message = f'submit {self.start_time} ~ {self.end_time}.'
            self.write_log("INFO", f'[ OK ] {message}')


            return 0

        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.write_log("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.write_log("FATAL", f'add time data: {message}')
            return self._error_code


    # ====================================================================== #
    #  関数名: write_log
    # ---------------------------------------------------------------------- #
    #  説明: ログ
    # ====================================================================== #
    def write_log(self, level, message):
        with open(self.log_path, 'a') as f:
            f.write(f'[{level}] {message}\n')
        if self.debugflag:
            print(f'[{level}] {message}')

# ========================================================================== #
#  メインパート
# ========================================================================== #
def main():
    # Logディレクトリ内を空にする
    log_dir = './Log'
    screenshot_dir = './screenshot'
    shutil.rmtree(log_dir)
    shutil.rmtree(screenshot_dir)
    os.mkdir(log_dir)
    os.mkdir(screenshot_dir)

    # コマンドライン引数の受け取り
    args = check_args()
    assert args != 1, "Abnormality in argument."

    rakudasu = Rakudasu(args)
    # chrome 展開
    assert not rakudasu.open_chrome()
    # rakudasu ページアクセス
    assert not rakudasu.url_access()
    # ログイン
    assert not rakudasu.login()
    # 時間入力
    assert not rakudasu.add_timedata()




if __name__ == "__main__":
    main()
