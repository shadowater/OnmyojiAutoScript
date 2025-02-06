from ast import Return
import json
import os
from numpy import random
from time import sleep
from PIL import Image
from datetime import datetime

import sys
sys.path.append("D:\\softwa\\yys\\OnmyojiAutoScript-easy-install")
from tasks.Restart.login import LoginHandler as login_task
from tasks.Restart.script_task import ScriptTask as restart_task
from tasks.DemonEncounter.script_task import ScriptTask as demon_task
from tasks.DailyTrifles.script_task import ScriptTask as trifles_task
from tasks.TalismanPass.script_task import ScriptTask as talisman_task
from tasks.Component.SwitchAccount.switch_account import SwitchAccount
from tasks.Component.SwitchAccount.switch_account_config import AccountInfo
from tasks.AreaBoss.script_task import ScriptTask as areaboss_task
from tasks.Orochi.script_task import ScriptTask as orochi_task

# from tasks.GameUi.assets import GameUiAssets
from tasks.Component.GeneralInvite.assets import GeneralInviteAssets
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
    
def connect_team_30(cur_task: orochi_task, switch_out=False):
    # 主页主队，同心队, 集结，御魂副本集结，副本， 创建队伍，开加成，开自动，run，取消，退出组队，回到主页
    if cur_task.ui_get_current_page() != page_main:
        cur_task.ui_goto(page_main)
    [cur_task.I_HOME_TEAM, cur_task.I_CHECK_TEAM, MultiAccountAssets.I_UNION,
     MultiAccountAssets.I_YUHUN_UNION, MultiAccountAssets.I_MISSION, MultiAccountAssets.I_AUTO,
     GeneralInviteAssets.I_GI_CANCEL, ]
    
    cur_task.ui_click(cur_task.I_HOME_TEAM, cur_task.I_CHECK_TEAM, 1.5)
    cur_task.ui_click(cur_task.I_CHECK_TEAM, MultiAccountAssets.I_UNION, 1.5)
    cur_task.ui_click(MultiAccountAssets.I_UNION, MultiAccountAssets.I_YUHUN_UNION, 1.5)
    cur_task.ui_click_until_disappear(MultiAccountAssets.I_YUHUN_UNION, 1.5)
    cur_task.ui_click_until_disappear(MultiAccountAssets.I_MISSION, 1.5)
    
    cur_task.create_room()
    cur_task.ensure_private()
    cur_task.create_ensure()

    # 切换出战阴阳师
    if switch_out:
        switch_out = RuleClick((600,570,100,25), (600,570,100,25))
        sleep(random.random()+1)
        cur_task.click(switch_out)

    input("first test, press enter to continue...")

    cur_task.ui_click_until_disappear(MultiAccountAssets.I_AUTO)
    
    while 1:
        cur_task.screenshot()
        if cur_task.appear(GeneralInviteAssets.I_GI_CANCEL):
            break
        sleep(1)
        
    cur_task.ui_click_until_disappear(GeneralInviteAssets.I_GI_CANCEL, 1.5)
    cur_task.exit_room()
    
    if cur_task.ui_get_current_page() != page_main:
        cur_task.ui_goto(page_main)
    

daliy_json = "D:\\softwa\\yys\\OnmyojiAutoScript-easy-install\\tasks\\MultiAccount\\multi_daily_temp.json"
target_json = "D:\\softwa\\yys\\OnmyojiAutoScript-easy-install\\config\\multi_account.json"
os.system(f'copy {daliy_json} {target_json}')
account_data = json.load(open("D:\\softwa\\yys\\OnmyojiAutoScript-easy-install\\tasks\\MultiAccount\\account_info_temp.json", 'rb'))

# try start app
config = Config('multi_account')
device = Device(config)
restart_task = restart_task(config, device)
# restart_task.app_start()

# loop in multi account
login = login_task(config, device)
multi_account = MultiAccountAssets()

orochi = orochi_task(config, device)

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

        add_team_source(orochi)        
        
        if orochi.ui_get_current_page() != page_main:
            orochi.ui_goto(page_main)

        if "队长" in key:
            if "月哥" in key:
                connect_team_30(orochi, switch_out=True)
            else:
                connect_team_30(orochi)

    except Exception as e:
        logger.error(f"Account {key} failed")
        continue_flag = True
        input("Need human intervention...")

    # 下一个账号

    sleep(10+random.random()*5)
        
restart_task.app_stop()