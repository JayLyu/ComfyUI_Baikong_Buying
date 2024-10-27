# -*- coding: utf-8 -*-

import torch
import pandas as pd
import numpy as np
from PIL import Image
import json
from io import StringIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.font_manager import FontProperties
import os

# Tensor to PIL


def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# Convert PIL to Tensor


def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


class BK_HousingCalc:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "csv": ("CSV",),
            },
            "optional": {
                "sort_by": ("STRING", {
                    "default": "房屋总价,得房率",
                    "multiline": False,
                }),
                "sort_direction": (["正序", "倒序"], {"default": "正序"}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "IMAGE")
    RETURN_NAMES = ("JSON", "CSV", "IMAGE")
    FUNCTION = "exec"
    OUTPUT_NODE = True
    CATEGORY = "⭐️ Baikong"
    DESCRIPTION = "使用表格预览数据，并输出csv、json两种格式的结果"

    def json_to_table(self, json_data):

        # 将 JSON 数据转换为 DataFrame
        df = pd.json_normalize(json_data)

        # 填充缺失值为 "-"
        df.fillna("-", inplace=True)

        return df

    def create_table_image(self, df):
        # 设置更高的 DPI 值来提高清晰度
        plt.rcParams['figure.dpi'] = 200

        # 调整高度计算方式，减小系数
        rows = len(df) + 1  # +1 是为了包含表头
        fig, ax = plt.subplots(
            figsize=(15, max(4, rows * 0.25)), dpi=200)
        ax.axis('tight')
        ax.axis('off')

        # 获取字体文件路径
        font_dir = os.path.join(os.path.dirname(
            os.path.dirname(os.path.realpath(__file__))), "fonts")
        font_path = os.path.join(font_dir, "AlibabaPuHuiTi-3-45-Light.ttf")
        font_prop = FontProperties(fname=font_path)

        # 创建表格时应用字体
        table = ax.table(cellText=df.values,
                         colLabels=df.columns,
                         cellLoc='center',
                         loc='center')

        # 调整表格样式并应用字体
        table.auto_set_font_size(False)
        table.set_fontsize(9)

        # 为每个单元格设置字体
        for cell in table._cells.values():
            cell.set_text_props(fontproperties=font_prop)
            cell.set_edgecolor('black')
            cell.set_linewidth(0.5)

        # 自动调整布局以确保表格完全显示
        plt.tight_layout()

        # 将图表转换为图片时保持高 DPI
        canvas = FigureCanvas(fig)
        canvas.draw()

        # 获取更高分辨率的图像数据
        s, (width, height) = canvas.print_to_buffer()
        image = Image.frombytes("RGBA", (width, height), s)
        image = image.convert('RGB')
        plt.close(fig)

        return image

    def exec(self, csv, sort_by="", sort_direction="正序", unique_id=None, extra_pnginfo=None):
        if unique_id is not None and extra_pnginfo is not None:
            df = pd.read_csv(StringIO(csv))

            # 填充缺失值为 "-"
            df.fillna("-", inplace=True)

            # 处理排序
            if sort_by.strip():
                # 将排序字段拆分为列表
                sort_columns = [col.strip() for col in sort_by.split(',')]
                # 验证所有排序列是否存在
                valid_columns = [
                    col for col in sort_columns if col in df.columns]

                if valid_columns:
                    # 根据选择的方向确定升序还是降序
                    ascending = True if sort_direction == "正序" else False
                    # 如果是多列排序，创建相同长度的 ascending 列表
                    if len(valid_columns) > 1:
                        ascending = [ascending] * len(valid_columns)

                    df = df.sort_values(by=valid_columns, ascending=ascending)
                    print(f"[BK_Table_Preview] ○ Sorted by {valid_columns} in {sort_direction} order")
                else:
                    print(
                        f"[BK_Table_Preview] ⚠️ Warning: No valid column names found in {sort_by}")

            # 将表格转换为 JSON 格式
            json_output = df.to_json(
                orient='records', force_ascii=False)

            # 将 DataFrame 转换为 CSV 字符串
            csv_output = df.to_csv(index=False)

            # 创建表格图片
            table_image = self.create_table_image(df)
            # 转换为 tensor
            table_tensor = pil2tensor(table_image)

            # print(f"[BK_Table_Preview] ○ INPUT {df}")

        return (json.dumps(json.loads(json_output),
                           ensure_ascii=False,
                           indent=2),
                csv_output,
                table_tensor)
