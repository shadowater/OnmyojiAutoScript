"""
通用任务函数库
提取各个任务脚本中的公共函数
"""
import time
from numpy import random
from time import sleep

from tasks.Component.GeneralInvite.assets import GeneralInviteAssets
from tasks.MultiAccount.assets import MultiAccountAssets
from tasks.GameUi.page import page_main, page_demon_encounter, page_guild
from module.logger import logger
from module.base.timer import Timer


def add_team_source(cur_task):
    """
    补充同心队素材
    主页主队，同心队，同心队中心，一键寄存，确认，回到主页
    """
    if cur_task.ui_get_current_page() != page_main:
        cur_task.ui_goto(page_main)
        
    cur_task.ui_click(cur_task.I_HOME_TEAM, cur_task.I_CHECK_TEAM, 1.5)
    cur_task.ui_click(cur_task.I_CHECK_TEAM, MultiAccountAssets.I_TEAM_HOME, 1.5)
    cur_task.ui_click(MultiAccountAssets.I_TEAM_HOME, MultiAccountAssets.I_ONE_STEP_SOURCE, 1.5)
    cur_task.ui_click(MultiAccountAssets.I_ONE_STEP_SOURCE, GeneralInviteAssets.I_GI_SURE, 1.5)
    cur_task.ui_click_until_disappear(GeneralInviteAssets.I_GI_SURE, 1.5)
    
    if cur_task.ui_get_current_page() != page_main:
        cur_task.ui_goto(page_main)


def donate_guild(cur_task):
    """
    捐赠勾玉到公会
    进入寮页面，寮信息，寮捐赠，增加勾玉数量，确定捐赠
    """
    cur_task.ui_goto(page_guild)
    cur_task.ui_click(MultiAccountAssets.I_GUILD_INFO, MultiAccountAssets.I_DONATE, interval=2)
    cur_task.click(MultiAccountAssets.I_DONATE, interval=1)
    time.sleep(1 + random.random())
    if cur_task.wait_until_appear(MultiAccountAssets.I_DONATE_ADD, wait_time=0.5):
        cur_task.ui_click(MultiAccountAssets.I_DONATE_ADD, MultiAccountAssets.I_DONATE_SURE, interval=0.5)
        cur_task.click(MultiAccountAssets.I_DONATE_SURE)
    time.sleep(1)
    cur_task.click(cur_task.I_UI_BACK_YELLOW)
    cur_task.click(cur_task.I_UI_BACK_YELLOW)
    cur_task.ui_goto(page_main)


def lantern_task(cur_task):
    """
    逢魔任务
    执行逢魔之时任务
    """
    if not cur_task.check_time():
        logger.warning('Time is not right')
        return 0
    
    cur_task.ui_get_current_page()
    cur_task.ui_goto(page_demon_encounter)

    ocr_timer = Timer(0.8)
    ocr_timer.start()
    while 1:
        cur_task.screenshot()
        if not ocr_timer.reached():
            continue
        else:
            ocr_timer.reset()
        cu, re, total = cur_task.O_DE_COUNTER.ocr(cur_task.device.image)
        if cu + re != total:
            logger.warning('Lantern count error')
            continue
        if cu == 0 and re == 4:
            break

        if cur_task.appear_then_click(cur_task.I_DE_FIND, interval=2.5):
            continue
    logger.info('Lantern count success')
    # 然后领取红色达摩
    cur_task.screenshot()
    if not cur_task.appear(cur_task.I_DE_AWARD):
        cur_task.ui_get_reward(cur_task.I_DE_RED_DHARMA)
    cur_task.wait_until_appear(cur_task.I_DE_AWARD)
    cur_task.ui_goto(page_main)


def connect_team_30(cur_task):
    """
    创建30层队伍并执行任务
    主页主队，同心队, 集结，御魂副本集结，副本， 创建队伍，开加成，开自动，run，取消，退出组队，回到主页
    """
    if cur_task.ui_get_current_page() != page_main:
        cur_task.ui_goto(page_main)
    
    cur_task.ui_click(cur_task.I_HOME_TEAM, cur_task.I_CHECK_TEAM, 1.5)
    cur_task.ui_click(cur_task.I_CHECK_TEAM, MultiAccountAssets.I_UNION, 1.5)
    cur_task.ui_click(MultiAccountAssets.I_UNION, MultiAccountAssets.I_YUHUN_UNION, 1.5)
    cur_task.ui_click_until_disappear(MultiAccountAssets.I_YUHUN_UNION, 1.5)
    cur_task.ui_click_until_disappear(MultiAccountAssets.I_MISSION, 1.5)
    
    cur_task.create_room()
    cur_task.ensure_private()
    cur_task.create_ensure()
    
    cur_task.ui_click_until_disappear(MultiAccountAssets.I_AUTO, 3)
    
    # 等待战斗结束
    cur_task.device.stuck_timer_long = Timer(1800, count=1800).start()
    cur_task.device.stuck_record_add('BATTLE_STATUS_S')    
    cur_task.wait_until_appear(GeneralInviteAssets.I_GI_CANCEL, wait_time=1800)
    cur_task.device.stuck_record_clear()
    
    cur_task.ui_click_until_disappear(GeneralInviteAssets.I_GI_CANCEL, 1.5)
    sleep(random.random() + 0.5)
    cur_task.exit_room()
    
    if cur_task.ui_get_current_page() != page_main:
        cur_task.ui_goto(page_main)
