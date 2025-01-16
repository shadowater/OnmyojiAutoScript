import json
import os
from numpy import random
from time import sleep
from datetime import datetime

import sys
sys.path.append("D:\\Software\\yys\\bot\\OnmyojiAutoScript-easy-install")
from tasks.Restart.login import LoginHandler as login_task
from tasks.Restart.script_task import ScriptTask as restart_task
from tasks.DemonEncounter.script_task import ScriptTask as demon_task
from tasks.DailyTrifles.script_task import ScriptTask as trifles_task
from tasks.TalismanPass.script_task import ScriptTask as talisman_task
from tasks.KekkaiUtilize.script_task import ScriptTask as kekkai_task
from tasks.AreaBoss.script_task import ScriptTask as areaboss_task
from tasks.MultiAccount.assets import MultiAccountAssets
from tasks.GameUi.page import page_main
from module.config.config import Config
from module.device.device import Device
from module.atom.click import RuleClick
from module.logger import logger

def switch_account_by_name(script, assets, accountName):
    """
    保证在登录的界面
    :return:
    """
    logger.hr('Switch account by name')
    # 滑动至分组最上层
    last_group_text = ''
    while 1:
        script.screenshot()
        compare1 = assets.O_ACCOUNT_GROUP_NAME.detect_and_ocr(script.device.image)
        now_group_text = str([result.ocr_text for result in compare1])
        if now_group_text == last_group_text:
            break
        script.swipe(assets.S_ACCOUNT_GROUP_SWIPE_UP, 2)
        sleep(2.5)
        last_group_text = now_group_text
    logger.info('Swipe to top of group')

    # 判断有无目标分组
    while 1:
        script.screenshot()
        # 获取当前分组名
        results = assets.O_ACCOUNT_GROUP_NAME.detect_and_ocr(script.device.image)
        text1 = [result.ocr_text for result in results]
        # 判断当前分组有无目标分组
        result = set(text1).intersection({accountName})
        # 有则跳出检测
        if result and len(result) > 0:
            break
        script.swipe(assets.S_ACCOUNT_GROUP_SWIPE_DOWN)
        sleep(1.5)
    logger.info('Swipe down to find target group')

    while 1:
        script.screenshot()
        assets.O_ACCOUNT_GROUP_NAME.keyword = accountName
        if script.ocr_appear_click(assets.O_ACCOUNT_GROUP_NAME):
            break


def switch_account():
    log_out = RuleClick((27,33,65,59), (27,33,65,59))
    login.click(log_out, 1)
    sleep(random.random()*2+0.5)
    
    login.screenshot()
    login.appear_then_click(multi_account.I_USER_CENTER)
    sleep(random.random()*2+0.5)
    
    login.click(multi_account.O_SWITCH_ACCOUNT)
    sleep(random.random()*2+0.5)
    
    login.screenshot()
    login.ui_click_until_disappear(multi_account.I_PULL_DOWN_TAP)
    sleep(random.random()*2+0.5)
    
    switch_account_by_name(login, multi_account, account.keyword)
    sleep(random.random()*2+0.5)
    
    login.screenshot()
    login.ocr_appear_click(multi_account.O_LOGIN)
    sleep(random.random()*2+0.5)
    
    if "and" in key:
        login.ui_click_until_disappear(multi_account.I_ANDROID)
    elif "ios" in key:
        login.ui_click_until_disappear(multi_account.I_IOS)
        
    login.app_handle_login()


daliy_json = "D:\\Software\\yys\\bot\\OnmyojiAutoScript-easy-install\\tasks\\MultiAccount\\multi_daily_temp.json"
target_json = "D:\\Software\\yys\\bot\\OnmyojiAutoScript-easy-install\\config\\multi_account.json"
os.system(f'copy {daliy_json} {target_json}')
account_data = json.load(open("D:\\Software\\yys\\bot\\OnmyojiAutoScript-easy-install\\tasks\\MultiAccount\\account_info_temp.json", 'rb'))

# try start app
config = Config('multi_account')
device = Device(config)
restart_task = restart_task(config, device)
restart_task.app_start()

# loop in multi account
login = login_task(config, device)
multi_account = MultiAccountAssets()
account = multi_account.O_ACCOUNT
for key, value in account_data.items():
    account.name = key
    account.keyword = value
    
    if "小号" not in key:
        continue

    ## switch account
    switch_account()

    ## load config and run task
    demon = demon_task(config, device)
    try:
        demon.run()
    except Exception as e:
        # demon.execute_boss()
        logger.error(f"Task demon encounter finished")
    
    trifles = trifles_task(config, device)
    try:
        trifles.run()
    except Exception as e:
        logger.error(f"Task trifles finished")
        
    kekkai = kekkai_task(config, device)
    try:
        kekkai.run()
    except Exception as e:
        logger.error(f"Task kekkai finished")
        
    areaboss = areaboss_task(config, device)
    try:
        now = datetime.now()
        if now.hour > 7:
            areaboss.run()
    except Exception as e:
        logger.error(f"Task areaboss finished")
        
    talisman = talisman_task(config, device)
    try:
        talisman.run()
    except Exception as e:
        talisman.ui_goto(page_main)
        logger.error(f"Task talisman finished")
        
    # sleep(10+random.random()*5)
    input("Press Enter to continue...")
    