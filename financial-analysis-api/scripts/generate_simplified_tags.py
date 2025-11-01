"""
生成简化的行业标签，用于前端UI
"""
import sys
import os
from collections import defaultdict

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from sqlalchemy import text

def extract_simplified_tags():
    """提取简化的行业标签"""
    db = SessionLocal()
    try:
        # 查询所有不重复的行业
        query = """
        SELECT DISTINCT 
            eastmoney_industry,
            regulatory_industry
        FROM stock_basic_info
        WHERE eastmoney_industry IS NOT NULL 
           OR regulatory_industry IS NOT NULL
        """
        
        result = db.execute(text(query))
        
        # 提取一级和二级分类
        eastmoney_tags = set()
        regulatory_tags = set()
        
        for row in result:
            # 东财行业：取前两级
            if row.eastmoney_industry:
                parts = row.eastmoney_industry.split('-')
                if len(parts) >= 2:
                    # 只取一级和二级分类
                    eastmoney_tags.add(f"{parts[0]}-{parts[1]}")
                elif len(parts) == 1:
                    eastmoney_tags.add(parts[0])
            
            # 证监会行业：取一级分类
            if row.regulatory_industry:
                parts = row.regulatory_industry.split('-')
                if len(parts) >= 1:
                    regulatory_tags.add(parts[0])
        
        print("=" * 80)
        print("简化后的东财行业标签（一级-二级）:")
        print("=" * 80)
        for tag in sorted(eastmoney_tags):
            print(f"  - {tag}")
        
        print("\n" + "=" * 80)
        print("简化后的证监会行业标签（一级）:")
        print("=" * 80)
        for tag in sorted(regulatory_tags):
            print(f"  - {tag}")
        
        # 生成分组
        all_tags = sorted(eastmoney_tags.union(regulatory_tags))
        
        # 定义分组规则（基于关键词匹配）
        groups = {
            '一次能源': ['煤炭', '石油', '天然气', '电力', '燃气', '水务', '化石能源', '采矿业'],
            '二次产物': ['化工', '化学', '石化', '塑料', '橡胶', '化纤', '基础化工'],
            '能源产业': ['金属', '钢铁', '有色', '矿', '冶炼'],
            '能源项目': ['机械', '设备', '电气', '电子', '仪器', '交运设备'],
            '能源交易': ['金融', '银行', '保险', '证券', '房地产', '商贸'],
            '工业制造': ['汽车', '家电', '纺织', '服装', '建筑', '轻工', '制造业'],
            '主要消费': ['农', '林', '牧', '渔', '食品', '饮料', '医药', '生物'],
            '其他': []  # 其他未分类的
        }
        
        # 自动分类
        categorized = defaultdict(list)
        uncategorized = []
        
        for tag in all_tags:
            found = False
            for group_name, keywords in groups.items():
                if group_name == '其他':
                    continue
                for keyword in keywords:
                    if keyword in tag:
                        categorized[group_name].append(tag)
                        found = True
                        break
                if found:
                    break
            if not found:
                uncategorized.append(tag)
        
        # 将未分类的添加到"其他"
        if uncategorized:
            categorized['其他'] = uncategorized
        
        # 输出分组结果
        print("\n" + "=" * 80)
        print("简化分组结果（用于前端UI）:")
        print("=" * 80)
        
        result = []
        for group_name in ['一次能源', '二次产物', '能源产业', '能源项目', '能源交易', '工业制造', '主要消费', '其他']:
            if group_name in categorized and categorized[group_name]:
                tags = categorized[group_name]
                result.append({
                    'name': group_name,
                    'tags': tags
                })
                print(f"\n{group_name} ({len(tags)} 个标签):")
                for tag in tags[:10]:  # 只显示前10个
                    print(f"  - {tag}")
                if len(tags) > 10:
                    print(f"  ... 还有 {len(tags) - 10} 个")
        
        # 输出 TypeScript 代码（更简洁）
        print("\n" + "=" * 80)
        print("TypeScript 代码片段（用于 Snapshot.vue）:")
        print("=" * 80)
        print("const industryGroups = [")
        for group in result:
            print(f"  {{")
            print(f"    name: '{group['name']}',")
            # 格式化tags，每行不超过80字符
            tags_str = str(group['tags'])
            if len(tags_str) > 80:
                # 如果太长，简化输出
                print(f"    tags: [")
                for tag in group['tags']:
                    print(f"      '{tag}',")
                print(f"    ]")
            else:
                print(f"    tags: {tags_str}")
            print(f"  }},")
        print("]")
        
    finally:
        db.close()

if __name__ == "__main__":
    print("开始提取简化的行业标签...")
    extract_simplified_tags()
    print("\n提取完成!")
