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

class BK_Table_Preview:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "csv1": ("CSV",),
                "csv2": ("CSV",),
                "csv3": ("CSV",),
                "csv4": ("CSV",),
                "csv5": ("CSV",),
                "csv6": ("CSV",),
                "csv7": ("CSV",),
                "csv8": ("CSV",),
                "csv9": ("CSV",),
                "csv10": ("CSV",),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("CSV", "STRING", "STRING", "IMAGE")  # 增加 IMAGE 类型
    RETURN_NAMES = ("CSV", "JSON", "CSV_VALUE", "TABLE_IMAGE")  # 增加对应的名称
    FUNCTION = "exec"
    OUTPUT_NODE = True
    CATEGORY = "⭐️ Baikong"
    DESCRIPTION = "预览 Excel"

    def json_to_table(self, json_data):

        # 将 JSON 数据转换为 DataFrame
        df = pd.json_normalize(json_data)

        # 填充缺失值为 "-"
        df.fillna("-", inplace=True)

        return df

    def create_table_image(self, df):
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, len(df) * 0.5))  # 根据数据行数调整图片大小
        ax.axis('tight')
        ax.axis('off')

        # 获取字体文件路径
        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
        font_path = os.path.join(font_dir, file_list[0])  # 假设只有一个字体文件
        font_prop = FontProperties(fname=font_path)
        
        # 创建表格
        table = ax.table(cellText=df.values,
                        colLabels=df.columns,
                        cellLoc='center',
                        loc='center')
        
        # 调整表格样式
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.5)

        # 设置中文字体
        for cell in table._cells.values():
            cell.get_text().set_fontproperties(font_prop)

        # 将图表转换为图片
        canvas = FigureCanvas(fig)
        canvas.draw()
        
        # 将 canvas 转换为 PIL Image
        s, (width, height) = canvas.print_to_buffer()
        image = Image.frombytes("RGBA", (width, height), s)
        
        # 转换为 RGB 模式
        image = image.convert('RGB')
        
        # 关闭 matplotlib 图表以释放内存
        plt.close(fig)
        
        return image

    def exec(self, csv1=None, csv2=None, csv3=None, csv4=None,
             csv5=None, csv6=None, csv7=None, csv8=None, csv9=None, csv10=None,
             unique_id=None, extra_pnginfo=None):
        if unique_id is not None and extra_pnginfo is not None:
            # 将所有 CSV 输入放入列表
            csv_inputs = [csv1, csv2, csv3, csv4,
                          csv5, csv6, csv7, csv8, csv9, csv10]

            # 初始化一个空的 DataFrame 列表
            dataframes = []

            for csv in csv_inputs:
                if csv:  # 确保 csv 不为空
                    # 使用 pandas 读取 CSV 数据
                    df = pd.read_csv(StringIO(csv))
                    # 将 DataFrame 添加到列表中
                    dataframes.append(df)

            # 合并所有 DataFrame，使用外连接以保留所有字段
            combined_table = pd.concat(
                dataframes, axis=0, join='outer', ignore_index=True)

            # 填充缺失值为 "-"
            combined_table.fillna("-", inplace=True)

            # 将合并后的表格转换为 JSON 格式
            json_output = combined_table.to_json(
                orient='records', force_ascii=False)

            # 将 DataFrame 转换为 CSV 字符串
            csv_output = combined_table.to_csv(index=False)

            # 创建表格图片
            table_image = self.create_table_image(combined_table)
            # 转换为 tensor
            table_tensor = pil2tensor(table_image)

            print(f"[BK_Table_Preview] ○ OUTPUT {combined_table}")
            print(f"[BK_Table_Preview] ○ OUTPUT {json_output}")

        return {
            # "ui": {"text": json_output},
            "result": (combined_table, 
                      json.dumps(json.loads(json_output),
                               ensure_ascii=False,  # 保持中文不转换为 unicode
                               indent=2),  # 使用2空格缩进格式化
                      csv_output,  # CSV 字符串输出
                      table_tensor)  # 表格图片输出
        }
