"""
任务6: 每天18点以后启动，悬赏封印截图 (重构版 - 使用基类)
账号配置: account_info_wantsquest.json
"""
import sys
import os

cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)

from tasks.DemonEncounter.script_task import ScriptTask as demon_task
from tasks.MultiAccount.base_task import BaseMultiAccountTask, ensure_page_main
from tasks.MultiAccount.task_list import screenshot_wantedquests
from module.logger import logger


class Task6WantsquestEvening(BaseMultiAccountTask):
    """任务6: 晚上悬赏封印截图"""
    
    def __init__(self):
        account_file = "D:\\software\\yys\\resource\\task_account\\account_info_wantsquest.json"
        super().__init__(account_file, "任务6-晚上悬赏封印截图")
        self.cur_task = None
    
    def init_device(self):
        """初始化设备并创建任务实例"""
        super().init_device()
        self.cur_task = demon_task(self.config, self.device)
    
    def execute_task_for_account(self, account_info):
        """为单个账号执行悬赏封印截图"""
        账号 = account_info.get("账号")
        角色 = account_info.get("角色")
        系统 = account_info.get("系统")
        
        try:
            screenshot_wantedquests(self.cur_task, 账号, 角色, 系统)
            logger.info(f"账号 {账号}-{角色}-{系统} 晚上悬赏封印截图完成")
        except Exception as e:
            logger.error(f"账号 {账号}-{角色} 晚上悬赏封印截图失败: {e}")
        
        # 返回主页
        ensure_page_main(self.cur_task)


def main():
    """主函数"""
    task = Task6WantsquestEvening()
    task.run()


if __name__ == "__main__":
    main()
