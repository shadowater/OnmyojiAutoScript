import os
import sys
from PIL import Image
from time import sleep
from numpy import random
from datetime import datetime
cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)
from module.logger import logger
from module.base.timer import Timer
from tasks.DemonEncounter.script_task import ScriptTask
from tasks.GameUi.page import page_demon_encounter, page_main
from tasks.WantedQuests.assets import WantedQuestsAssets
from tasks.WantedQuests.assets import WantedQuestsAssets
from tasks.GlobalGame.assets import GlobalGameAssets
from tasks.MysteryShop.assets import MysteryShopAssets

class lantern_task(ScriptTask):

    def run(self):
        if not self.check_time():
            logger.warning('Time is not right')
            return 0
        
        self.ui_get_current_page()
        self.ui_goto(page_demon_encounter)

        ocr_timer = Timer(0.8)
        ocr_timer.start()
        while 1:
            self.screenshot()
            if not ocr_timer.reached():
                continue
            else:
                ocr_timer.reset()
            cu, re, total = self.O_DE_COUNTER.ocr(self.device.image)
            if cu + re != total:
                logger.warning('Lantern count error')
                continue
            if cu == 0 and re == 4:
                break

            if self.appear_then_click(self.I_DE_FIND, interval=2.5):
                continue
        logger.info('Lantern count success')
        # 然后领取红色达摩
        self.screenshot()
        if not self.appear(self.I_DE_AWARD):
            self.ui_get_reward(self.I_DE_RED_DHARMA)
        self.wait_until_appear(self.I_DE_AWARD)
        self.ui_goto(page_main)

        if not self.check_time():
            logger.warning('Time is not right')
            return 0
        
        self.ui_get_current_page()
        self.ui_goto(page_demon_encounter)
        

def screenshot_wantedquests(cur_task, key, value, oas_path):

    while 1:
        cur_task.screenshot()
        if cur_task.appear(WantedQuestsAssets.I_TRACE_ENABLE) or cur_task.appear(WantedQuestsAssets.I_TRACE_DISABLE):
            break
        if cur_task.appear_then_click(WantedQuestsAssets.I_WQ_SEAL, interval=3):
            continue
        if cur_task.appear_then_click(WantedQuestsAssets.I_WQ_DONE, interval=3):
            continue
        
    cur_task.screenshot() 
    img = Image.fromarray(cur_task.device.image, mode='RGB')
    img.save(oas_path.split("OnmyojiAutoScript")[0] + f"{key}_{value}_wantedquests.png")
    cur_task.ui_click_until_disappear(GlobalGameAssets.I_UI_BACK_RED)
    sleep(random.random()+0.5)

def screenshot_mysteryshop(cur_task, key, value, oas_path):
    day_of_week = datetime.now().weekday()
    if day_of_week != 2 and day_of_week != 5:
        logger.warning('Today is not MysteryShop day')
    else:
        cur_task.ui_click(cur_task.I_MAIN_GOTO_MALL ,cur_task.I_BACK_Y)
        sleep(random.random()+0.5)
        cur_task.ui_click(cur_task.I_BACK_Y ,cur_task.I_BACK_BLUE)
        sleep(random.random()+0.5)
        cur_task.ui_click(cur_task.I_BACK_Y , MysteryShopAssets.I_ME_ENTER)
        sleep(random.random()+0.5)
        cur_task.ui_click(MysteryShopAssets.I_ME_ENTER, MysteryShopAssets.I_MS_SHARE)
        logger.info('Enter MysteryShop')
            
        # refresh = RuleClick((1199,533,55,54), (1199,533,55,54))
        # have_blue = cur_task.appear(MysteryShopAssets.I_MS_BLUE)
        # have_black = cur_task.appear(MysteryShopAssets.I_MS_BLACK)
        # if not have_blue and not have_black:
        #     cur_task.click(refresh)
        #     cur_task.click(kekkai.I_UI_CONFIRM_SAMLL)
        
        cur_task.screenshot() 
        img = Image.fromarray(cur_task.device.image, mode='RGB')
        img.save(oas_path.split("OnmyojiAutoScript")[0] + f"{key}_{value}_mysteryshop.png")
            
        sleep(random.random()+0.5)
        cur_task.ui_click(cur_task.I_BACK_Y ,cur_task.I_BACK_BLUE)
        sleep(random.random()+0.5)
        cur_task.ui_click(cur_task.I_BACK_BLUE ,cur_task.I_CHECK_MAIN)


