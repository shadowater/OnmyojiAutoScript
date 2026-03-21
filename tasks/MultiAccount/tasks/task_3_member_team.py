"""
任务3: 每天10点以后启动，补充同心队素材 (重构版 - 使用基类)
账号配置: account_info_member.json
"""
import sys
import os

cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)

from tasks.DemonEncounter.script_task import ScriptTask as demon_task
from tasks.MultiAccount.base_task import BaseMultiAccountTask, ensure_page_main
from tasks.MultiAccount.common_functions import add_team_source
from module.logger import logger


class Task3MemberTeam(BaseMultiAccountTask):
    """任务3: 补充同心队素材"""
    
    def __init__(self):
        account_file = "D:\\software\\yys\\resource\\task_account\\account_info_member.json"
        super().__init__(account_file, "任务3-补充同心队素材")
        self.demon = None
    
    def init_device(self):
        """初始化设备并创建任务实例"""
        super().init_device()
        self.demon = demon_task(self.config, self.device)
    
    def execute_task_for_account(self, account_info):
        """为单个账号执行补充同心队素材任务"""
        账号 = account_info.get("账号")
        角色 = account_info.get("角色")
        
        try:
            add_team_source(self.demon)
            logger.info(f"账号 {账号}-{角色} 补充同心队素材完成")
        except Exception as e:
            logger.error(f"账号 {账号}-{角色} 补充同心队素材失败: {e}")
        
        # 返回主页
        ensure_page_main(self.demon)


def main():
    """主函数"""
    task = Task3MemberTeam()
    task.run()


if __name__ == "__main__":
    main()
