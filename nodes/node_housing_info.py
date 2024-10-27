# -*- coding: utf-8 -*-

import pandas as pd
import json
from io import StringIO

class BK_HousingInfo:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "pipeline": ("CSV",), 
                "小区名称": ("STRING",{"default": "滨运锦绣里",}),
                "房屋总价": ("INT", {"default": 4200000, "min": 0, "max": 99999999999}),
                "室": ("INT", {"default": 3, "min": 0, "max": 20}),
                "厅": ("INT", {"default": 2, "min": 0, "max": 10}),
                "卫": ("INT", {"default": 2, "min": 0, "max": 10}),
                "建筑面积": ("FLOAT", {"default": 110.0, "min": 0, "max": 1000, "step": 0.01}),
                "得房率": ("INT", {"default": 91, "min": 0, "max": 200, "step": 1}),
                "当前楼层": ("INT", {"default": 16, "min": 0, "max": 100}),
                "总楼层": ("INT", {"default": 17, "min": 0, "max": 100}),
                "装修标准": ("INT", {"default": 4000, "min": 0, "max": 99999999999}),
                "房屋权属": (["商品房","公房","经济适用房","其他",],{"default": "商品房"}),
                "楼房类型": (["塔楼", "板楼", "高层", "小高层", "超高层"],{"default": "塔楼"}),
                "房屋用途": (["普通住宅","商业类","别墅","四合院","车位","其他",],{"default": "普通住宅"}),
                "房屋类型": (["新房","二手房"],{"default": "新房"}),
                "装修": (["精装修","无"],{"default": "精装修"}),
                "交房时间": ("STRING",{"default": "2024-11",}),
                "物业费": ("FLOAT", {"default": 5.5, "min": 0, "max": 100, "step": 0.01}),
                "容积率": ("FLOAT", {"default": 2.2, "min": 0, "max": 100, "step": 0.01}),
                "总户数": ("INT", {"default": 1500, "min": 0, "max": 5000}),
            }
        }

    RETURN_TYPES = ("CSV", )
    RETURN_NAMES = ("CSV", )
    FUNCTION = "exec"
    OUTPUT_NODE = True
    CATEGORY = "⭐️ Baikong"
    DESCRIPTION = "目标房产的基础信息"

    def exec(self, pipeline=None, 房屋总价=None, 室=None, 厅=None, 卫=None, 建筑面积=None, 
             小区名称=None, 得房率=None, 当前楼层=None, 总楼层=None, 装修标准=None, 房屋用途=None, 
             房屋权属=None, 楼房类型=None, 房屋类型=None, 装修=None, 交房时间=None, 物业费=None,
             容积率=None, 总户数=None):
        
        data = {
            "小区名称": 小区名称 or "-",
            "房屋总价": f"{房屋总价/10000:.2f}万元",
            "房型": f"{室}室{厅}厅{卫}卫",
            "建筑面积": f"{建筑面积:.2f}m²",
            "得房率": f"{得房率}%" or "-",
            "套内面积": f"{建筑面积*得房率/100:.2f}m²" or "-",
            "楼层": f"{当前楼层}/{总楼层}" or "-",
            "装修标准": f"{装修标准}元/m²" or "-",
            "交房时间": 交房时间 or "-",
            "物业费(月)": f"{物业费}元/m²" or "-",
            "物业费(年)": f"{物业费*建筑面积*12:.2f}元" or "-",
            "房屋用途": 房屋用途 or "-",
            "楼房类型": 楼房类型 or "-",
            "房屋类型": 房屋类型 or "-",
            "装修": 装修 or "-",
            "容积率": 容积率 or "-",
            "总户数": 总户数 or "-"
        }
        
        current_df = pd.DataFrame([data])
        
        if pipeline is not None:
            pipeline_df = pd.read_csv(StringIO(pipeline))
            combined_df = pd.concat([pipeline_df, current_df], ignore_index=True)
        else:
            combined_df = current_df

        result = combined_df.to_csv(index=False, encoding='utf-8')

        print(f"[BK_District_Info] ○ INPUT {小区名称}-{室}室{厅}厅{卫}卫")
        
        return (result,)
