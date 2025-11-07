import os  # 导入os模块，用于操作文件和目录
import pandas as pd  # 导入pandas模块，用于数据分析和处理
import phydrus as ps  # 导入phydrus模块，用于模拟土壤水分运动
import matplotlib.pyplot as plt  # 导入matplotlib.pyplot模块，用于绘图
import numpy as np  # 导入numpy模块，用于数值计算

# 1. 设置工作空间和可执行文件路径
ws = "2022&2023"
exe = "Hydrus1D/hydrus" #Please re-enter the address where you saved the Hydrus1D folder.

# 2. 描述模型
desc = "Root uptake with meteorological data"

# 3. 创建模型对象，设置模型名称、描述、单位等
ml = ps.Model(exe_name=exe, ws_name=ws, name="model", description=desc,
              mass_units="mmol", time_unit="days", length_unit="cm")

# 4. 添加时间信息，设置模拟时间范围和是否打印时间信息
times = ml.add_time_info(tinit=0, tmax=730, print_times=True)

# 5. 添加水流信息，设置边界条件、根系参数、地下水位等
ml.add_waterflow(linitw=False, top_bc=3, bot_bc=2, rroot=0)

# 6. 创建土壤材料属性数据框
m = ml.get_empty_material_df(n=4)  # 创建材料属性数据框
m.loc[1:4] = [[0.0364, 0.3766, 0.01396, 1.562, 145.8, 0.05],
              [0.045, 0.3635, 0.010299, 1.334, 160.3, 0.05],
              [0.0513, 0.4051, 0.004948, 1.308, 37.638, 0.05],
              [0.0449, 0.3477, 0.00894, 1.521, 67.44, 0.05]]  # soil parameters

ml.add_material(m)  # 添加材料属性数据到模型

# 7. 创建土壤剖面，设置剖面深度、层厚、初始水头、材料编号等
profile = ps.create_profile(bot=[-140, -200, -440, -600], dx=1,
                            h=-60, mat=m.index)
ml.add_profile(profile)  # 添加土壤剖面到模型
ml.profile["h"] = pd.read_csv("/Users/liuyang/Downloads/phydrus/2022&2023/data/h.csv", header=None) #Please re-enter the address where you are running this program.

# 8. 读取大气边界条件
atm = pd.read_csv("/Users/liuyang/Downloads/phydrus/2022&2023/data/2022&2023.csv", index_col=0) #Please re-enter the address where you are running this program.
ml.add_atmospheric_bc(atm)  # 添加大气边界条件数据到模型
ml.atmosphere["hB"] = pd.read_csv("/Users/liuyang/Downloads/phydrus/2022&2023/data/gwl.csv", index_col=0) #Please re-enter the address where you are running this program.

# 9. 添加观测节点
ml.add_obs_nodes([-10, -30, -50, -90, -150, -250, -350, -450, -550])

# 10. 读取根系吸水参数
ml.profile["Beta"] = pd.read_csv("/Users/liuyang/Downloads/phydrus/2022&2023/data/beta.csv") #Please re-enter the address where you are running this program.

# 11. 添加根系吸水
ml.add_root_uptake(model=0, poptm=[-25, -25, -25, -25], crootmax=0.5, r2l=5.8e-4,
                   p0=-10, p2h=-200, p2l=-800, p3=-8000) #crootmax is omega; r2l is Kcomp

# 12. 写入输入文件并模拟
ml.write_input()
ml.simulate()

# 13. 读取、绘制水位信息
df = ml.read_tlevel()
df.plot(subplots=True)

# 14. 读取实测土壤含水量信息
swc = pd.read_csv("/Users/liuyang/Downloads/phydrus/2022&2023/data/swc.csv", sep=",") #Please re-enter the address where you are running this program.

# 15. 读取观测节点信息
df = ml.read_obs_node()

# 16. 绘制土壤含水量曲线
fig, axs = plt.subplots(3, 3, figsize=(12, 9), sharex=True, sharey=True)

axs[0, 0].plot(swc["tAtm"], swc["10 cm"], linestyle="", marker="o", markersize=3, color="red")
axs[0, 0].plot(df[ml.obs_nodes[0]]["theta"], color="black")
axs[0, 0].set_title("10 cm depth")
axs[0, 0].set_ylabel(r"$\theta$ [-]")

axs[0, 1].plot(swc["tAtm"], swc["30 cm"], linestyle="", marker="o", markersize=3, color="red")
axs[0, 1].plot(df[ml.obs_nodes[1]]["theta"], color="black")
axs[0, 1].set_title("30 cm depth")
axs[0, 1].set_ylabel(r"$\theta$ [-]")

axs[0, 2].plot(swc["tAtm"], swc["50 cm"], linestyle="", marker="o", markersize=3, color="red")
axs[0, 2].plot(df[ml.obs_nodes[2]]["theta"], color="black")
axs[0, 2].set_title("50 cm depth")
axs[0, 2].set_ylabel(r"$\theta$ [-]")

axs[1, 0].plot(swc["tAtm"], swc["90 cm"], linestyle="", marker="o", markersize=3, color="red")
axs[1, 0].plot(df[ml.obs_nodes[3]]["theta"], color="black")
axs[1, 0].set_title("90 cm depth")
axs[1, 0].set_ylabel(r"$\theta$ [-]")

axs[1, 1].plot(swc["tAtm"], swc["150 cm"], linestyle="", marker="o", markersize=3, color="red")
axs[1, 1].plot(df[ml.obs_nodes[4]]["theta"], color="black")
axs[1, 1].set_title("150 cm depth")
axs[1, 1].set_ylabel(r"$\theta$ [-]")

axs[1, 2].plot(swc["tAtm"], swc["250 cm"], linestyle="", marker="o", markersize=3, color="red")
axs[1, 2].plot(df[ml.obs_nodes[5]]["theta"], color="black")
axs[1, 2].set_title("250 cm depth")
axs[1, 2].set_ylabel(r"$\theta$ [-]")

axs[2, 0].plot(swc["tAtm"], swc["350 cm"], linestyle="", marker="o", markersize=3, color="red")
axs[2, 0].plot(df[ml.obs_nodes[6]]["theta"], color="black")
axs[2, 0].set_title("350 cm depth")
axs[2, 0].set_ylabel(r"$\theta$ [-]")

axs[2, 1].plot(swc["tAtm"], swc["450 cm"], linestyle="", marker="o", markersize=3, color="red")
axs[2, 1].plot(df[ml.obs_nodes[7]]["theta"], color="black")
axs[2, 1].set_title("450 cm depth")
axs[2, 1].set_ylabel(r"$\theta$ [-]")

axs[2, 2].plot(swc["tAtm"], swc["550 cm"], linestyle="", marker="o", markersize=3, color="red")
axs[2, 2].plot(df[ml.obs_nodes[8]]["theta"], color="black")
axs[2, 2].set_title("550 cm depth")
axs[2, 2].set_ylabel(r"$\theta$ [-]")

plt.show()

# 17. 将数据分类整理
df = ml.read_nod_inf()
merged_dfs = {}  # 创建一个字典来存储每个列的合并数据

# 循环遍历所有列（从第三列开始）
for col in df[90.0].columns[2:8]:  # 从第三列开始，即 "Head" 列
    # 创建一个空列表来存储所有 DataFrame 的指定列
    dfs = []
    # 遍历字典，将每个 DataFrame 的指定列添加到列表中
    for time, data in df.items():
        dfs.append(data[col])
    # 将所有 DataFrame 合并成一个新的 DataFrame
    merged_df = pd.concat(dfs, axis=1)
    # 设置列名
    merged_df.columns = [f"{col}_{time}" for time in df.keys()]
    # 将合并后的 DataFrame 保存到字典中
    merged_dfs[col] = merged_df

# 创建一个保存目录
output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

# 保存 DataFrame
for col, merged_df in merged_dfs.items():
    merged_df.to_csv(os.path.join(output_dir, f"{col}.csv"), index=False)

# 18. 数据处理
aa = pd.read_csv("/Users/liuyang/Downloads/phydrus/2022&2023/output/sink.csv") #Please re-enter the address where you are running this program.

# 计算前 40 行的总和
sum_sum = aa.iloc[:600].sum()
sum_1 = aa.iloc[:100].sum()
sum_2 = aa.iloc[101:600].sum()
sum_3 = aa.iloc[0:60].sum()
sum_4 = aa.iloc[60:200].sum()

# 创建一个新的 DataFrame 来存储结果
results_df = pd.DataFrame({
    'sum': sum_sum,
    '0-100': sum_1,
    '100-600':sum_2,
    '0-60': sum_3,
    '60-200': sum_4
})

# 导出为 CSV 文件
results_df.to_csv(f'{output_dir}/sum_sink.csv', index=False)
