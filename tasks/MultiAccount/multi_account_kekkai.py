import json
import os
import sys
from numpy import random
from time import sleep
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
account_data = json.load(open(oas_path + "\\tasks\\MultiAccount\\account_info_temp.json", 'rb'))

# try start app
config = Config('multi_account')
device = Device(config)
restart_task = restart_task(config, device)
restart_task.app_start()

# loop in multi account
kekkaiactivation = kekkaiactivation_task(config, device)
kekkaiutilize = kekkaiutilize_task(config, device)
task_list = [kekkaiactivation, kekkaiutilize]

for key, value in account_data.items():
    # continue
    
    and_or_ios = True if "and" in key else False
    character = key.split("#")[-1]
    
    try:    

        toAccount=AccountInfo(account=value, apple_or_android=and_or_ios,
                                character=character, svr="孤高之心")
        sa=SwitchAccount(config,device,toAccount)
        sa.switchAccount()
            
        for cur_task in task_list:
            try:
                cur_task.run()
            except Exception as e:
                logger.error(f"Task {cur_task} finished")
                
        kekkaiactivation.ui_goto(page_main)

        value = value.replace("*", "x")
        screenshot_wantedquests(kekkaiactivation, key, value, oas_path)
        # screenshot_mysteryshop(kekkaiactivation, key, value, oas_path)
                
        sleep(5+random.random()*5)
    except:
        input("Need human intervention...")
    
restart_task.app_stop()