# -*- coding: utf-8 -*-

import pandas as pd
import json

class BK_District_Info:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "小区名称": ("STRING",{"default": "滨运锦绣里",}),
                "房屋总价": ("INT", {"default": 4000000, "min": 0, "max": 99999999999}),
                "室": ("INT", {"default": 3, "min": 0, "max": 20}),
                "厅": ("INT", {"default": 2, "min": 0, "max": 10}),
                "卫": ("INT", {"default": 2, "min": 0, "max": 10}),
                "建筑面积": ("FLOAT", {"default": 100.0, "min": 0, "max": 1000, "step": 0.01}),
                "得房率": ("INT", {"default": 80, "min": 0, "max": 200, "step": 1}),
                "当前楼层": ("INT", {"default": 4, "min": 0, "max": 100}),
                "总楼层": ("INT", {"default": 8, "min": 0, "max": 100}),
                "房屋权属": (["商品房","公房","经济适用房","其他",],{"default": "商品房"}),
                "楼房类型": (["塔楼", "板楼", "高层", "小高层", "超高层"],{"default": "塔楼"}),
                "房屋用途": (["普通住宅","商业类","别墅","四合院","车位","其他",],{"default": "普通住宅"}),
                "房屋类型": (["新房","二手房"],{"default": "新房"}),
                "装修": (["精装修","无"],{"default": "精装修"}),
                "交房时间": ("STRING",{"default": "2024-11",}),
                "物业费": ("FLOAT", {"default": 3.0, "min": 0, "max": 100, "step": 0.01}),
            }
        }
    RETURN_TYPES = ("CSV", )
    RETURN_NAMES = ("CSV", )
    FUNCTION = "exec"
    OUTPUT_NODE = True
    CATEGORY = "⭐️ Baikong"
    DESCRIPTION = "预览 Excel"

    def exec(self, 房屋总价, 室, 厅, 卫, 建筑面积, 小区名称=None, 得房率=None, 
             当前楼层=None, 总楼层=None, 房屋用途=None, 房屋权属=None, 楼房类型=None, 
             房屋类型=None, 装修=None, 交房时间=None, 物业费=None):
        
        # 创建一个字典来存储输入数据
        data = {
            "小区名称": 小区名称 or "-",
            "房屋总价": f"{房屋总价/10000:.2f}万元",
            "房型": f"{室}室{厅}厅{卫}卫",
            "建筑面积": f"{建筑面积}m²",
            "得房率": f"{得房率}%" or "-",
            "套内面积": f"{建筑面积*得房率/100:.2f}m²" or "-",
            "楼层": f"{当前楼层}/{总楼层}" or "-",
            "交房时间": 交房时间 or "-",
            "物业费(月)": f"{物业费}元/m²" or "-",
            "物业费(年)": f"{物业费*建筑面积*12:.2f}元" or "-",
            "房屋用途": 房屋用途 or "-",
            "楼房类型": 楼房类型 or "-",
            "房屋类型": 房屋类型 or "-",
            "装修": 装修 or "-"
        }
        
        # 将数据转换为 DataFrame
        df = pd.DataFrame([data])

        result =  df.to_csv(index=False, encoding='utf-8')

        print(f"[BK_District_Info] ○ INPUT {result}")
        
        # 返回 DataFrame 作为 CSV 格式
        return (result,)