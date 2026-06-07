# -*- coding: utf-8 -*-
"""
阴阳师御魂数据转换工具 - 带御魂名称版
只用第一个文件，通过suit_id映射表显示中文名称
"""

import argparse
import json
from pathlib import Path

# ============ 御魂ID到名称映射表（从第二个文件提取）============
SUIT_ID_TO_NAME = {
    300002: "雪幽魂",
    300003: "地藏像",
    300004: "蝠翼",
    300006: "涅槃之火",
    300007: "三味",
    300008: "魍魉之匣",
    300009: "被服",
    300010: "招财猫",
    300011: "反枕",
    300012: "轮入道",
    300013: "日女巳时",
    300014: "镜姬",
    300015: "钟灵",
    300018: "狰",
    300019: "火灵",
    300020: "鸣屋",
    300021: "薙魂",
    300022: "心眼",
    300023: "木魅",
    300024: "树妖",
    300026: "网切",
    300027: "阴摩罗",
    300029: "伤魂鸟",
    300030: "破势",
    300031: "镇墓兽",
    300032: "珍珠",
    300033: "骰子鬼",
    300034: "蚌精",
    300035: "魅妖",
    300036: "针女",
    300039: "返魂香",
    300048: "狂骨",
    300049: "幽谷响",
    300050: "土蜘蛛",
    300051: "胧车",
    300052: "荒骷髅",
    300053: "地震鲶",
    300054: "蜃气楼",
    300055: "片叶之苇",
    300056: "尘冢",
    300057: "油赤子",
    300058: "夜啼石",
    300059: "夜送犬",
    300060: "雨降",
    300073: "飞缘魔",
    300074: "兵主部",
    300075: "青女房",
    300076: "涂佛",
    300077: "鬼灵歌伎",
    300079: "遗念火",
    300080: "共潜",
    300081: "恶楼",
    300082: "贝吹坊",
    300083: "海月火玉",
    300084: "出世螺",
    300085: "火之车",
    300086: "隐念",
    300087: "叠叩",
    300088: "应声虫",
    300089: "元兴寺",
    300090: "钓瓶火",
    300091: "夜荒魂",
    300092: "无刀取",
    300093: "奉海图",
}

# ============ 属性编码映射表 ============
ATTR_CODE_MAP = {
    0: "EffectResistRate",
    1: "Defense",
    2: "Attack",
    3: "HpRate",
    4: "DefenseRate",
    5: "AttackRate",
    6: "Speed",
    7: "CritRate",
    8: "CritPower",
    9: "EffectHitRate",
    10: "Hp",
    11: "EffectResistRate",
}

ATTR_TYPE_MAP = {
    "Attack": "攻击",
    "Hp": "生命",
    "Defense": "防御",
    "AttackRate": "攻击加成",
    "HpRate": "生命加成",
    "DefenseRate": "防御加成",
    "CritRate": "暴击",
    "CritPower": "暴击伤害",
    "Speed": "速度",
    "EffectHitRate": "效果命中",
    "EffectResistRate": "效果抵抗",
}

# 各属性副属性的最大成长值
MAX_GROWTH = {
    "CritPower": 0.04,
    "CritRate": 0.03,
    "Speed": 3.0,
    "HpRate": 0.03,
    "AttackRate": 0.03,
    "DefenseRate": 0.03,
    "EffectHitRate": 0.04,
    "EffectResistRate": 0.04,
    "Attack": 27,
    "Defense": 5,
    "Hp": 114,
}

PERCENT_ATTRS = {"AttackRate", "HpRate", "DefenseRate", "CritRate",
                  "CritPower", "EffectHitRate", "EffectResistRate"}

# base_rindex 到主属性类型的映射
RINDEX_TO_MAIN_ATTR = {
    0: "Attack",
    1: "Defense",
    2: "Hp",
    3: "Speed",
    4: "CritRate",
}

# equip_id 对应位置映射（从导出数据提取）
EQUIP_ID_TO_POS = {
    110006: 1,
    120006: 2,
    130006: 3,
    140006: 4,
    150006: 5,
    160006: 6,
    180001: 1,
    180003: 3,
    180005: 5,
    180011: 5,
    180013: 1,
    180015: 3,
    180016: 4,
    180020: 2,
    190026: 4,
    190044: 4,
    190056: 2,
}

OTHERS_EQUIP_ID_MASK = (1 << 20) - 1
OTHERS_LEVEL_BASE = 0xC2
OTHERS_LEVEL_SHIFT = 40
OTHERS_SUIT_SHIFT = 20

# 主属性数值满级值
MAX_MAIN_VALUES = {
    (1, "Attack"): 486,
    (3, "Defense"): 104,
    (5, "Hp"): 2052,
    (2, "Speed"): 57,
    (2, "AttackRate"): 0.55,
    (2, "DefenseRate"): 0.55,
    (2, "HpRate"): 0.55,
    (4, "AttackRate"): 0.55,
    (4, "DefenseRate"): 0.55,
    (4, "HpRate"): 0.55,
    (4, "EffectHitRate"): 0.55,
    (4, "EffectResistRate"): 0.55,
    (6, "AttackRate"): 0.55,
    (6, "DefenseRate"): 0.55,
    (6, "HpRate"): 0.55,
    (6, "CritRate"): 0.55,
    (6, "CritPower"): 0.89,
}


def decode_suit_id(others):
    """解码御魂类型ID"""
    return (others >> OTHERS_SUIT_SHIFT) & OTHERS_EQUIP_ID_MASK


def decode_equip_id(others):
    """解码 equip_id（用于定位位置）"""
    return others & OTHERS_EQUIP_ID_MASK


def decode_level(others):
    """解码等级"""
    prefix = others >> OTHERS_LEVEL_SHIFT
    return (prefix - OTHERS_LEVEL_BASE) // 0x100


def get_suit_name(suit_id):
    """获取御魂名称"""
    return SUIT_ID_TO_NAME.get(suit_id, f"未知({suit_id})")


def decode_position(equip_id, base_rindex):
    """解码位置（优先使用 equip_id 规则）"""
    if equip_id in EQUIP_ID_TO_POS:
        return EQUIP_ID_TO_POS[equip_id]
    pos_map = {0: 1, 1: 3, 2: 5, 3: 2, 4: 6}
    return pos_map.get(base_rindex, 1)


def decode_main_attr(base_rindex):
    """解码主属性类型"""
    return RINDEX_TO_MAIN_ATTR.get(base_rindex, "Unknown")


def infer_main_value(pos, attr_type, level):
    """推断主属性数值"""
    max_val = MAX_MAIN_VALUES.get((pos, attr_type), 0)
    if level == 0:
        ratio = 0.1
    else:
        ratio = 0.1 + 0.9 * (level / 15)
    return max_val * ratio


def convert_ratio_to_value(attr_type, ratio):
    """将比例转换为游戏值"""
    max_growth = MAX_GROWTH.get(attr_type, 0.03)
    return ratio * max_growth


def format_value(attr_type, value):
    """格式化数值"""
    if attr_type in PERCENT_ATTRS:
        return f"{value*100:.2f}%"
    else:
        if value == int(value):
            return f"{int(value)}"
        return f"{value:.2f}"


def calc_times(value, attr_type):
    """计算强化次数"""
    avg = MAX_GROWTH.get(attr_type, 0.03) * 0.9
    if value <= 0:
        return 1
    times = max(1, round(value / avg))
    return min(times, 6)


def calc_effective_times(value, attr_type):
    """计算等效强化次数"""
    avg = MAX_GROWTH.get(attr_type, 0.03) * 0.9
    if value <= 0:
        return 1.0
    return round(value / avg, 2)


def parse_data(filepath):
    """解析数据文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = []
    
    for equip_id, equip_data in data.items():
        others = equip_data.get("others", 0)
        base_rindex = equip_data.get("base_rindex", 0)
        rattr = equip_data.get("rattr", [])
        
        # 解码
        equip_id = decode_equip_id(others)
        pos = decode_position(equip_id, base_rindex)
        main_attr = decode_main_attr(base_rindex)
        level = decode_level(others)
        suit_id = decode_suit_id(others)
        suit_name = get_suit_name(suit_id)
        
        # 主属性
        main_value = infer_main_value(pos, main_attr, level)
        
        # 副属性
        sub_attrs = []
        for item in rattr:
            if len(item) >= 2:
                code = item[0]
                ratio = item[1]
                
                attr_type = ATTR_CODE_MAP.get(code)
                if not attr_type:
                    continue
                
                game_value = convert_ratio_to_value(attr_type, ratio)
                
                sub_attrs.append({
                    "类型": ATTR_TYPE_MAP.get(attr_type, attr_type),
                    "数值": format_value(attr_type, game_value),
                    "强化次数": calc_times(game_value, attr_type),
                    "等效强化次数": calc_effective_times(game_value, attr_type),
                })
        
        results.append({
            "id": equip_id,
            "位置": pos,
            "类型": suit_name,  # 中文名称
            "类型ID": suit_id,
            "equip_id": equip_id,
            "等级": level,
            "主属性": {
                "类型": ATTR_TYPE_MAP.get(main_attr, main_attr),
                "数值": format_value(main_attr, main_value),
            },
            "副属性": sub_attrs,
        })
    
    return results


def main():
    parser = argparse.ArgumentParser(description="阴阳师御魂数据转换 - 带中文名称版")
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path("D:/Software/yys/yys-export.260515_0302_255/yys-export.260515_0303_129.json"),
        help="输入的 yys-export json 文件路径",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="输出 json 文件路径（默认与输入同目录）",
    )
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output or (input_file.parent / "yys_yuhun_with_names.json")
    
    print("=" * 70)
    print("阴阳师御魂数据转换 - 带中文名称版")
    print("=" * 70)
    print(f"输入: {input_file}")
    print(f"御魂种类: {len(SUIT_ID_TO_NAME)} 种")
    print()
    
    print("解析转换中...")
    results = parse_data(input_file)
    
    output = {
        "meta": {
            "description": "阴阳师御魂数据 - 只用第一个文件（带中文名称）",
            "count": len(results),
            "suit_types": len(SUIT_ID_TO_NAME),
            "note": "御魂名称通过suit_id查表获得，位置与等级通过 others 解码",
        },
        "equips": results,
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"输出: {output_file}")
    print(f"御魂数量: {len(results)}")
    
    # 统计
    pos_dist = {}
    suit_dist = {}
    for r in results:
        pos_dist[r["位置"]] = pos_dist.get(r["位置"], 0) + 1
        suit_dist[r["类型"]] = suit_dist.get(r["类型"], 0) + 1
    
    print(f"\n位置分布: {dict(sorted(pos_dist.items()))}")
    
    print("\n御魂类型分布（前10）:")
    for name, count in sorted(suit_dist.items(), key=lambda x: -x[1])[:10]:
        print(f"  {name}: {count}")
    
    print("\n前3个御魂预览:")
    print("-" * 70)
    for r in results[:3]:
        print(f"【{r['位置']}号位】{r['类型']} +{r['等级']}")
        print(f"  主属性: {r['主属性']['类型']}+{r['主属性']['数值']}")
        subs = [f"{s['类型']}+{s['数值']}({s['强化次数']}次)" for s in r['副属性']]
        print(f"  副属性: {' / '.join(subs)}")
        print()


if __name__ == "__main__":
    main()
