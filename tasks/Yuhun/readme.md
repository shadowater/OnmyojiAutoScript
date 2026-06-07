# 御魂强化自动化

目标：自动完成阴阳师御魂批量强化。流程从御魂选择页开始，逐个识别御魂类型、等级、主属性和副属性，调用 `yuhun/enhancement_system` 判断是否值得强化；不值得则取消选中，直到选满 6 个。随后进入强化设置页执行计算和强化，再在强化结果页判断继续强化或弃置，循环直到御魂强化到 15 或弃置。

## 开发规范

新流程开发统一按这个顺序推进：

1. 规划流程：明确目标、页面划分、页面动作、终止条件和状态器。
2. 约定单页素材：先写清素材用途、类型、检测方式、是否阵列、坐标来源、验证截图和动态规则。
3. 生成素材并截图验证：生成配置、裁剪模板、输出标注图，用户确认后继续。
4. 逐页重复素材准备：一个页面稳定后再进入下一个页面。
5. 流程脚本调试：连接模拟器实际跑流程，每一步识别后都要求用户输入 `y/n`，`n` 则停止并回到素材配置。

脚本运行时只依赖两类识别：`OCR` 和 `Template matching`。

## 目录规范

```text
tasks/Yuhun/
├── readme.md                 # 本文：流程、规范、素材大纲、TODO
├── asset_temp/               # 标定用源截图和工具输出，避开 assets_extract.py
│   ├── README.md
│   ├── select/               # 选择页源截图和参考图
│   ├── enhance/              # 强化设置页源截图和参考图
│   ├── result/               # 强化结果页源截图和参考图
│   └── _unused/              # 暂不使用的参考截图
├── select/                   # 御魂选择页面素材
│   ├── temp_layout.json      # 页面源布局，只存人工可维护参数
│   ├── image.json            # 模板匹配素材
│   ├── ocr.json              # OCR 素材
│   ├── click.json            # 点击区域
│   └── *.png                 # 裁剪后的模板图
├── enhance/                  # 强化设置页面素材
├── result/                   # 强化结果页面素材
├── tools/                    # bbox、素材生成、OCR 测试工具
├── config.py
└── yuhun/enhancement_system/ # 是否值得强化的决策逻辑
```

目录约定：

- `asset_temp/<page>/` 放原始截图、Gemini bbox JSON 和标注 PNG。
- 标注图与源图同目录，文件名使用 `*_标注.png`、`*_布局标注.png`、`*_强化标注.png`。
- 页面目录按页面语义命名，如 `select/`、`enhance/`、`result/`。
- `temp_layout.json` 是源配置，不写入大量派生 bbox；文件名带 `temp`，避免 `assets_extract.py` 扫描。
- `image.json`、`ocr.json`、`click.json` 是运行时资产输入，可由工具从 `temp_layout.json` 同步生成。
- 裁剪得到的运行时模板图必须放在对应页面目录，和 `image.json` 同目录，以符合 `assets_extract.py` 的 `imageName` 路径约定。

`assets_extract.py` 约束：

- 它会递归读取任务目录下所有 `*.json`，但跳过路径中包含 `temp` 的文件。
- 它生成 `RuleImage.file` 时只使用 `image.json` 所在目录加 `imageName`，不读取 `sourceImage`。
- 因此，所有非运行时 JSON 必须放在带 `temp` 的路径中，例如 `asset_temp/` 或 `temp_layout.json`。
- 运行时模板 PNG 必须和对应页面的 `image.json` 放在同一个目录，例如 `enhance/enhance_calc.png`。
- `sourceImage` 只给素材准备工具使用，用于从 `asset_temp/<page>/` 的源截图裁剪运行时模板。

单页素材规范：

- 每个页面目录都保留 `temp_layout.json`，作为人工维护的 bbox 源配置。
- `temp_layout.json` 只存手动标定参数，如按钮 ROI、阵列起点、间距、动态规则；不要写入大量派生坐标。
- `prepare_yuhun_assets.py` 负责从 `temp_layout.json` 同步生成或更新 `image.json`、`ocr.json`、`click.json`。
- `asset_temp/<page>/` 中的源图、bbox JSON、标注 PNG 只用于开发和验证，不作为运行时资产直接引用。
- 用户确认标注图后，再运行 `--crop-only` 生成页面目录下的运行时模板 PNG。

素材准备闭环：

1. 提供素材描述：在文档和 `tools/bbox_targets.yaml` 中说明当前页面有哪些素材、用途、识别方式、是否阵列、是否有动态规则。
2. Gemini 初步标框：运行 `yuhun_bbox_tool.py detect --review`，在 `asset_temp/<page>/` 的源图旁生成 `<截图名>.json` 和 `<截图名>_标注.png`。
3. 生成源布局：根据 Gemini bbox JSON 和页面规则，由素材脚本生成或更新页面目录下的 `temp_layout.json`。
4. 人工微调：人工查看 `*_标注.png`、`*_布局标注.png`、`*_强化标注.png`，只修改 `temp_layout.json` 中需要手动维护的源参数。
5. 同步运行时资产：运行 `prepare_yuhun_assets.py --crop-only`，脚本基于 `temp_layout.json` 更新 `image.json`、`ocr.json`、`click.json`，并裁剪运行时模板 PNG。
6. 验证后提取：标注图和 OCR 测试通过后，再运行 `dev_tools/assets_extract.py` 生成运行时 `assets.py`。

## 工具链

素材准备工具链：

1. `tools/bbox_targets.yaml`：记录每张 `asset_temp/<page>/*.png` 要交给 Gemini 检测的 UI 元素。
2. `yuhun_bbox_tool.py`：调用 Gemini 标框，在源图同目录输出 bbox JSON 和 `*_标注.png`。
3. `prepare_yuhun_assets.py`：基于 `temp_layout.json` 同步运行时 JSON、裁剪模板、生成页面标注图、测试 OCR。
4. `dev_tools/assets_extract.py`：从页面目录的运行时 JSON 和模板 PNG 生成 `assets.py`。

常用命令：

```powershell
.\toolkit\python tasks\Yuhun\tools\yuhun_bbox_tool.py status
.\toolkit\python tasks\Yuhun\tools\yuhun_bbox_tool.py detect --review
.\toolkit\python tasks\Yuhun\tools\prepare_yuhun_assets.py --status
.\toolkit\python tasks\Yuhun\tools\prepare_yuhun_assets.py --crop-only
.\toolkit\python tasks\Yuhun\tools\prepare_yuhun_assets.py --annotate-select --select-capture select_one_detail.png
.\toolkit\python tasks\Yuhun\tools\prepare_yuhun_assets.py --annotate-enhance
$env:PYTHONIOENCODING='utf-8'; .\toolkit\python tasks\Yuhun\tools\prepare_yuhun_assets.py --test-select-ocr --select-capture select_one_detail.png
.\toolkit\python dev_tools\assets_extract.py
```

## 素材描述规范

每个素材都应说明：

| 字段 | 含义 | 是否必填 |
|------|------|----------|
| `itemName` | 程序内唯一名称 | 是 |
| `description` | 给用户和模型看的语义描述 | 是 |
| `assetType` | `click`、`ocr`、`template`、`layout`、`array` | 建议 |
| `method` | `OCR` 或 `Template matching`；点击区域可为空 | 识别素材必填 |
| `array.enabled` | 是否由阵列规则生成 | 阵列素材必填 |
| `array.source` | 阵列源配置，如 `select/temp_layout.json` | 阵列素材必填 |
| `sourceImage` | 裁剪模板使用的截图 | 模板素材必填 |
| `roiFront` / `roiBack` | 运行时 ROI | 运行时素材必填 |
| `dynamicRules` | 动态调整规则，如等级 `>=3` 时宽度减少 | 有动态规则时必填 |

现有框架已经使用 `itemName`、`description`、`method`、`sourceImage`、`roiFront`、`roiBack`。后续新增字段用于文档化和通用工具扩展，运行时代码可以暂时忽略。

## 页面流程

| 页面 | 目标 | 大致动作 | 进入下一页条件 |
|------|------|----------|----------------|
| 御魂选择页面 | 选出 6 个值得强化的御魂 | 点击候选御魂、OCR 详情、计算 worth、不值得则取消选中、最终校验选中状态 | 选中数量为 6，状态器与画面一致 |
| 强化设置页面 | 对已选御魂执行计算和强化 | 点击计算、确认强化 | 强化动作完成并进入结果页 |
| 强化结果页面 | 判断继续强化或弃置 | OCR 结果等级和副属性加成，保留值得继续强化的御魂，弃置不值得的御魂 | 本轮处理完成，返回选择页或继续强化 |

## 御魂选择页

目标：在 4x4 待整理区中逐个检查御魂，直到选中 6 个值得强化的御魂。

素材清单：

| 素材 | 类型 | 检测方式 | 是否阵列 | 说明 |
|------|------|----------|----------|------|
| `grid_spec` | `layout` | 脚本推导 | 是 | 只维护第一个御魂 bbox、横纵间距、御魂尺寸，生成 16 个候选格 |
| `slot_1..slot_16` | `click` | 点击区域 | 是 | 由 `grid_spec` 生成，用于点击候选御魂 |
| `select_slot_1_selected..select_slot_16_selected` | `template` | `Template matching` | 是 | 使用单模板 `select_slot_selected.png`，在每个平移 ROI 内判断是否选中 |
| `soul_type_level` | `ocr` | `OCR` | 否 | 位于详情弹窗，识别御魂类型和等级，如 `招财猫+12` |
| `detail_main_attr` | `ocr` | `OCR` | 否 | 详情弹窗主属性；等级 `>=3` 时宽度减少 30 px |
| `detail_sub_attr_1..4` | `ocr` | `OCR` | 否 | 详情弹窗副属性；等级 `>=3` 时宽度减少 30 px |
| `select_confirm_count` | `ocr` | `OCR` | 否 | 右侧确认区 `(N/12)`，用于校验选中数量 |
| `select_enhance_all` | `template` | `Template matching` | 否 | 点击「全部强化」进入强化设置页 |

选择页伪代码：

```text
state = {
  checked_slots: {},      # slot_index -> soul_info
  expected_selected: {},  # slot_index -> bool
  actual_selected: {},    # slot_index -> bool
  selected_count: 0
}

for slot_index in 待整理区格子顺序:
  if state.selected_count >= 6:
    break

  click(slot_index)  # 打开详情，同时默认选中该御魂

  soul_type_level_text = ocr_soul_type_level()
  level = parse_level(soul_type_level_text)
  set_name = parse_soul_type(soul_type_level_text) or config.default_soul_set

  attr_ocr_rois = config.detail_attr_rois
  if level >= 3:
    attr_ocr_rois = shrink_width(attr_ocr_rois, 30)

  soul_info = {
    level: level,
    set_name: set_name,
    main_attr: ocr_detail_main_attr(attr_ocr_rois.main_attr),
    sub_attrs: ocr_detail_sub_attrs(attr_ocr_rois.sub_attrs)
  }

  worth = enhancement_calculator.is_worth_enhancing(soul_info)
  state.checked_slots[slot_index] = soul_info
  state.expected_selected[slot_index] = worth

  if not worth:
    click(slot_index)  # 取消选中
  else:
    state.selected_count += 1

if state.selected_count != 6:
  report_error("未选满 6 个值得强化的御魂")
  stop

for slot_index, soul_info in state.checked_slots:
  recalculated_worth = enhancement_calculator.is_worth_enhancing(soul_info)
  if recalculated_worth != state.expected_selected[slot_index]:
    report_error("状态器记录与最终计算结果不一致")
    stop

for slot_index, expected in state.expected_selected:
  actual = check_slot_selected(slot_index)
  state.actual_selected[slot_index] = actual
  if actual != expected:
    report_error("御魂选中状态与状态器不一致")
    stop

click(select_enhance_all)
```

## 强化设置页

目标：对已选 6 个御魂执行计算和强化。

| 素材 | 类型 | 检测方式 | 是否阵列 | 说明 |
|------|------|----------|----------|------|
| `enhance/temp_layout.json` | `layout` | 脚本同步 | 否 | 强化设置页按钮模板 ROI 源配置 |
| `enhance_calc` | `template` | `Template matching` | 否 | 计算按钮 |
| `enhance_confirm` | `template` | `Template matching` | 否 | 强化确认按钮或确认弹窗按钮 |

待补充：

- 计算完成后的状态确认素材。
- 强化失败或资源不足的异常状态素材。

## 强化结果页

目标：识别强化结果，决定继续强化或弃置。

| 素材 | 类型 | 检测方式 | 是否阵列 | 说明 |
|------|------|----------|----------|------|
| `result_slot_1..6` | `click` | 点击区域 | 是 | 结果页 6 个御魂位置 |
| `result_level_1..6` | `ocr` | `OCR` | 是 | 结果页每个御魂等级 |
| `result_sub_bonus_*` | `ocr` | `OCR` | 待定 | 本轮强化提升的副属性类型和值 |
| `result_soul_selected` | `template` | `Template matching` | 待定 | 判断结果页御魂是否选中 |
| `result_enhance` | `template` | `Template matching` | 否 | 继续强化按钮 |
| `result_discard` | `template` | `Template matching` | 否 | 弃置按钮 |
| `result_back` | `template` | `Template matching` | 否 | 返回选择页 |

待补充：

- 结果页 6 个御魂是否也是规则阵列。
- 本轮副属性强化项的 OCR 区域。
- 继续强化弹窗或二次确认状态。

## TODO

### 素材工具链

- [x] 建立 `asset_temp/`、`select/`、`enhance/`、`result/`、`tools/` 目录结构
- [x] 准备 `bbox_targets.yaml`，描述每张截图需要 Gemini 定位的 UI 元素
- [x] 实现 `yuhun_bbox_tool.py detect --review`
- [x] 实现 `prepare_yuhun_assets.py --crop-only`
- [x] 用 `select_slot_selected.png` 单模板匹配判断待整理区御魂是否选中
- [x] 选择页 OCR 测试通过，并支持等级 `>=3` 时属性框宽度减少 30 px
- [ ] 根据确认后的 bbox 微调 `result/temp_layout.json`、各 `image.json` / `ocr.json`
- [ ] 运行 `dev_tools/assets_extract.py` 生成 `tasks/Yuhun/assets.py`

### 强化流程实现

- [ ] 新建/完善 `script_task.py`，连接模拟器并进入御魂批量强化界面
- [ ] 选择界面：依次点击御魂，OCR 识别类型、等级、主属性、副属性
- [ ] 每步识别后等待用户输入 `y/n`，`n` 则退出并提示重新准备 bbox / 配置
- [ ] 调用 `yuhun/enhancement_system` 判断是否值得强化；不值得则取消选中
- [ ] 选满 6 个后点击「全部强化」→「计算」→「强化」
- [ ] 结果页：识别 6 个御魂等级和本轮副属性强化项
- [ ] 结果页：值得继续强化的御魂保持/选中，不值得的选择「弃置」
- [ ] 循环直到全部御魂强化到 15 或弃置
- [ ] 点击返回，回到御魂选择界面继续下一轮