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


# def add_team_source(cur_task):
#     # 主页主队，同心队，同心队中心，一键寄存，确认，回到主页
    
#     if cur_task.ui_get_current_page() != page_main:
#         cur_task.ui_goto(page_main)
        
#     cur_task.ui_click(cur_task.I_HOME_TEAM, cur_task.I_CHECK_TEAM, 1.5)
#     cur_task.ui_click(cur_task.I_CHECK_TEAM, MultiAccountAssets.I_TEAM_HOME, 1.5)
#     cur_task.ui_click(MultiAccountAssets.I_TEAM_HOME, MultiAccountAssets.I_ONE_STEP_SOURCE, 1.5)
#     cur_task.ui_click(MultiAccountAssets.I_ONE_STEP_SOURCE, GeneralInviteAssets.I_GI_SURE, 1.5)
#     cur_task.ui_click_until_disappear(GeneralInviteAssets.I_GI_SURE, 1.5)
    
#     if cur_task.ui_get_current_page() != page_main:
#         cur_task.ui_goto(page_main)
    
# def connect_team_30(cur_task: orochi_task, switch_out=False):
#     # 主页主队，同心队, 集结，御魂副本集结，副本， 创建队伍，开加成，开自动，run，取消，退出组队，回到主页
#     if cur_task.ui_get_current_page() != page_main:
#         cur_task.ui_goto(page_main)
#     [cur_task.I_HOME_TEAM, cur_task.I_CHECK_TEAM, MultiAccountAssets.I_UNION,
#      MultiAccountAssets.I_YUHUN_UNION, MultiAccountAssets.I_MISSION, MultiAccountAssets.I_AUTO,
#      GeneralInviteAssets.I_GI_CANCEL, ]
    
#     cur_task.ui_click(cur_task.I_HOME_TEAM, cur_task.I_CHECK_TEAM, 1.5)
#     cur_task.ui_click(cur_task.I_CHECK_TEAM, MultiAccountAssets.I_UNION, 1.5)
#     cur_task.ui_click(MultiAccountAssets.I_UNION, MultiAccountAssets.I_YUHUN_UNION, 1.5)
#     cur_task.ui_click_until_disappear(MultiAccountAssets.I_YUHUN_UNION, 1.5)
#     cur_task.ui_click_until_disappear(MultiAccountAssets.I_MISSION, 1.5)
    
#     cur_task.create_room()
#     cur_task.ensure_private()
#     cur_task.create_ensure()

#     # 切换出战阴阳师
#     if switch_out:
#         switch_out = RuleClick((600,570,100,25), (600,570,100,25))
#         sleep(random.random()+1)
#         cur_task.click(switch_out)

#     input("first test, press enter to continue...")

#     cur_task.ui_click_until_disappear(MultiAccountAssets.I_AUTO)
    
#     while 1:
#         cur_task.screenshot()
#         if cur_task.appear(GeneralInviteAssets.I_GI_CANCEL):
#             break
#         sleep(1)
        
#     cur_task.ui_click_until_disappear(GeneralInviteAssets.I_GI_CANCEL, 1.5)
#     cur_task.exit_room()
    
#     if cur_task.ui_get_current_page() != page_main:
#         cur_task.ui_goto(page_main)
    
