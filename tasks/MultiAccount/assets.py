from module.atom.image import RuleImage
from module.atom.click import RuleClick
from module.atom.long_click import RuleLongClick
from module.atom.swipe import RuleSwipe
from module.atom.ocr import RuleOcr
from module.atom.list import RuleList

# This file was automatically generated by ./dev_tools/assets_extract.py.
# Don't modify it manually.
class MultiAccountAssets: 


	# Image Rule Assets
	# 同心队中心 
	I_TEAM_HOME = RuleImage(roi_front=(932,269,38,38), roi_back=(932,269,38,38), threshold=0.8, method="Template matching", file="./tasks/MultiAccount/resource/team_home.png")
	# 一键寄存 
	I_ONE_STEP_SOURCE = RuleImage(roi_front=(1186,472,72,142), roi_back=(1186,472,72,142), threshold=0.8, method="Template matching", file="./tasks/MultiAccount/resource/one_step_source.png")
	# 集结 
	I_UNION = RuleImage(roi_front=(1095,625,86,59), roi_back=(1095,625,86,59), threshold=0.8, method="Template matching", file="./tasks/MultiAccount/resource/union.png")
	# 御魂副本集结 
	I_YUHUN_UNION = RuleImage(roi_front=(415,317,454,51), roi_back=(415,317,454,51), threshold=0.8, method="Template matching", file="./tasks/MultiAccount/resource/yuhun_union.png")
	# 组队 
	I_MISSION = RuleImage(roi_front=(964,644,67,42), roi_back=(964,644,67,42), threshold=0.8, method="Template matching", file="./tasks/MultiAccount/resource/mission.png")
	# 打开自动 
	I_AUTO = RuleImage(roi_front=(263,649,18,18), roi_back=(263,649,18,18), threshold=0.8, method="Template matching", file="./tasks/MultiAccount/resource/auto.png")


