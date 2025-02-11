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

cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]

daliy_json = oas_path + "\\tasks\\MultiAccount\\multi_daily_temp.json"
target_json = oas_path + "\\config\\multi_account.json"
os.system(f'copy {daliy_json} {target_json}')
account_data = json.load(open(oas_path + "\\tasks\\MultiAccount\\account_info_temp.json", 'rb'))

config = Config('multi_account')
device = Device(config)

toAccount=AccountInfo(account="qhq79062449ran@163.com", apple_or_android=True,
                        character="明月倾城倾城陌", svr="孤高之心")
sa=SwitchAccount(config,device,toAccount)
sa.switchAccount()


# # try start app
# config = Config('multi_account')
# device = Device(config)
# restart_task = restart_task(config, device)
# restart_task.app_start()

# # loop in multi account
# login = login_task(config, device)
# multi_account = MultiAccountAssets()

# demon = demon_task(config, device)
# trifles = trifles_task(config, device)
# areaboss = areaboss_task(config, device)
# talisman = talisman_task(config, device)

# task_list = [trifles, areaboss, talisman]
# run_task_indices = []
# continue_flag = True

# task_list = [task_list[ii] for ii in range(len(task_list)) if ii in run_task_indices]
# for key, value in account_data.items():
#     # continue
    
#     try:
#         ## switch account
#         and_or_ios = True if "and" in key else False
#         character = key.split("#")[-1]
        
#         toAccount=AccountInfo(account=value, apple_or_android=and_or_ios,
#                                 character=character, svr="孤高之心")
#         sa=SwitchAccount(config,device,toAccount)
#         sa.switchAccount()

#         lantern_task()
                
#         ## run task 
#         for cur_task in task_list:
#             try:
#                 cur_task.run()
#             except Exception as e:
#                 logger.error(f"Task {cur_task} finished")
                
#         if demon.ui_get_current_page() != page_main:
#             demon.ui_goto(page_main)

#         # 截个图，看看勾协和蓝屏黑蛋
#         # value = value.replace("*", "x")
#         # if not os.path.exists(f"D:\\Software\\yys\\MultiAccount\\wantedquests\\{key}_{value}.png"):
#         #     screenshot_wantedquests()
#         # if not os.path.exists(f"D:\\Software\\yys\\MultiAccount\\mysteryshop\\{key}_{value}.png"):
#         #     screenshot_mysteryshop()
            
#     except Exception as e:
#         logger.error(f"Account {key} failed")
#         continue_flag = True
#         input("Need human intervention...")

#     # 下一个账号
#     if continue_flag:
#         sleep(10+random.random()*5)
#     else:
#         input("Press Enter to continue...")
        
# restart_task.app_stop()