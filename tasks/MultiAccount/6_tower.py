import json
import os
from numpy import random
from time import sleep

import sys
cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)
from tasks.Restart.login import LoginHandler as login_task
from tasks.Restart.script_task import ScriptTask as restart_task
from tasks.Component.SwitchAccount.switch_account import SwitchAccount
from tasks.Component.SwitchAccount.switch_account_config import AccountInfo
from tasks.ActivityShikigami.script_task import ScriptTask as activity_task
from tasks.SoulsTidy.script_task import ScriptTask as souls_tidy_task
from tasks.MultiAccount.assets import MultiAccountAssets
from module.config.config import Config
from module.device.device import Device
from datetime import datetime


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
login = login_task(config, device)
activity = activity_task(config, device)
souls_tidy = souls_tidy_task(config, device)
continue_flag = True
# activity.run()

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

        # try:
        #     souls_tidy.run()
        # except Exception as e:
        #     pass

        try:
            activity.run()
            
        except Exception as e:
            pass
        
        activity.current_count = 0
        activity.start_time = datetime.now()
    except Exception as e:
        restart_task.app_stop()
        input(f"Error2: {e}")

        
    # input("Continue? (y/n)")
    sleep(5+random.random()*5)
               
               
restart_task.app_stop()