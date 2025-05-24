import json
import os
import sys
from numpy import random
from time import sleep
import pandas as pd
cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)
from tasks.Restart.script_task import ScriptTask as restart_task
from tasks.KekkaiActivation.script_task import ScriptTask as kekkaiactivation_task
from tasks.KekkaiUtilize.script_task import ScriptTask as kekkaiutilize_task
from tasks.Component.SwitchAccount.switch_account import SwitchAccount
from tasks.Component.SwitchAccount.switch_account_config import AccountInfo
from tasks.GameUi.page import page_main
from tasks.MultiAccount.task_list import screenshot_wantedquests, screenshot_mysteryshop
from module.config.config import Config
from module.device.device import Device
from module.logger import logger



daliy_json = oas_path + "\\tasks\\MultiAccount\\multi_daily_temp.json"
target_json = oas_path + "\\config\\multi_account.json"
os.system(f'copy {daliy_json} {target_json}')
# sleep(3600*7)


# try start app
config = Config('multi_account')
device = Device(config)
restart_task = restart_task(config, device)
restart_task.app_start()

# loop in multi account
kekkaiactivation = kekkaiactivation_task(config, device)
kekkaiutilize = kekkaiutilize_task(config, device)
# task_list = []
task_list = [kekkaiutilize]

account_data = pd.read_csv(oas_path + "\\tasks\\MultiAccount\\account_info.csv")
account_data.replace("and", True, inplace=True)
account_data.replace("ios", False, inplace=True)
account_data.fillna("", inplace=True)

for ii in account_data.iterrows():
    ii = ii[1]
    # screenshot_wantedquests(kekkaiactivation, ii["account"], ii["character"],oas_path)
    print(ii)
    try:
        toAccount=AccountInfo(account=ii["account"], apple_or_android=ii["system"],
                                character=ii["character"], svr="网易一" + ii["server"])
        sa=SwitchAccount(config,device,toAccount)
        sa.switchAccount()
            
        for cur_task in task_list:
            try:
                cur_task.run()
            except Exception as e:
                logger.error(f"Task {cur_task} finished")
                
        kekkaiactivation.ui_goto(page_main)
        screenshot_wantedquests(kekkaiactivation, ii["account"].replace("*","x"), ii["character"],oas_path)
        # screenshot_mysteryshop(kekkaiactivation, key, value, oas_path)
        # input("Need human intervention...")
        sleep(5+random.random()*5)
    except:
        # restart_task.app_stop()
        logger.error(f"Account {ii['name']} failed")
        break
    
restart_task.app_stop()