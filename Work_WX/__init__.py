import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from io import StringIO

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 示例数据（3行数据）
text_data = """
姓名,年龄,城市,评分,部门
Alice,30,纽约,85,技术部
Bob,25,洛杉矶,92,市场部
Charlie,35,芝加哥,78,财务部
"""
df = pd.read_csv(StringIO(text_data.strip()))
print(df)
rows = len(df) + 1  # 3数据行 + 1表头 = 4行
print(rows)
cols = len(df.columns)
print(cols)
print("DataFrame 行数:", len(df))
print("DataFrame 列数:", len(df.columns))
# 动态计算图表尺寸
fig = plt.figure(figsize=(cols * 1.8, rows * 0.6))
ax = plt.gca()
ax.axis('off')

# --------------------------
# 生成颜色矩阵
# --------------------------
header_color = '#2E86C1'
row_colors = ['#EBF5FB', '#FFFFFF']
cell_colors = [[header_color] * cols]  # 表头行


for i in range(len(df)):
    color = row_colors[i % 2]
    cell_colors.append([color] * cols)  # 数据行

# 对评分列应用渐变色
score_col_idx = df.columns.get_loc("评分")  # 动态获取列索引
score_values = df['评分'].values.astype(float)
cmap = LinearSegmentedColormap.from_list('score_cmap', ['#2ECC71', '#F1C40F', '#E74C3C'], N=256)
norm = plt.Normalize(score_values.min(), score_values.max())

for idx, score in enumerate(score_values):
    rgba = cmap(norm(score))
    cell_colors[idx + 1][score_col_idx] = rgba  # 修改对应单元格颜色

# --------------------------
# 绘制表格
# --------------------------
table = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    cellColours=cell_colors,  # 确保行数=rows=4
    loc='center',
    cellLoc='center',
    edges='BRLT'
)

# 调整样式
table.auto_set_font_size(False)
table.set_fontsize(12)
for cell in table.get_celld().values():
    cell.set_text_props(color='#2C3E50')

# 保存图片
plt.savefig('fixed_table.png', bbox_inches='tight', dpi=300)
plt.close()