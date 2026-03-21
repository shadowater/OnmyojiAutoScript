"""
多账号任务调度器
一直运行，按照预设时间自动执行各个任务
"""
import os
import sys
import time
import schedule
from datetime import datetime

cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)

from module.logger import logger

# 导入各个任务的主函数
from tasks.task_1_assist import main as task_1_main
from tasks.task_2_leader_30 import main as task_2_main
from tasks.task_3_member_team import main as task_3_main
from tasks.task_4_consortia import main as task_4_main
from tasks.task_5_wantsquest_morning import main as task_5_main
from tasks.task_6_wantsquest_evening import main as task_6_main


def safe_run_task(task_name, task_func):
    """安全执行任务，捕获异常避免调度器崩溃"""
    try:
        logger.info(f"========== 开始执行 {task_name} ==========")
        start_time = datetime.now()
        task_func()
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f"========== {task_name} 执行完成，耗时 {duration:.0f} 秒 ==========")
    except Exception as e:
        logger.error(f"========== {task_name} 执行失败: {e} ==========")


def run_task_1():
    """执行任务1: 刷协战"""
    safe_run_task("任务1-刷协战", task_1_main)


def run_task_2():
    """执行任务2: 队长刷30"""
    safe_run_task("任务2-队长刷30", task_2_main)


def run_task_3():
    """执行任务3: 补充同心队素材"""
    safe_run_task("任务3-补充同心队素材", task_3_main)


def run_task_4():
    """执行任务4: 捐勾玉+逢魔"""
    safe_run_task("任务4-捐勾玉+逢魔", task_4_main)


def run_task_5():
    """执行任务5: 早晨刷勾协"""
    safe_run_task("任务5-早晨刷勾协", task_5_main)


def run_task_6():
    """执行任务6: 晚上刷勾协"""
    safe_run_task("任务6-晚上刷勾协", task_6_main)


def setup_schedule():
    """设置任务调度时间表"""
    # 任务1: 每天0点10分启动，刷协战
    schedule.every().day.at("00:10").do(run_task_1)
    
    # 任务2: 每天0点30分启动，队长刷30
    schedule.every().day.at("00:30").do(run_task_2)
    
    # 任务5: 每天5点启动，早晨刷勾协
    schedule.every().day.at("05:00").do(run_task_5)
    
    # 任务3: 每天10点启动，补充同心队素材
    schedule.every().day.at("10:00").do(run_task_3)
    
    # 任务4: 每天17点启动，捐勾玉+逢魔
    schedule.every().day.at("17:00").do(run_task_4)
    
    # 任务6: 每天18点启动，晚上刷勾协
    schedule.every().day.at("18:00").do(run_task_6)
    
    logger.info("任务调度器已设置完成")
    logger.info("任务1 (刷协战): 每天 00:10")
    logger.info("任务2 (队长刷30): 每天 00:30")
    logger.info("任务5 (早晨刷勾协): 每天 05:00")
    logger.info("任务3 (补充同心队素材): 每天 10:00")
    logger.info("任务4 (捐勾玉+逢魔): 每天 17:00")
    logger.info("任务6 (晚上刷勾协): 每天 18:00")


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("多账号任务调度器启动")
    logger.info("=" * 60)
    
    # 设置调度
    setup_schedule()
    
    # 显示下一次任务执行时间
    logger.info(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    next_run = schedule.next_run()
    if next_run:
        logger.info(f"下一次任务执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 主循环
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)  # 每30秒检查一次
    except KeyboardInterrupt:
        logger.info("收到停止信号，调度器正在关闭...")
    except Exception as e:
        logger.error(f"调度器发生错误: {e}")
    finally:
        logger.info("调度器已停止")


if __name__ == "__main__":
    main()
