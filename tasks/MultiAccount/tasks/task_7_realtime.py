"""
任务7: 实时检测并点击指定元素（区域内随机点模式，且禁用报错）
"""
import sys
import os
import random
from time import sleep

# 获取项目根目录并添加到 sys.path
cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)

from tasks.EvoZone.script_task import ScriptTask as runner_task
from tasks.MultiAccount.assets import MultiAccountAssets
from module.config.config import Config
from module.device.device import Device
from module.logger import logger

def run_realtime_detection():
    # 1. 初始化设备和任务实例
    logger.info("正在初始化设备...")
    config = Config('multi_account')
    device = Device(config)
    
    # 【关键】：禁用点击频率检查，彻底防止 Too many click 报错
    if hasattr(device, 'click_record_check'):
        device.click_record_check = lambda: None
        logger.info("已成功禁用 click_record_check")
    
    runner = runner_task(config, device)
    
    # 2. 定义需要检测的元素列表
    target_images = [
        MultiAccountAssets.I_POINT_IN_MAIN,
        MultiAccountAssets.I_POINT_IN_TASK,
        MultiAccountAssets.I_QUESTION,
        MultiAccountAssets.I_LOOK,
        MultiAccountAssets.I_BATTLE,
        MultiAccountAssets.I_FASTER,
        MultiAccountAssets.I_JUMP,
        MultiAccountAssets.I_PREPARE
    ]
    
    logger.info("开始实时检测循环（区域内随机点模式）...")
    
    try:
        while True:
            # 截图
            runner.screenshot()
            
            found = False
            for img in target_images:
                if runner.appear(img):
                    # 获取区域 (x, y, w, h)
                    x, y, w, h = img.roi_front
                    # 在区域内产生随机点
                    rand_x = random.randint(x, x + w)
                    rand_y = random.randint(y, y + h)
                    
                    logger.info(f"检测到元素 {img.file}，点击区域内随机点: ({rand_x}, {rand_y})")
                    device.click(rand_x, rand_y)
                    found = True
                    break 
            
            if not found:
                # 400, 400, 100, 100 区域内的随机点
                rand_x = random.randint(400, 500)
                rand_y = random.randint(400, 500)
                device.click(rand_x, rand_y)
            
            # 休息一秒
            sleep(1)
            
    except KeyboardInterrupt:
        logger.info("用户手动停止脚本")
    except Exception as e:
        logger.error(f"运行发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_realtime_detection()
