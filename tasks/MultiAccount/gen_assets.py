import sys
import os
cur_path = os.path.abspath(__file__)
oas_path = cur_path.split("tasks")[0]
sys.path.append(oas_path)
from dev_tools.assets_extract import AssetsExtractor

ae = AssetsExtractor(oas_path + "\\tasks\\MultiAccount")
ae.extract()



