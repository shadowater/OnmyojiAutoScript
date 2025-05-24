from ast import Return
import json
import os
import time
from numpy import random
from time import sleep
from PIL import Image
from datetime import datetime

import sys
cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)
from tasks.Restart.login import LoginHandler as login_task
from tasks.Restart.script_task import ScriptTask as restart_task
from tasks.DemonEncounter.script_task import ScriptTask as demon_task
from tasks.DailyTrifles.script_task import ScriptTask as trifles_task
from tasks.TalismanPass.script_task import ScriptTask as talisman_task
from tasks.Component.SwitchAccount.switch_account import SwitchAccount
from tasks.Component.SwitchAccount.switch_account_config import AccountInfo
from tasks.AreaBoss.script_task import ScriptTask as areaboss_task
from tasks.Exploration.script_task import ScriptTask as exploration_task
from tasks.Component.GeneralInvite.assets import GeneralInviteAssets
from tasks.WantedQuests.assets import WantedQuestsAssets
from tasks.MultiAccount.assets import MultiAccountAssets
from tasks.GlobalGame.assets import GlobalGameAssets
from tasks.MysteryShop.assets import MysteryShopAssets
from tasks.GameUi.page import page_main, page_demon_encounter, page_guild
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
        if demon.appear_then_click(WantedQuestsAssets.I_WQ_SEAL, interval=3):
            continue
        if demon.appear_then_click(WantedQuestsAssets.I_WQ_DONE, interval=3):
            continue
        
    demon.screenshot() 
    img = Image.fromarray(demon.device.image, mode='RGB')
    img.save(cur_path.split("OnmyojiAutoScript")[0] + f"{key}_{value}_wantedquests.png")
    demon.ui_click_until_disappear(GlobalGameAssets.I_UI_BACK_RED, 2)
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
        img.save(cur_path.split("OnmyojiAutoScript")[0] + f"{key}_{value}_mysteryshop.png")
            
        sleep(random.random()+0.5)
        demon.ui_click(demon.I_BACK_Y ,demon.I_BACK_BLUE)
        sleep(random.random()+0.5)
        demon.ui_click(demon.I_BACK_BLUE ,demon.I_CHECK_MAIN)


def donate_guild():
    # 进入寮页面，寮信息，寮捐赠，增加勾玉数量，确定捐赠
    demon.ui_goto(page_guild)
    demon.ui_click(MultiAccountAssets.I_GUILD_INFO, MultiAccountAssets.I_DONATE, interval=2)
    demon.click(MultiAccountAssets.I_DONATE, interval=1)
    demon.ui_click(MultiAccountAssets.I_DONATE_ADD, MultiAccountAssets.I_DONATE_SURE, interval=0.5)
    demon.click(MultiAccountAssets.I_DONATE_SURE)
    time.sleep(1)
    demon.click(demon.I_UI_BACK_YELLOW)
    demon.click(demon.I_UI_BACK_YELLOW)
    demon.ui_goto(page_main)


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

def add_team_source(cur_task):
    # 主页主队，同心队，同心队中心，一键寄存，确认，回到主页
    
    if cur_task.ui_get_current_page() != page_main:
        cur_task.ui_goto(page_main)
        
    cur_task.ui_click(cur_task.I_HOME_TEAM, cur_task.I_CHECK_TEAM, 1.5)
    cur_task.ui_click(cur_task.I_CHECK_TEAM, MultiAccountAssets.I_TEAM_HOME, 1.5)
    cur_task.ui_click(MultiAccountAssets.I_TEAM_HOME, MultiAccountAssets.I_ONE_STEP_SOURCE, 1.5)
    cur_task.ui_click(MultiAccountAssets.I_ONE_STEP_SOURCE, GeneralInviteAssets.I_GI_SURE, 1.5)
    cur_task.ui_click_until_disappear(GeneralInviteAssets.I_GI_SURE, 1.5)
    
    if cur_task.ui_get_current_page() != page_main:
        cur_task.ui_goto(page_main)

import pandas as pd

cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]

daliy_json = oas_path + "\\tasks\\MultiAccount\\multi_daily_temp.json"
target_json = oas_path + "\\config\\multi_account.json"
os.system(f'copy {daliy_json} {target_json}')
# sleep(3600*12)

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
exploration = exploration_task(config, device)
continue_flag =True

task_list = [areaboss, talisman, trifles]

account_data = pd.read_csv(oas_path + "\\tasks\\MultiAccount\\account_info.csv")
account_data.replace("and", True, inplace=True)
account_data.replace("ios", False, inplace=True)
account_data.fillna("", inplace=True)

for ii in account_data.iterrows():
    ii = ii[1]

    # if "队长" not in ii["team"]:
    #     continue
    print(ii)
    try:
        toAccount=AccountInfo(account=ii["account"], apple_or_android=ii["system"],
                                character=ii["character"], svr="网易一" + ii["server"])
        sa=SwitchAccount(config,device,toAccount)
        sa.switchAccount()
   
        ## run task 
        for cur_task in task_list:
            try:
                cur_task.run()
            except Exception as e:
                logger.error(f"Task {cur_task} finished")
                
        if demon.ui_get_current_page() != page_main:
            demon.ui_goto(page_main)
            
    except Exception as e:
        restart_task.app_stop()
        logger.error(f"Account {ii['name']} failed")
        break

    # 下一个账号
    if continue_flag:
        sleep(10+random.random()*5)
    else:
        input("Press Enter to continue...")
        
restart_task.app_stop()