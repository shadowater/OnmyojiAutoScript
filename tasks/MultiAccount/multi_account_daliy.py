from ast import Return
import json
import os
from numpy import random
from time import sleep
from PIL import Image
from datetime import datetime

import sys
sys.path.append("D:\\software\\yys\\OnmyojiAutoScript")
from tasks.Restart.login import LoginHandler as login_task
from tasks.Restart.script_task import ScriptTask as restart_task
from tasks.DemonEncounter.script_task import ScriptTask as demon_task
from tasks.DailyTrifles.script_task import ScriptTask as trifles_task
from tasks.TalismanPass.script_task import ScriptTask as talisman_task
from tasks.Component.SwitchAccount.switch_account import SwitchAccount
from tasks.Component.SwitchAccount.switch_account_config import AccountInfo
from tasks.AreaBoss.script_task import ScriptTask as areaboss_task

from tasks.WantedQuests.assets import WantedQuestsAssets
from tasks.MultiAccount.assets import MultiAccountAssets
from tasks.GlobalGame.assets import GlobalGameAssets
from tasks.MysteryShop.assets import MysteryShopAssets
from tasks.GameUi.page import page_main, page_demon_encounter
from module.config.config import Config
from module.device.device import Device
from module.atom.click import RuleClick
from module.logger import logger
from module.base.timer import Timer

def screenshot_wantedquests():
    while 1:
        demon.screenshot()
        if demon.appear(WantedQuestsAssets.I_TRACE_ENABLE) or demon.appear(WantedQuestsAssets.I_TRACE_DISABLE):
            break
        if demon.appear_then_click(WantedQuestsAssets.I_WQ_SEAL, interval=1):
            continue
        
    demon.screenshot() 
    img = Image.fromarray(demon.device.image, mode='RGB')
    img.save(f"D:\\Software\\yys\\MultiAccount\\wantedquests\\{key}_{value}.png")
    demon.ui_click_until_disappear(GlobalGameAssets.I_UI_BACK_RED)
    sleep(random.random()+0.5)

def screenshot_mysteryshop():
    day_of_week = datetime.now().weekday()
    if day_of_week != 2 and day_of_week != 5:
        logger.warning('Today is not MysteryShop day')
    else:
        demon.ui_click(demon.I_MAIN_GOTO_MALL ,demon.I_BACK_Y)
        sleep(random.random()+0.5)
        demon.ui_click(demon.I_BACK_Y ,demon.I_BACK_BLUE)
        sleep(random.random()+0.5)
        demon.ui_click(demon.I_BACK_Y , MysteryShopAssets.I_ME_ENTER)
        sleep(random.random()+0.5)
        demon.ui_click(MysteryShopAssets.I_ME_ENTER, MysteryShopAssets.I_MS_SHARE)
        logger.info('Enter MysteryShop')
            
        # refresh = RuleClick((1199,533,55,54), (1199,533,55,54))
        # have_blue = demon.appear(MysteryShopAssets.I_MS_BLUE)
        # have_black = demon.appear(MysteryShopAssets.I_MS_BLACK)
        # if not have_blue and not have_black:
        #     demon.click(refresh)
        #     demon.click(kekkai.I_UI_CONFIRM_SAMLL)
        
        demon.screenshot() 
        img = Image.fromarray(demon.device.image, mode='RGB')
        img.save(f"D:\\Software\\yys\\MultiAccount\\mysteryshop\\{key}_{value}.png")
            
        sleep(random.random()+0.5)
        demon.ui_click(demon.I_BACK_Y ,demon.I_BACK_BLUE)
        sleep(random.random()+0.5)
        demon.ui_click(demon.I_BACK_BLUE ,demon.I_CHECK_MAIN)

def lantern_task():

    if not demon.check_time():
        logger.warning('Time is not right')
        return 0
    
    demon.ui_get_current_page()
    demon.ui_goto(page_demon_encounter)

    ocr_timer = Timer(0.8)
    ocr_timer.start()
    while 1:
        demon.screenshot()
        if not ocr_timer.reached():
            continue
        else:
            ocr_timer.reset()
        cu, re, total = demon.O_DE_COUNTER.ocr(demon.device.image)
        if cu + re != total:
            logger.warning('Lantern count error')
            continue
        if cu == 0 and re == 4:
            break

        if demon.appear_then_click(demon.I_DE_FIND, interval=2.5):
            continue
    logger.info('Lantern count success')
    # 然后领取红色达摩
    demon.screenshot()
    if not demon.appear(demon.I_DE_AWARD):
        demon.ui_get_reward(demon.I_DE_RED_DHARMA)
    demon.wait_until_appear(demon.I_DE_AWARD)
    demon.ui_goto(page_main)


daliy_json = "D:\\software\\yys\\OnmyojiAutoScript\\tasks\\MultiAccount\\multi_daily_temp.json"
target_json = "D:\\software\\yys\\OnmyojiAutoScript\\config\\multi_account.json"
os.system(f'copy {daliy_json} {target_json}')
account_data = json.load(open("D:\\software\\yys\\OnmyojiAutoScript\\tasks\\MultiAccount\\account_info_temp.json", 'rb'))

# try start app
config = Config('multi_account')
device = Device(config)
restart_task = restart_task(config, device)
restart_task.app_start()

# loop in multi account
login = login_task(config, device)
multi_account = MultiAccountAssets()

demon = demon_task(config, device)
trifles = trifles_task(config, device)
areaboss = areaboss_task(config, device)
talisman = talisman_task(config, device)

task_list = [trifles, areaboss, talisman]
run_task_indices = []
continue_flag = True

task_list = [task_list[ii] for ii in range(len(task_list)) if ii in run_task_indices]
for key, value in account_data.items():
    # continue
    
    try:
        ## switch account
        and_or_ios = True if "and" in key else False
        character = key.split("#")[-1]
        
        toAccount=AccountInfo(account=value, apple_or_android=and_or_ios,
                                character=character, svr="孤高之心")
        sa=SwitchAccount(config,device,toAccount)
        sa.switchAccount()

        lantern_task()
                
        ## run task 
        for cur_task in task_list:
            try:
                cur_task.run()
            except Exception as e:
                logger.error(f"Task {cur_task} finished")
                
        if demon.ui_get_current_page() != page_main:
            demon.ui_goto(page_main)

        # 截个图，看看勾协和蓝屏黑蛋
        # value = value.replace("*", "x")
        # if not os.path.exists(f"D:\\Software\\yys\\MultiAccount\\wantedquests\\{key}_{value}.png"):
        #     screenshot_wantedquests()
        # if not os.path.exists(f"D:\\Software\\yys\\MultiAccount\\mysteryshop\\{key}_{value}.png"):
        #     screenshot_mysteryshop()
            
    except Exception as e:
        logger.error(f"Account {key} failed")
        continue_flag = True
        input("Need human intervention...")

    # 下一个账号
    if continue_flag:
        sleep(10+random.random()*5)
    else:
        input("Press Enter to continue...")
        
restart_task.app_stop()