"""
任务1: 每天0点后启动，刷协战 (重构版 - 使用基类)
账号配置: account_info_assist_task.json
"""
import sys
import os

cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)

from tasks.EvoZone.script_task import ScriptTask as evozone_task
from tasks.MultiAccount.base_task import BaseMultiAccountTask, ensure_page_main
from module.logger import logger


class Task1AssistBoss(BaseMultiAccountTask):
    """任务1: 刷协战"""
    
    def __init__(self):
        account_file = "D:\\software\\yys\\resource\\task_account\\account_info_assist_task.json"
        super().__init__(account_file, "任务1-刷协战")
        self.areaboss = None
    
    def init_device(self):
        """初始化设备并创建协战任务实例"""
        super().init_device()
        self.areaboss = evozone_task(self.config, self.device)
    
    def execute_task_for_account(self, account_info):
        """为单个账号执行协战任务"""
        账号 = account_info.get("账号")
        角色 = account_info.get("角色")
        
        try:
            self.areaboss.run()
            logger.info(f"账号 {账号}-{角色} 协战任务完成")
        except Exception as e:
            logger.error(f"账号 {账号}-{角色} 协战任务失败: {e}")
        
        # 返回主页
        ensure_page_main(self.areaboss)


def main():
    """主函数"""
    task = Task1AssistBoss()
    task.run()


if __name__ == "__main__":
    main()
