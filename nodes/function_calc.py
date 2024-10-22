import matplotlib
matplotlib.use('Agg')

import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import io
from matplotlib.font_manager import FontProperties
import os

def 计算月供(贷款额, 年利率, 贷款月数):
    月利率 = 年利率 / 12
    if 贷款额 > 0:
        return (贷款额 * 月利率 * (1 + 月利率) ** 贷款月数) / ((1 + 月利率) ** 贷款月数 - 1)
    return 0

def 计算总月供(公积金贷款额, 商业贷款额, 公积金年利率, 商业年利率, 贷款月数):
    公积金月供 = 计算月供(公积金贷款额, 公积金年利率, 贷款月数)
    商业月供 = 计算月供(商业贷款额, 商业年利率, 贷款月数)
    return 公积金月供 + 商业月供

def 绘制趋势图(ax, df, 工作年限, 交房时间, 是否卖出房产, 卖出时间, font_prop):
    ax.plot(df['月份'], df['资金池'], label='购房资金池')
    ax.plot(df['月份'], df['无购房资金池'], label='无购房资金池')
    ax.plot(df['月份'], df['房贷余额'], label='房贷余额')
    ax.axvline(x=工作年限*12, color='r', linestyle='--', label='失业时点')
    ax.axvline(x=交房时间, color='g', linestyle='--', label='交房时点')
    if 是否卖出房产:
        ax.axvline(x=交房时间+卖出时间, color='m', linestyle='--', label='卖房时点')
    ax.legend(prop=font_prop)
    ax.grid(True)

def 合并资金池和月度收支图(df, 房价, 首付, 房贷年限, 工作年限, 交房时间, 是否卖出房产, 卖出时间):
    sns.set(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)

    # 获取字体文件路径
    font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")
    file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
    font_path = os.path.join(font_dir, file_list[0])  # 假设只有一个字体文件
    font_prop = FontProperties(fname=font_path)

    # 添加新的列用于存储计算结果
    df['月结余_不含大额变动_调整'] = df['月结余_不含大额变动'] - df['年终奖']

    # 绘制趋势图
    sns.lineplot(x='月份', y='资金池', data=df, ax=ax1, label='购房资金池')
    sns.lineplot(x='月份', y='无购房资金池', data=df, ax=ax1, label='无购房资金池')
    sns.lineplot(x='月份', y='房贷余额', data=df, ax=ax1, label='房贷余额')
    ax1.axvline(x=工作年限*12, color='r', linestyle='--', label='失业时点')
    ax1.axvline(x=交房时间, color='g', linestyle='--', label='交房时点')
    if 是否卖出房产:
        ax1.axvline(x=交房时间+卖出时间, color='m', linestyle='--', label='卖房时点')
    ax1.set_title(f'购入 {房价/10000} 万元房产, 首付 {首付/10000} 万元, 贷款 {房贷年限} 年 vs 不购房', fontproperties=font_prop)
    ax1.set_ylabel('金额 (元)', fontproperties=font_prop)
    ax1.legend(prop=font_prop)

    # 绘制月度收支平衡图
    sns.lineplot(x='月份', y='月收入总额', data=df, ax=ax2, label='月收入总额 (不含奖金)')
    sns.lineplot(x='月份', y='月支出总额', data=df, ax=ax2, label='月支出总额')
    sns.lineplot(x='月份', y='月结余_不含大额变动_调整', data=df, ax=ax2, label='月结余 (不含大额变动和奖金)')
    ax2.axvline(x=工作年限*12, color='r', linestyle='--', label='失业时点')
    ax2.axvline(x=交房时间, color='g', linestyle='--', label='交房时点')
    if 是否卖出房产:
        ax2.axvline(x=交房时间+卖出时间, color='m', linestyle='--', label='卖房时点')
    ax2.set_title('月度收入与支出平衡 (不含奖金)', fontproperties=font_prop)
    ax2.set_xlabel('月份', fontproperties=font_prop)
    ax2.set_ylabel('金额 (元)', fontproperties=font_prop)
    ax2.legend(prop=font_prop)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)
    plt.close(fig)  # 关闭图形以释放资源
    return img
