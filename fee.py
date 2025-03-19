import pandas as pd
import streamlit as st

# 设置页面标题和配置
st.set_page_config(page_title="运费计算工具", layout="wide")
st.title("运费计算工具")

try:
    # 读取Excel文件，设置多级表头
    df = pd.read_excel('运费报价模板V1.1(1).xlsx', sheet_name='车辆价格')
    
    # 创建两列布局
    col1, col2 = st.columns(2)
    
    with col1:
        # 选择载重
        weight = st.selectbox(
            "选择载重",
            ['4.2M', '6.8M', '7.9M', '9.6M', '12.5M'],
            help="请选择车辆载重"
        )
        
        # 选择提货地点
        start_location = st.selectbox(
            "选择提货地点",
            ['南京提货', '盐城提货'],
            help="请选择起始地点"
        )
        
        # 获取所有有效的送货地址（第二列，排除空值）
        destinations = df.iloc[:, 1].dropna().unique()
        destination = st.selectbox(
            "选择送货地址",
            sorted(destinations),
            help="请选择目的地"
        )

    # 获取价格信息
    row = df[df.iloc[:, 1] == destination].iloc[0]
    
    # 根据选择获取对应的价格
    location_prefix = '南京提货' if start_location == '南京提货' else '盐城提货'
    
    # 获取专车价格和单公里价格
    # 使用iloc来获取对应的列，因为我们知道列的顺序
    if location_prefix == '南京提货':
        col_idx = {'4.2M': (2,3), '6.8M': (6,7), '7.9M': (10,11), '9.6M': (14,15), '12.5M': (18,19)}
    else:
        col_idx = {'4.2M': (4,5), '6.8M': (8,9), '7.9M': (12,13), '9.6M': (16,17), '12.5M': (20,21)}
    
    special_price = row.iloc[col_idx[weight][0]]
    per_km_price = row.iloc[col_idx[weight][1]]
    
    with col2:
        st.info(f"📌 专车价格: {special_price} RMB")
        st.info(f"📍 单公里价格: {per_km_price} RMB/km")
        
        # 输入公里数
        km = st.number_input(
            "输入公里数",
            min_value=0.0,
            step=0.1,
            help="请输入运输距离（公里）"
        )
        
        # 计算总价
        total_cost = km * per_km_price
        
        # 显示总价
        st.success(f"💰 总费用: {total_cost:.2f} RMB")

except Exception as e:
    st.error(f"发生错误: {str(e)}")
    st.error("请确保Excel文件'运费报价模板V1.1(1).xlsx'存在且格式正确。")