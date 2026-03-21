import json
import os
import time
from numpy import random
from time import sleep

import sys
import numpy as np
from sympy import im
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
from module.base.timer import Timer

# try start app
config = Config('daily_ios')
device = Device(config)
activity = activity_task(config, device)
restart_task = restart_task(config, device)


while 1:
    
    activity.screenshot()
    
    # if  activity.appear(MultiAccountAssets.I_SUNMMING):
    activity.appear_then_click(MultiAccountAssets.I_SUNMMING, interval = 0.9)
    
    # if  activity.appear(MultiAccountAssets.I_CHAR):
    activity.appear_then_click(MultiAccountAssets.I_CHAR, interval = 1.9)
        
    # if activity.appear(activity.I_PREPARE_HIGHLIGHT):
    if activity.appear_then_click(activity.I_PREPARE_HIGHLIGHT, interval = 2.5):
        activity.device.stuck_timer_long = Timer(240, count=240).start()
        activity.device.stuck_record_add('BATTLE_STATUS_S')    
        if activity.wait_until_appear(activity.I_WIN, wait_time=240):
            activity.appear_then_click(activity.I_WIN, interval = 2.9)
        else:
            restart_task.app_stop()
            break
        

    time.sleep(np.random.random()+1)