import os
import glob
from tqdm import tqdm
import numpy as np
import zhplot
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import zhplot
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd # 处理csv
import argparse # 传参

def Count_Day(Model, Data, Date, Type):
    if Model == 0: # Cost
        data = Data[Data["Property"] == -1]
    elif Model == 1: # Income
        data = Data[Data["Property"] == 1]
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

# 根据传入时间自动计算数据
def Compute_Date(Start_Date, End_Date, CSV_Path):
    data = pd.read_csv(CSV_Path, encoding='utf-8')
    # Preliminary Info
    Cost_Type = data[data["Property"] == -1]["Type"].unique()
    Income_Type = data[data["Property"] == 1]["Type"].unique()
    if Start_Date != "0" and End_Date != "0":
        data = data[(data["Date"] >= Start_Date) & (data["Date"] <= End_Date)]
    data = data.reset_index(drop=True)
    data.index = data.index + 1
    Date = data["Date"].unique()
    print(f"[Count_Head::Compute_Date] Start Date: {Date[0]}, End Date: {Date[-1]}")
    ######################################################################
    # Count
    Cost_Gross = np.empty((len(Date), len(Cost_Type) + 2), dtype=object)
    Income_Gross = np.empty((len(Date), len(Income_Type) + 2), dtype=object)
    index = 0
    for date in Date:
        # Cost_Gross
        day_res = Count_Day(0, data, date, Cost_Type)
        Cost_Gross[index, 0] = date
        Cost_Gross[index, 1:] = np.round(day_res, 4)
        # Income_Gross
        day_res = Count_Day(1, data, date, Income_Type)
        Income_Gross[index, 0] = date
        Income_Gross[index, 1:] = np.round(day_res, 4)
        index = index + 1
    # Process Type
    Cost_Type = np.insert(Cost_Type, 0, ["Date","Total"])
    Income_Type = np.insert(Income_Type, 0, ["Date","Total"])
    # Return
    return Date, Cost_Gross, Income_Gross, Cost_Type, Income_Type

# 绘制传入时间内的支出、收入图
def Plot_Everyday(Date, Cost_Gross, Income_Gross, Pic_Dir,interval = 1):
    Date_Plot = [datetime.strptime(date, "%Y-%m-%d") for date in Date]
    Cost_Gross_Plot = -1 * Cost_Gross[:, 1]
    Income_Gross_Plot = Income_Gross[:, 1]
    plt.figure(figsize=(10, 8))
    plt.plot(Date_Plot, Cost_Gross_Plot, color='green', label="支出")
    plt.bar(Date_Plot, Income_Gross_Plot, color='red', alpha=0.5, label="收入")
    for index, (date, cost) in enumerate(zip(Date_Plot, Cost_Gross_Plot)):
        plt.text(date, cost, f"{cost}", ha='center', va='bottom', fontsize=9)
    for index, (date, cost) in enumerate(zip(Date_Plot, Income_Gross_Plot)):
        plt.text(date, cost, f"{cost}", ha='center', va='bottom', fontsize=9)
    plt.title("每日收入与支出总览图")
    plt.xlabel("日期")
    plt.ylabel("花费金额")
    plt.yscale('symlog')
    # **扩展 x 轴范围，避免 1-1 被截断**
    plt.xlim(min(Date_Plot) - timedelta(days=0.5), max(Date_Plot) + timedelta(days=0.5))
    plt.ylim(1e-2, 1e5)
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interval))  # 1天一个刻度;
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))  # 只显示月-日
    plt.xticks(rotation=90, fontsize=8)
    # 添加网格线
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend()
    # plt.show()
    first = min(Date_Plot).date()
    end = max(Date_Plot).date()
    Pic_Path = Pic_Dir + f"/Cost_And_Income_{first}_{end}.jpg"
    plt.savefig(Pic_Path, dpi=500)
    plt.close()

# 绘制传入区间内支出的细节
def Plot_Cost_Details(Date, Cost_Gross, Cost_Type, Pic_Dir,interval = 1):
    Date_Plot = [datetime.strptime(date, "%Y-%m-%d") for date in Date]
    Cost_Gross_Plot = -1 * Cost_Gross[:, 2:]
    Cost_Gross_Type = Cost_Type[2:]
    plt.figure(figsize=(10, 8))
    bottom = np.zeros(len(Date_Plot))

    for index, type in enumerate(Cost_Gross_Type):
        bars = plt.bar(Date_Plot, Cost_Gross_Plot[:, index], label=type, bottom=bottom)

        # **在柱子顶部添加数值**
        for bar, value in zip(bars, Cost_Gross_Plot[:, index]):
            if value > 0 and value > 1:  # 避免负值显示
                plt.text(
                    bar.get_x() + bar.get_width() / 2,  # X 轴位置：柱子中心
                    bar.get_height() + bar.get_y() - 0.3*value,  # Y 轴位置：顶部 + 偏移量
                    f"{value:.1f}",  # 显示一位小数
                    ha='center', va='bottom', fontsize=8, color='black'
                )
            elif value > 0 and value < 1:
                plt.text(
                    bar.get_x() + bar.get_width() / 2,  # X 轴位置：柱子中心
                    bar.get_height() + bar.get_y() + 0.1*value,  # Y 轴位置：顶部 + 偏移量
                    f"{value:.1f}",  # 显示一位小数
                    ha='center', va='bottom', fontsize=8, color='black'
                )

        bottom = bottom + Cost_Gross_Plot[:, index]  # 更新 bottom 以堆叠柱子
    plt.title("每日支出细则")
    plt.xlabel("日期")
    plt.ylabel("花费金额")
    plt.yscale('log')
    # **扩展 x 轴范围，避免 1-1 被截断**
    plt.xlim(min(Date_Plot) - timedelta(days=0.5), max(Date_Plot) + timedelta(days=0.5))
    plt.ylim(1e-2, 1e5)
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interval))  # 1天一个刻度;
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))  # 只显示月-日
    plt.xticks(rotation=90, fontsize=8)
    # 添加网格线
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend()
    # plt.show()
    first = min(Date_Plot).date()
    end = max(Date_Plot).date()
    Pic_Path = Pic_Dir + f"/Cost_Detials_{first}_{end}.jpg"
    plt.savefig(Pic_Path, dpi=500)
    plt.close()
    
# 绘制传入时间内各种支出的占比
def Plot_Cost_Pie_Chart(Date, Cost_Gross, Cost_Type, Pic_Dir):
    Date_Plot = pd.to_datetime(Date)
    Cost_Gross_Plot = -1 * np.sum(Cost_Gross[:, 2:], axis=0)
    Cost_Type_Plot = Cost_Type[2:]
    plt.figure(figsize=(10, 8))
    # 绘制饼图，Cost_Gross_Plot 为每部分的大小，Cost_Type_Plot 为每部分的标签
    plt.pie(Cost_Gross_Plot, labels=Cost_Type_Plot, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.axis('equal') # 保证饼图是圆的
    plt.title("各种花销比例")
    plt.legend()
    # 调整饼图与表格的相对位置
    plt.subplots_adjust(bottom=0.35)  # 留出更多空间给表格
    # 创建表格
    total_cost = np.sum(Cost_Gross_Plot)
    cost_percent = (Cost_Gross_Plot / total_cost) * 100
    # 获取最后一个日期和第一个日期
    first_date = Date_Plot[0]
    last_date = Date_Plot[-1]
    # 计算年份和月份差异
    delta_days = (last_date - first_date).days
    month_diff = delta_days/30.0
    average_monthly = Cost_Gross_Plot / month_diff 
    print(f"[Count_Head::Plot_Cost_Pie_Chart] There are {delta_days + 1} days.")
    table_data = []
    for i, label in enumerate(Cost_Type_Plot):
        table_data.append([label, f'{Cost_Gross_Plot[i]:.2f}', f'{cost_percent[i]:.2f}%', f'{average_monthly[i]:.2f}'])
    # 计算小结
    total_cost_str = f'{total_cost:.2f}'
    cost_percent_total = f'{100.0:.2f}%'  # 小结占比为100%
    average_monthly_total = f'{np.sum(average_monthly):.2f}'  # 总体平均每月支出
    # 添加小结行
    table_data.append(['小结', total_cost_str, cost_percent_total, average_monthly_total])
    # 设置表格的列名
    col_labels = ['支出类别', '总金额', '占比(%)', '平均每月支出']
    # 在饼图下面添加表格
    table = plt.table(cellText=table_data, colLabels=col_labels, loc='bottom', cellLoc='center', bbox=[0.1, -0.5, 0.8, 0.4])
    # 微调数字位置，让数字距离上边界更远一些
    for key, cell in table.get_celld().items():
        cell.set_text_props(verticalalignment='center')  # 设置文本垂直对齐方式
        cell.set_fontsize(10)  # 可调整字体大小，避免拥挤
    # plt.show()
    first = min(Date_Plot).date()
    end = max(Date_Plot).date()
    Pic_Path = Pic_Dir + f"/Cost_Pie_Chart_{first}_{end}.jpg"
    plt.savefig(Pic_Path, dpi=500)
    plt.close()

# 绘制前100项花销
def Plot_Cost_First_100(Start_Date, End_Date, CSV_Path, Pic_Dir):
    data = pd.read_csv(CSV_Path, encoding='utf-8')
    Cost_Type = data[data["Property"] == -1]["Type"].unique()
    Income_Type = data[data["Property"] == 1]["Type"].unique()
    if Start_Date != "0" and End_Date != "0":
            data = data[(data["Date"] >= Start_Date) & (data["Date"] <= End_Date)]
    data = data[data["Property"] == -1]
    column_labels = ['No.','日期','类别','金额','注释']
    # 所有详细花销
    temp_data = data.reset_index(drop=True)
    temp_data = temp_data.nsmallest(100, "Quantity")
    table_data = []
    index = 1
    for _, row in temp_data.iterrows():
        table_data.append([
            index,
            row["Date"],
            row["Type"],
            row["Quantity"],
            row["Comment"]
        ])
        index = index + 1
    # Plot
    fig, ax = plt.subplots(figsize=(5, 20))
    ax.set_axis_off()
    table = ax.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width([0, 1, 2, 3, 4])
    # plt.show()
    pic_path = Pic_Dir + f"/Total_Cost_{Start_Date}_{End_Date}.jpg"
    plt.savefig(pic_path, dpi=500)
    plt.close()
    # 每类详细花销
    for cost_type in Cost_Type:
        temp_data = data[data["Type"] == cost_type]
        temp_data = temp_data.reset_index(drop=True)
        temp_data = temp_data.nsmallest(100, "Quantity")
        table_data = []
        index = 1
        for _, row in temp_data.iterrows():
            table_data.append([
                index, 
                row["Date"],
                row["Type"],
                row["Quantity"],
                row["Comment"]
            ])
            index = index + 1
        # Plot
        if(len(table_data) != 0):
            fig, ax = plt.subplots(figsize=(5, 20))
            ax.set_axis_off()
            table = ax.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.auto_set_column_width([0, 1, 2, 3, 4])
            # plt.show()
            pic_path = Pic_Dir + f"/{cost_type}_{Start_Date}_{End_Date}.jpg"
            plt.savefig(pic_path, dpi=500)
            plt.close()
        else:
            continue

# 根据传入时间，自动计算画图
def Analysis(Start_Date, End_Date, CSV_Path, Pic_Dir, Interval=1):
    Date, Cost_Gross, Income_Gross, Cost_Type, Income_Type = Compute_Date(Start_Date, End_Date, CSV_Path)
    Plot_Everyday(Date, Cost_Gross, Income_Gross, Pic_Dir, Interval)
    Plot_Cost_Details(Date, Cost_Gross, Cost_Type, Pic_Dir, Interval)
    Plot_Cost_Pie_Chart(Date, Cost_Gross, Cost_Type, Pic_Dir)
    Plot_Cost_First_100(Start_Date, End_Date, CSV_Path, Pic_Dir)

def Analysis_Monthly(CSV_Path, Pic_Dir, Interval=1):
    data = pd.read_csv(CSV_Path, encoding='utf-8')
    data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
    # 提取每个月的起始日期和结束日期
    data["Month"] = data["Date"].dt.to_period("M")  # 提取每个月
    # 使用字典来存储每个月的起止日期
    monthly_range = data.groupby("Month")["Date"].agg(["min", "max"])
    # 创建两个列表来分别存储每个月的起始和结束日期
    start_dates = []
    end_dates = []
    # 遍历并将结果添加到列表
    for month, row in monthly_range.iterrows():
        start_dates.append(row["min"].strftime("%Y-%m-%d"))
        end_dates.append(row["max"].strftime("%Y-%m-%d"))
    # Process Monthly
    for index in range(len(start_dates)):
        Start_Date = start_dates[index]
        End_Date = end_dates[index]
        Analysis(Start_Date, End_Date, CSV_Path, Pic_Dir, Interval=1)

# 分析所有数据
def Analysis_All(CSV_Path, Pic_Dir):
    data = pd.read_csv(CSV_Path, encoding='utf-8')
    data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
    # 创建两个列表来分别存储每个月的起始和结束日期
    Date = data["Date"].unique()
    length = len(Date)
    Start_Date = Date[0].strftime("%Y-%m-%d")
    End_Date = Date[length - 1].strftime("%Y-%m-%d")
    Interval = int(1.0 * length / 30.0) + 1
    Analysis(Start_Date, End_Date, CSV_Path, Pic_Dir, Interval=Interval)