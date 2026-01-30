# -*- coding: utf-8 -*-
"""
简化的燃油追踪器 - 修复版本
"""

import json
import os
from datetime import datetime
from typing import List, Dict


class FuelTrackerSimple:
    def __init__(self, data_file: str = "fuel_records_simple.json"):
        self.data_file = data_file
        self.records: List[Dict] = []
        self.load_data()

    def load_data(self):
        """从文件加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.records = data
                    else:
                        self.records = []
            except Exception as e:
                print(f"加载数据失败: {e}")
                self.records = []
        else:
            self.records = []

    def save_data(self):
        """保存数据到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False

    def add_record(self, date: str, odometer: float, fuel_amount: float, fuel_price: float, station: str = "", note: str = ""):
        """添加加油记录"""
        try:
            cost = fuel_amount * fuel_price
            record = {
                "date": date,
                "odometer": float(odometer),
                "fuel_amount": float(fuel_amount),
                "fuel_price": float(fuel_price),
                "station": station,
                "note": note,
                "cost": round(cost, 2)
            }
            self.records.append(record)
            self.records.sort(key=lambda x: x["date"])  # 按日期排序
            success = self.save_data()
            if success:
                return record
            else:
                return None
        except ValueError as e:
            print(f"输入值错误: {e}")
            return None
        except Exception as e:
            print(f"添加记录失败: {e}")
            return None

    def calculate_fuel_efficiency(self) -> List[Dict]:
        """计算每次加油的油耗"""
        try:
            results = []
            if len(self.records) < 2:
                return results
                
            sorted_records = sorted(self.records, key=lambda x: x["odometer"])

            for i in range(1, len(sorted_records)):
                prev_record = sorted_records[i-1]
                curr_record = sorted_records[i]

                distance = curr_record["odometer"] - prev_record["odometer"]
                fuel_used = curr_record["fuel_amount"]

                if distance > 0 and fuel_used > 0:
                    efficiency = distance / fuel_used  # km/L
                    consumption = (fuel_used / distance) * 100  # L/100km

                    results.append({
                        "date": curr_record["date"],
                        "distance": round(distance, 2),
                        "fuel_used": round(fuel_used, 2),
                        "efficiency_km_per_l": round(efficiency, 2),
                        "consumption_l_per_100km": round(consumption, 2),
                        "from_odometer": prev_record["odometer"],
                        "to_odometer": curr_record["odometer"]
                    })

            return results
        except Exception as e:
            print(f"计算油耗时出错: {e}")
            return []

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        try:
            if not self.records:
                return {
                    "total_records": 0,
                    "total_cost": 0,
                    "total_fuel": 0,
                    "average_price": 0,
                    "total_distance": 0,
                    "average_consumption": 0,
                    "first_date": None,
                    "last_date": None
                }

            total_cost = sum(record["cost"] for record in self.records)
            total_fuel = sum(record["fuel_amount"] for record in self.records)
            avg_price = total_cost / total_fuel if total_fuel > 0 else 0

            # 获取里程范围
            sorted_records = sorted(self.records, key=lambda x: x["odometer"])
            total_distance = 0
            if len(sorted_records) > 1:
                total_distance = sorted_records[-1]["odometer"] - sorted_records[0]["odometer"]

            # 计算平均油耗
            efficiencies = self.calculate_fuel_efficiency()
            avg_consumption = 0
            if efficiencies:
                avg_consumption = sum(item["consumption_l_per_100km"] for item in efficiencies) / len(efficiencies)

            return {
                "total_records": len(self.records),
                "total_cost": round(total_cost, 2),
                "total_fuel": round(total_fuel, 2),
                "average_price": round(avg_price, 2),
                "total_distance": round(total_distance, 2),
                "average_consumption": round(avg_consumption, 2) if avg_consumption > 0 else 0,
                "first_date": sorted_records[0]["date"] if sorted_records else None,
                "last_date": sorted_records[-1]["date"] if sorted_records else None
            }
        except Exception as e:
            print(f"获取统计数据时出错: {e}")
            return {
                "total_records": 0,
                "total_cost": 0,
                "total_fuel": 0,
                "average_price": 0,
                "total_distance": 0,
                "average_consumption": 0,
                "first_date": None,
                "last_date": None
            }

    def get_records(self) -> List[Dict]:
        """获取所有记录"""
        return self.records