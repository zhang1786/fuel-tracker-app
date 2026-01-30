#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
燃油追踪应用
用于记录加油情况和计算油耗
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class FuelRecord:
    def __init__(self, date: str, odometer: float, fuel_amount: float, fuel_price: float, station: str = "", note: str = ""):
        self.date = date
        self.odometer = odometer
        self.fuel_amount = fuel_amount
        self.fuel_price = fuel_price
        self.station = station
        self.note = note
        self.cost = fuel_amount * fuel_price

    def to_dict(self):
        return {
            "date": self.date,
            "odometer": self.odometer,
            "fuel_amount": self.fuel_amount,
            "fuel_price": self.fuel_price,
            "station": self.station,
            "note": self.note,
            "cost": self.cost
        }

    @classmethod
    def from_dict(cls, data):
        record = cls(data["date"], data["odometer"], data["fuel_amount"], data["fuel_price"], data["station"], data["note"])
        record.cost = data["cost"]
        return record


class FuelTrackerApp:
    def __init__(self, data_file: str = "fuel_records.json"):
        self.data_file = data_file
        self.records: List[FuelRecord] = []
        self.load_data()

    def load_data(self):
        """从文件加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.records = [FuelRecord.from_dict(record) for record in data]
            except Exception as e:
                print(f"加载数据失败: {e}")
                self.records = []

    def save_data(self):
        """保存数据到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([record.to_dict() for record in self.records], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")

    def add_record(self, date: str, odometer: float, fuel_amount: float, fuel_price: float, station: str = "", note: str = ""):
        """添加加油记录"""
        record = FuelRecord(date, odometer, fuel_amount, fuel_price, station, note)
        self.records.append(record)
        self.records.sort(key=lambda x: x.date)  # 按日期排序
        self.save_data()
        return record

    def calculate_fuel_efficiency(self) -> List[Dict]:
        """计算每次加油的油耗"""
        results = []
        sorted_records = sorted(self.records, key=lambda x: x.odometer)

        for i in range(1, len(sorted_records)):
            prev_record = sorted_records[i-1]
            curr_record = sorted_records[i]

            distance = curr_record.odometer - prev_record.odometer
            fuel_used = curr_record.fuel_amount

            if distance > 0 and fuel_used > 0:
                efficiency = distance / fuel_used  # km/L
                consumption = (fuel_used / distance) * 100  # L/100km

                results.append({
                    "date": curr_record.date,
                    "distance": distance,
                    "fuel_used": fuel_used,
                    "efficiency_km_per_l": round(efficiency, 2),
                    "consumption_l_per_100km": round(consumption, 2),
                    "from_odometer": prev_record.odometer,
                    "to_odometer": curr_record.odometer
                })

        return results

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        if not self.records:
            return {"total_records": 0}

        total_cost = sum(record.cost for record in self.records)
        total_fuel = sum(record.fuel_amount for record in self.records)
        avg_price = total_cost / total_fuel if total_fuel > 0 else 0

        # 获取里程范围
        sorted_records = sorted(self.records, key=lambda x: x.odometer)
        total_distance = sorted_records[-1].odometer - sorted_records[0].odometer if len(sorted_records) > 1 else 0

        # 计算平均油耗
        efficiencies = self.calculate_fuel_efficiency()
        avg_consumption = sum(item["consumption_l_per_100km"] for item in efficiencies) / len(efficiencies) if efficiencies else 0

        return {
            "total_records": len(self.records),
            "total_cost": round(total_cost, 2),
            "total_fuel": round(total_fuel, 2),
            "average_price": round(avg_price, 2),
            "total_distance": round(total_distance, 2),
            "average_consumption": round(avg_consumption, 2),
            "first_date": sorted_records[0].date if sorted_records else None,
            "last_date": sorted_records[-1].date if sorted_records else None
        }

    def get_records(self) -> List[Dict]:
        """获取所有记录"""
        return [record.to_dict() for record in self.records]

    def delete_record(self, index: int):
        """删除指定索引的记录"""
        if 0 <= index < len(self.records):
            del self.records[index]
            self.save_data()
            return True
        return False


def main():
    app = FuelTrackerApp()

    while True:
        print("\n=== 燃油追踪应用 ===")
        print("1. 添加加油记录")
        print("2. 查看所有记录")
        print("3. 查看油耗详情")
        print("4. 查看统计信息")
        print("5. 删除记录")
        print("6. 退出")

        choice = input("请选择操作 (1-6): ").strip()

        if choice == "1":
            print("\n--- 添加加油记录 ---")
            try:
                date_input = input("请输入日期 (YYYY-MM-DD) [默认今天]: ").strip()
                if not date_input:
                    date_input = datetime.now().strftime("%Y-%m-%d")

                odometer = float(input("请输入里程数 (km): "))
                fuel_amount = float(input("请输入加油量 (L): "))
                fuel_price = float(input("请输入油价 (元/L): "))
                station = input("请输入加油站 (可选): ").strip()
                note = input("请输入备注 (可选): ").strip()

                app.add_record(date_input, odometer, fuel_amount, fuel_price, station, note)
                print("加油记录已添加！")

            except ValueError:
                print("输入格式错误，请输入有效的数字！")
            except Exception as e:
                print(f"添加记录失败: {e}")

        elif choice == "2":
            print("\n--- 所有加油记录 ---")
            records = app.get_records()
            if not records:
                print("暂无记录")
            else:
                for i, record in enumerate(records):
                    print(f"{i+1}. {record['date']} | 里程: {record['odometer']}km | "
                          f"加油: {record['fuel_amount']}L | 价格: {record['fuel_price']}元/L | "
                          f"费用: {record['cost']:.2f}元")
                    if record['station']:
                        print(f"   加油站: {record['station']}")
                    if record['note']:
                        print(f"   备注: {record['note']}")
                    print("-" * 50)

        elif choice == "3":
            print("\n--- 油耗详情 ---")
            efficiencies = app.calculate_fuel_efficiency()
            if not efficiencies:
                print("暂无油耗数据（需要至少2条记录才能计算油耗）")
            else:
                for eff in efficiencies:
                    print(f"日期: {eff['date']} | 行驶: {eff['distance']:.2f}km | "
                          f"耗油: {eff['fuel_used']:.2f}L | 油耗: {eff['consumption_l_per_100km']:.2f}L/100km")
                print(f"\n平均油耗: {app.get_statistics()['average_consumption']:.2f}L/100km")

        elif choice == "4":
            print("\n--- 统计信息 ---")
            stats = app.get_statistics()
            if stats["total_records"] == 0:
                print("暂无记录")
            else:
                print(f"总记录数: {stats['total_records']}")
                print(f"总花费: {stats['total_cost']:.2f}元")
                print(f"总加油量: {stats['total_fuel']:.2f}L")
                print(f"平均油价: {stats['average_price']:.2f}元/L")
                print(f"总行驶里程: {stats['total_distance']:.2f}km")
                print(f"平均油耗: {stats['average_consumption']:.2f}L/100km")
                if stats['first_date'] and stats['last_date']:
                    print(f"记录期间: {stats['first_date']} 至 {stats['last_date']}")

        elif choice == "5":
            print("\n--- 删除记录 ---")
            records = app.get_records()
            if not records:
                print("暂无记录可删除")
            else:
                for i, record in enumerate(records):
                    print(f"{i}. {record['date']} | 里程: {record['odometer']}km | 费用: {record['cost']:.2f}元")
                
                try:
                    index = int(input("请输入要删除的记录编号: "))
                    if app.delete_record(index):
                        print("记录已删除！")
                    else:
                        print("无效的编号！")
                except ValueError:
                    print("请输入有效的数字！")

        elif choice == "6":
            print("感谢使用燃油追踪应用！")
            break

        else:
            print("无效选项，请重新选择！")


if __name__ == "__main__":
    main()