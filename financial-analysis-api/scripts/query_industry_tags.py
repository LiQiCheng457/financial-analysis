"""
查询数据库中的行业数据，生成行业标签分组
"""
import sys
import os
import json
from collections import defaultdict

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from sqlalchemy import text

def query_industries():
    """查询所有公司的行业信息"""
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
        
        eastmoney_industries = set()
        regulatory_industries = set()
        
        for row in result:
            if row.eastmoney_industry:
                eastmoney_industries.add(row.eastmoney_industry)
            if row.regulatory_industry:
                regulatory_industries.add(row.regulatory_industry)
        
        print("=" * 60)
        print("东财行业分类:")
        print("=" * 60)
        for industry in sorted(eastmoney_industries):
            print(f"  - {industry}")
        
        print("\n" + "=" * 60)
        print("证监会行业分类:")
        print("=" * 60)
        for industry in sorted(regulatory_industries):
            print(f"  - {industry}")
        
        print("\n" + "=" * 60)
        print(f"东财行业总数: {len(eastmoney_industries)}")
        print(f"证监会行业总数: {len(regulatory_industries)}")
        print("=" * 60)
        
        # 生成分组建议
        print("\n生成前端行业标签分组建议...")
        generate_industry_groups(eastmoney_industries, regulatory_industries)
        
    finally:
        db.close()

def generate_industry_groups(eastmoney_industries, regulatory_industries):
    """根据行业数据生成分组"""
    
    # 合并所有行业
    all_industries = sorted(eastmoney_industries.union(regulatory_industries))
    
    # 定义分类规则
    groups = {
        '一次能源': ['煤炭', '石油', '天然气', '电力', '新能源', '燃气', '水务'],
        '二次产物': ['化工', '石化', '基础化工', '化学制品', '塑料', '橡胶', '化纤'],
        '能源产业': ['采掘', '钢铁', '有色金属', '黑色金属', '贵金属', '稀土', '矿业', '金属'],
        '能源项目': ['机械', '设备', '电气设备', '电力设备', '仪器仪表', '专用设备', '通用设备'],
        '能源交易': ['银行', '保险', '证券', '金融', '信托', '多元金融', '房地产', '商业'],
        '工业制造': ['汽车', '家电', '电子', '计算机', '通信', '传媒', '轻工', '纺织', '建筑', '交运'],
        '主要消费': ['食品', '饮料', '农林牧渔', '医药', '生物', '医疗'],
        '其他': []  # 其他未分类的
    }
    
    # 自动分类
    categorized = defaultdict(list)
    uncategorized = []
    
    for industry in all_industries:
        found = False
        for group_name, keywords in groups.items():
            if group_name == '其他':
                continue
            for keyword in keywords:
                if keyword in industry:
                    categorized[group_name].append(industry)
                    found = True
                    break
            if found:
                break
        if not found:
            uncategorized.append(industry)
    
    # 将未分类的添加到"其他"
    if uncategorized:
        categorized['其他'] = uncategorized
    
    # 输出分组结果
    print("\n自动分组结果（用于前端配置）:")
    print("=" * 60)
    
    result = []
    for group_name in ['一次能源', '二次产物', '能源产业', '能源项目', '能源交易', '工业制造', '主要消费', '其他']:
        if group_name in categorized and categorized[group_name]:
            tags = categorized[group_name]
            result.append({
                'name': group_name,
                'tags': tags
            })
            print(f"\n{group_name}:")
            for tag in tags:
                print(f"  - {tag}")
    
    # 输出 TypeScript 代码
    print("\n" + "=" * 60)
    print("TypeScript 代码片段:")
    print("=" * 60)
    print("const industryGroups = [")
    for group in result:
        print(f"  {{")
        print(f"    name: '{group['name']}',")
        print(f"    tags: {json.dumps(group['tags'], ensure_ascii=False)}")
        print(f"  }},")
    print("]")

if __name__ == "__main__":
    print("开始查询数据库中的行业数据...")
    query_industries()
    print("\n查询完成!")
