"""
任务2: 每天0点以后启动，队长刷30 (重构版 - 使用基类)
账号配置: account_info_leader.json
"""
import sys
import os

cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)

from tasks.Orochi.script_task import ScriptTask as orochi_task
from tasks.MultiAccount.base_task import BaseMultiAccountTask, ensure_page_main
from tasks.MultiAccount.common_functions import connect_team_30
from module.logger import logger


class Task2Leader30(BaseMultiAccountTask):
    """任务2: 队长刷30"""
    
    def __init__(self):
        account_file = "D:\\software\\yys\\resource\\task_account\\account_info_leader.json"
        super().__init__(account_file, "任务2-队长刷30")
        self.orochi = None
    
    def init_device(self):
        """初始化设备并创建大蛇任务实例"""
        super().init_device()
        self.orochi = orochi_task(self.config, self.device)
    
    def execute_task_for_account(self, account_info):
        """为单个账号执行队长刷30任务"""
        账号 = account_info.get("账号")
        角色 = account_info.get("角色")
        
        try:
            connect_team_30(self.orochi)
            logger.info(f"账号 {账号}-{角色} 队长刷30任务完成")
        except Exception as e:
            logger.error(f"账号 {账号}-{角色} 队长刷30任务失败: {e}")
            raise  # 这个任务失败应该中断,因为是队长任务


def main():
    """主函数"""
    task = Task2Leader30()
    task.run()


if __name__ == "__main__":
    main()
