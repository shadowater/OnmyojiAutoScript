"""
简化版多账号任务调度器
不依赖schedule库，使用纯Python实现
一直运行，按照预设时间自动执行各个任务
"""
import os
import sys
import time
import json
import subprocess
from datetime import datetime, timedelta

cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)

from module.logger import logger


# 任务配置: (任务名称, 脚本文件名, 执行时间(小时, 分钟))
TASK_SCHEDULE = [
    ("任务1-刷协战", "tasks/task_1_assist.py", 0, 0),
    ("任务2-队长刷30", "tasks/task_2_leader_30.py", 0, 0),
    ("任务3-补充同心队素材", "tasks/task_3_member_team.py", 0, 0),
    ("任务4-捐勾玉+逢魔", "tasks/task_4_consortia.py", 0, 0),
    ("任务5-早晨刷勾协", "tasks/task_5_wantsquest_morning.py", 5, 0),
    # ("任务6-晚上刷勾协", "tasks/task_6_wantsquest_evening.py", 18, 0),
]


class TaskScheduler:
    def __init__(self):
        self.tasks = TASK_SCHEDULE
        self.executed_today = set()  # 记录今天已执行的任务
        self.current_date = datetime.now().date()
        
    def should_run_task(self, task_name, hour, minute):
        """检查任务是否应该执行"""
        now = datetime.now()
        
        # 如果今天已经执行过，跳过
        if task_name in self.executed_today:
            return False
        
        # 检查是否到了执行时间
        if now.hour == hour and now.minute == minute:
            return True
        
        # 如果当前时间已经超过了计划时间，且今天还没执行，则立即执行
        task_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if now > task_time:
            return True
            
        return False
    
    def sync_morning_task_status(self):
        """将早晨刷勾协的任务状态更新为已完成 (JSON同步)"""
        morning_json = "D:\\software\\yys\\resource\\task_account\\account_info_wantsquest_morning.json"
        if not os.path.exists(morning_json):
            logger.warning(f"找不到早晨任务配置文件: {morning_json}")
            return
            
        try:
            with open(morning_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            current_date = datetime.now().strftime('%Y-%m-%d')
            for account in data:
                account["日期"] = current_date
                account["任务完成状态"] = True
            
            with open(morning_json, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            logger.info("已同步更新早晨刷勾协的JSON状态为已完成")
        except Exception as e:
            logger.error(f"同步更新早晨任务状态失败: {e}")

    def run_task(self, task_name, script_file):
        """执行任务脚本"""
        try:
            logger.info(f"========== 开始执行 {task_name} ==========")
            start_time = datetime.now()
            
            # 获取脚本完整路径
            script_path = os.path.join(os.path.dirname(__file__), script_file)
            
            # 使用subprocess运行脚本
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            if result.returncode == 0:
                logger.info(f"========== {task_name} 执行完成，耗时 {duration:.0f} 秒 ==========")
            else:
                logger.error(f"========== {task_name} 执行失败，返回码: {result.returncode} ==========")
                if result.stderr:
                    logger.error(f"错误信息: {result.stderr[:500]}")
            
            # 标记为已执行
            self.executed_today.add(task_name)
            
            # 特殊逻辑：如果是晚上刷勾协，同步更新早晨任务状态
            if task_name == "任务6-晚上刷勾协":
                morning_task_name = "任务5-早晨刷勾协"
                if morning_task_name not in self.executed_today:
                    logger.info(f"由于执行了 {task_name}，自动将 {morning_task_name} 标记为已完成")
                    self.executed_today.add(morning_task_name)
                # 同步更新JSON文件
                self.sync_morning_task_status()
            
        except Exception as e:
            logger.error(f"========== {task_name} 执行异常: {e} ==========")
    
    def get_next_task_info(self):
        """获取下一个即将执行的任务信息"""
        now = datetime.now()
        next_task = None
        min_delta = None
        
        for task_name, script_file, hour, minute in self.tasks:
            if task_name in self.executed_today:
                continue
            
            task_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if task_time < now:
                task_time += timedelta(days=1)
            
            delta = task_time - now
            if min_delta is None or delta < min_delta:
                min_delta = delta
                next_task = (task_name, task_time)
        
        return next_task
    
    def run(self):
        """主循环"""
        logger.info("=" * 60)
        logger.info("多账号任务调度器启动 (简化版)")
        logger.info("=" * 60)
        logger.info("任务时间表:")
        for task_name, script_file, hour, minute in self.tasks:
            logger.info(f"  {task_name}: 每天 {hour:02d}:{minute:02d}")
        logger.info("=" * 60)
        
        try:
            while True:
                now = datetime.now()
                
                # 检查日期是否变化，如果是新的一天，清空已执行记录
                if now.date() != self.current_date:
                    logger.info(f"新的一天开始: {now.date()}")
                    self.executed_today.clear()
                    self.current_date = now.date()
                
                # 检查是否当日所有任务已完成
                all_done = len(self.executed_today) >= len(self.tasks)
                
                # 检查每个任务是否需要执行
                for task_name, script_file, hour, minute in self.tasks:
                    # 1. 逻辑修改：如果当日所有任务已完成，跳过该任务检查
                    if all_done:
                        continue
                        
                    if self.should_run_task(task_name, hour, minute):
                        self.run_task(task_name, script_file)
                        # 重新检查是否全部完成
                        all_done = len(self.executed_today) >= len(self.tasks)
                
                # 显示下一个任务信息 (每小时显示一次)
                if now.minute == 0:
                    next_task = self.get_next_task_info()
                    if next_task:
                        task_name, task_time = next_task
                        logger.info(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                        logger.info(f"下一个任务: {task_name}, 执行时间: {task_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # 每分钟检查一次
                time.sleep(60)
                
        except KeyboardInterrupt:
            logger.info("收到停止信号，调度器正在关闭...")
        except Exception as e:
            logger.error(f"调度器发生错误: {e}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            logger.info("调度器已停止")


def main():
    scheduler = TaskScheduler()
    scheduler.run()


if __name__ == "__main__":
    main()
