"""
多账号任务基类
提取公共逻辑,减少代码冗余
"""
import json
import os
import sys
from numpy import random
from time import sleep
from datetime import datetime

cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)

from tasks.Restart.script_task import ScriptTask as restart_task
from tasks.Component.SwitchAccount.switch_account import SwitchAccount
from tasks.Component.SwitchAccount.switch_account_config import AccountInfo
from tasks.GameUi.page import page_main
from module.config.config import Config
from module.device.device import Device
from module.logger import logger


class BaseMultiAccountTask:
    """多账号任务基类"""
    
    def __init__(self, account_config_file, task_name="未命名任务"):
        """
        初始化多账号任务
        
        Args:
            account_config_file: 账号配置文件路径
            task_name: 任务名称,用于日志输出
        """
        self.task_name = task_name
        self.account_config_file = account_config_file
        self.oas_path = oas_path
        
        # 配置文件路径
        self.daliy_json = oas_path + "\\tasks\\MultiAccount\\multi_daily_temp.json"
        self.target_json = oas_path + "\\config\\multi_account.json"
        
        # 初始化设备和配置
        self.config = None
        self.device = None
        self.restart_task_instance = None
        self.account_data = []
        
    def load_account_config(self):
        """加载账号配置文件"""
        try:
            with open(self.account_config_file, 'r', encoding='utf-8') as f:
                self.account_data = json.load(f)
            logger.info(f"成功加载 {len(self.account_data)} 个账号配置")
            return True
        except Exception as e:
            logger.error(f"加载账号配置失败: {e}")
            return False
    
    def copy_config(self):
        """复制配置文件"""
        os.system(f'copy {self.daliy_json} {self.target_json}')
    
    def init_device(self):
        """初始化设备和任务"""
        self.config = Config('multi_account')
        self.device = Device(self.config)
        self.restart_task_instance = restart_task(self.config, self.device)
        self.restart_task_instance.app_start()
    
    def switch_account(self, account_info):
        """
        切换到指定账号
        
        Args:
            account_info: 账号信息字典
            
        Returns:
            bool: 切换是否成功
        """
        账号 = account_info.get("账号")
        系统 = account_info.get("系统")
        角色 = account_info.get("角色")
        服务器 = account_info.get("服务器")
        
        logger.info(f"开始切换账号: {账号} - {角色} ({服务器})")
        
        try:
            and_or_ios = True if 系统 == "and" else False
            toAccount = AccountInfo(
                account=账号,
                apple_or_android=and_or_ios,
                character=角色,
                svr="网易一" + 服务器
            )
            sa = SwitchAccount(self.config, self.device, toAccount)
            sa.switchAccount()
            return True
        except Exception as e:
            logger.error(f"账号 {账号}-{角色} 切换失败: {e}")
            return False
    
    def execute_task_for_account(self, account_info):
        """
        为单个账号执行任务 (子类需要重写此方法)
        
        Args:
            account_info: 账号信息字典
        """
        raise NotImplementedError("子类必须实现 execute_task_for_account 方法")
    
    def run(self):
        """主执行流程"""
        logger.info("=" * 60)
        logger.info(f"开始执行: {self.task_name}")
        logger.info("=" * 60)
        
        # 1. 复制配置文件
        self.copy_config()
        
        # 2. 加载账号配置
        if not self.load_account_config():
            logger.error("加载账号配置失败,任务终止")
            return
        
        # 3. 初始化设备
        self.init_device()
        
        # 4. 遍历账号执行任务
        for account_info in self.account_data:
            账号 = account_info.get("账号")
            角色 = account_info.get("角色")
            
            # 切换账号
            if not self.switch_account(account_info):
                logger.error(f"账号 {账号}-{角色} 切换失败,跳过该账号")
                continue
            
            # 执行任务
            try:
                self.execute_task_for_account(account_info)
                logger.info(f"账号 {账号}-{角色} 任务完成")
            except Exception as e:
                logger.error(f"账号 {账号}-{角色} 任务执行失败: {e}")
            
            # 等待一段时间再处理下一个账号
            sleep(5 + random.random() * 5)
        
        # 5. 停止应用
        self.restart_task_instance.app_stop()
        logger.info(f"{self.task_name} 全部完成")


# 通用任务函数 - 可以被各个任务脚本复用

def ensure_page_main(task_instance):
    """确保返回主页"""
    if task_instance.ui_get_current_page() != page_main:
        task_instance.ui_goto(page_main)


def create_task_instance(config, device, task_class):
    """
    创建任务实例的工厂函数
    
    Args:
        config: 配置对象
        device: 设备对象
        task_class: 任务类
        
    Returns:
        任务实例
    """
    return task_class(config, device)
