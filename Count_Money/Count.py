import os
import glob
from tqdm import tqdm
import numpy as np
import zhplot
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from pylab import mpl
from scipy.optimize import minimize
import pandas as pd # 处理csv
import argparse # 传参

def Count_Day(Model, Data, Date):
    if Model == 0: # Cost
        data = Data[Data["Property"] == -1]
    elif Model == 1: # Income
        data = Data[Data["Property"] == 1]
    Type = data["Type"].unique()
    data = data[data["Date"] == Date]    
    # Total Cost
    Total = np.sum(data["Quantity"])
    # Detailed Cost
    Detailed = []
    for index in Type:
        temp_data = data[data["Type"] == index]
        temp_cost = np.sum(temp_data["Quantity"])
        Detailed.append(temp_cost)
    # Return
    res = np.array([Total] + Detailed)
    return res

def Count_All(Data):
    # Preliminary Info
    Date = Data["Date"].unique()
    Cost_Type = Data[Data["Property"] == -1]["Type"].unique()
    Income_Type = Data[Data["Property"] == 1]["Type"].unique()
    # Loop
    Cost = np.empty((len(Date), len(Cost_Type) + 2), dtype=object)
    Income = np.empty((len(Date), len(Income_Type) + 2), dtype=object)
    index = 0
    for date in Date:
        # Cost
        day_res = Count_Day(0, Data, date)
        Cost[index, 0] = date
        Cost[index, 1:] = day_res
        # Income
        day_res = Count_Day(1, Data, date)
        Income[index, 0] = date
        Income[index, 1:] = day_res
        index = index + 1
    # Process Type
    Cost_Type = np.insert(Cost_Type, 0, ["Date","Total"])
    Income_Type = np.insert(Income_Type, 0, ["Date","Total"])
    # Plot
    temp_cost = Cost[:, 1: -1]
    temp_cost = np.sum(temp_cost, axis=0)
    temp_income = Income[:, 1: -1]
    temp_income = np.sum(temp_income, axis=0)
    # 设置类别标签（根据你的实际数据调整）
    categories = ["2025-01"]

    # 设置绘图
    fig, ax = plt.subplots(figsize=(15, 10))

    # 堆叠柱状图的底部位置
    bottoms_cost = np.zeros(temp_cost.shape[0])
    bottoms_income = np.zeros(temp_income.shape[0])

    # 绘制成本的堆叠柱状图
    for i in range(temp_cost.shape[0]):  # 按列堆叠
        ax.barh(categories, temp_cost[i], left=bottoms_cost, label=f"{Cost_Type[i + 2]}")
        bottoms_cost += temp_cost[i]  # 更新成本的底部位置

    # 绘制收入的堆叠柱状图
    for i in range(temp_income.shape[0]):  # 按列堆叠
        ax.barh(categories, temp_income[i], left=bottoms_income, label=f"{Income_Type[i + 2]}")
        bottoms_income += temp_income[i]  # 更新收入的底部位置

    # 添加标签和标题
    ax.set_xlabel("金额")
    ax.set_title("每月支出与收入")
    ax.legend()

    # 显示图形
    plt.tight_layout()
    plt.show()


CSV_File = "/mnt/e/账本/2025.01.csv"
data = pd.read_csv(CSV_File, encoding='utf-8')

Count_All(data)
