"""
任务4: 每天17点以后启动，捐勾玉，顺便逢魔 (重构版 - 使用基类)
账号配置: account_info_consortia.json
"""
import sys
import os

cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)

from tasks.DemonEncounter.script_task import ScriptTask as demon_task
from tasks.MultiAccount.base_task import BaseMultiAccountTask, ensure_page_main
from tasks.MultiAccount.common_functions import donate_guild, lantern_task
from module.logger import logger


class Task4Consortia(BaseMultiAccountTask):
    """任务4: 捐勾玉+逢魔"""
    
    def __init__(self):
        account_file = "D:\\software\\yys\\resource\\task_account\\account_info_consortia.json"
        super().__init__(account_file, "任务4-捐勾玉+逢魔")
        self.demon = None
    
    def init_device(self):
        """初始化设备并创建任务实例"""
        super().init_device()
        self.demon = demon_task(self.config, self.device)
    
    def execute_task_for_account(self, account_info):
        """为单个账号执行捐赠和逢魔任务"""
        账号 = account_info.get("账号")
        角色 = account_info.get("角色")
        
        # 执行捐赠任务
        try:
            donate_guild(self.demon)
            logger.info(f"账号 {账号}-{角色} 捐赠完成")
        except Exception as e:
            logger.error(f"账号 {账号}-{角色} 捐赠失败: {e}")
        
        # 执行逢魔任务
        try:
            lantern_task(self.demon)
            logger.info(f"账号 {账号}-{角色} 逢魔完成")
        except Exception as e:
            logger.error(f"账号 {账号}-{角色} 逢魔失败: {e}")
        
        # 返回主页
        ensure_page_main(self.demon)


def main():
    """主函数"""
    task = Task4Consortia()
    task.run()


if __name__ == "__main__":
    main()
