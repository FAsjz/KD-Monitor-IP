import matplotlib.pyplot as plt
import pandas as pd

# pic_path = r'\\Hrd-sh\ftpserver\Anonymous_Access\share_pic\table_image.png'
pic_path = r'D:\monitor_ips\table_image.png'

def make_pic(df):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows 系统常用
    plt.rcParams['axes.unicode_minus'] = False
    # 创建图像并绘制表格
    fig, ax = plt.subplots(figsize=(5, 3))  # 调整图像尺寸
    ax.axis('off')  # 隐藏坐标轴
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc='center',
        cellLoc='center',
        colColours=['#f0f0f0'] * len(df.columns)  # 设置列标题背景色
    )

    # 调整表格样式
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)  # 调整单元格宽高

    # 保存为图片
    plt.savefig(pic_path, bbox_inches='tight', dpi=300)
    plt.close()
    print('图片已生成')
    return pic_path


# df1 = pd.DataFrame({
#     'name':['Xiaoming','Xiaohong','Xiaojun'],
#     'age':[18,35,45],
#     'occupation':['student','teacher','doctor']
# })
#
# make_pic(df1)