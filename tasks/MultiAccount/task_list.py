import sys
sys.path.append("D:\\software\\yys\\OnmyojiAutoScript")
from module.logger import logger
from module.base.timer import Timer
from tasks.DemonEncounter.script_task import ScriptTask
from tasks.GameUi.page import page_demon_encounter, page_main


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
        

class screenshot_wantedquests():
    pass

class screenshot_mysteryshop():
    pass

# def screenshot_wantedquests():

#     while 1:
#         demon.screenshot()
#         if demon.appear(WantedQuestsAssets.I_TRACE_ENABLE) or demon.appear(WantedQuestsAssets.I_TRACE_DISABLE):
#             break
#         if demon.appear_then_click(WantedQuestsAssets.I_WQ_SEAL, interval=1):
#             continue
        
#     demon.screenshot() 
#     img = Image.fromarray(demon.device.image, mode='RGB')
#     img.save(f"D:\\Software\\yys\\MultiAccount\\wantedquests\\{key}_{value}.png")
#     demon.ui_click_until_disappear(GlobalGameAssets.I_UI_BACK_RED)
#     sleep(random.random()+0.5)

# def screenshot_mysteryshop():
#     day_of_week = datetime.now().weekday()
#     if day_of_week != 2 and day_of_week != 5:
#         logger.warning('Today is not MysteryShop day')
#     else:
#         demon.ui_click(demon.I_MAIN_GOTO_MALL ,demon.I_BACK_Y)
#         sleep(random.random()+0.5)
#         demon.ui_click(demon.I_BACK_Y ,demon.I_BACK_BLUE)
#         sleep(random.random()+0.5)
#         demon.ui_click(demon.I_BACK_Y , MysteryShopAssets.I_ME_ENTER)
#         sleep(random.random()+0.5)
#         demon.ui_click(MysteryShopAssets.I_ME_ENTER, MysteryShopAssets.I_MS_SHARE)
#         logger.info('Enter MysteryShop')
            
#         # refresh = RuleClick((1199,533,55,54), (1199,533,55,54))
#         # have_blue = demon.appear(MysteryShopAssets.I_MS_BLUE)
#         # have_black = demon.appear(MysteryShopAssets.I_MS_BLACK)
#         # if not have_blue and not have_black:
#         #     demon.click(refresh)
#         #     demon.click(kekkai.I_UI_CONFIRM_SAMLL)
        
#         demon.screenshot() 
#         img = Image.fromarray(demon.device.image, mode='RGB')
#         img.save(f"D:\\Software\\yys\\MultiAccount\\mysteryshop\\{key}_{value}.png")
            
#         sleep(random.random()+0.5)
#         demon.ui_click(demon.I_BACK_Y ,demon.I_BACK_BLUE)
#         sleep(random.random()+0.5)
#         demon.ui_click(demon.I_BACK_BLUE ,demon.I_CHECK_MAIN)