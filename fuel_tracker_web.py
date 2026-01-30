#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
燃油追踪 Web 应用
使用 Flask 框架创建一个可通过浏览器访问的加油记录和油耗计算应用
"""

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime
from typing import List, Dict


class FuelTrackerWeb:
    def __init__(self, data_file: str = "fuel_records_web.json"):
        self.data_file = data_file
        self.records = []
        self.load_data()

    def load_data(self):
        """从文件加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.records = json.load(f)
            except Exception as e:
                print(f"加载数据失败: {e}")
                self.records = []

    def save_data(self):
        """保存数据到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")

    def add_record(self, date: str, odometer: float, fuel_amount: float, fuel_price: float, station: str = "", note: str = ""):
        """添加加油记录"""
        cost = fuel_amount * fuel_price
        record = {
            "date": date,
            "odometer": odometer,
            "fuel_amount": fuel_amount,
            "fuel_price": fuel_price,
            "station": station,
            "note": note,
            "cost": round(cost, 2)
        }
        self.records.append(record)
        self.records.sort(key=lambda x: x["date"])  # 按日期排序
        self.save_data()
        return record

    def calculate_fuel_efficiency(self) -> List[Dict]:
        """计算每次加油的油耗"""
        results = []
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

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        if not self.records:
            return {"total_records": 0}

        total_cost = sum(record["cost"] for record in self.records)
        total_fuel = sum(record["fuel_amount"] for record in self.records)
        avg_price = total_cost / total_fuel if total_fuel > 0 else 0

        # 获取里程范围
        sorted_records = sorted(self.records, key=lambda x: x["odometer"])
        total_distance = sorted_records[-1]["odometer"] - sorted_records[0]["odometer"] if len(sorted_records) > 1 else 0

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
            "first_date": sorted_records[0]["date"] if sorted_records else None,
            "last_date": sorted_records[-1]["date"] if sorted_records else None
        }

    def get_records(self) -> List[Dict]:
        """获取所有记录"""
        return self.records

    def delete_record(self, index: int):
        """删除指定索引的记录"""
        if 0 <= index < len(self.records):
            del self.records[index]
            self.save_data()
            return True
        return False


# 初始化应用和数据
app = Flask(__name__)
tracker = FuelTrackerWeb()


# HTML 模板
index_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>燃油追踪应用</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .card {
            background-color: #f9f9f9;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #007bff;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, textarea, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .stat-card {
            background-color: #e9f7ef;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #28a745;
        }
        .stat-label {
            font-size: 14px;
            color: #666;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .tabs {
            display: flex;
            margin-bottom: 20px;
        }
        .tab {
            padding: 10px 20px;
            background-color: #eee;
            cursor: pointer;
            border: 1px solid #ddd;
            border-bottom: none;
            border-radius: 5px 5px 0 0;
            margin-right: 5px;
        }
        .tab.active {
            background-color: #007bff;
            color: white;
        }
        .btn-danger {
            background-color: #dc3545;
        }
        .btn-danger:hover {
            background-color: #c82333;
        }
        .btn-warning {
            background-color: #ffc107;
            color: black;
        }
        .btn-warning:hover {
            background-color: #e0a800;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚗 燃油追踪应用</h1>
        
        <div class="tabs">
            <div class="tab active" onclick="showTab('dashboard')">仪表盘</div>
            <div class="tab" onclick="showTab('add')">添加记录</div>
            <div class="tab" onclick="showTab('records')">加油记录</div>
            <div class="tab" onclick="showTab('efficiency')">油耗详情</div>
            <div class="tab" onclick="showTab('stats')">统计信息</div>
        </div>
        
        <div id="dashboard" class="tab-content active">
            <h2>📊 仪表盘</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{{ stats.total_records }}</div>
                    <div class="stat-label">总记录数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">¥{{ "%.2f"|format(stats.total_cost) }}</div>
                    <div class="stat-label">总花费</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ "%.2f"|format(stats.total_distance) }}km</div>
                    <div class="stat-label">总里程</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ "%.2f"|format(stats.average_consumption) }}L/100km</div>
                    <div class="stat-label">平均油耗</div>
                </div>
            </div>
            
            <div class="card">
                <h3>📈 最近加油记录</h3>
                {% if recent_records %}
                <table>
                    <thead>
                        <tr>
                            <th>日期</th>
                            <th>里程(km)</th>
                            <th>加油量(L)</th>
                            <th>费用(¥)</th>
                            <th>加油站</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for record in recent_records[:5] %}
                        <tr>
                            <td>{{ record.date }}</td>
                            <td>{{ record.odometer }}</td>
                            <td>{{ record.fuel_amount }}</td>
                            <td>{{ record.cost }}</td>
                            <td>{{ record.station if record.station else '-' }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p>暂无加油记录</p>
                {% endif %}
            </div>
        </div>
        
        <div id="add" class="tab-content">
            <h2>➕ 添加加油记录</h2>
            <form id="addForm">
                <div class="form-group">
                    <label for="date">日期:</label>
                    <input type="date" id="date" name="date" value="{{ today }}" required>
                </div>
                <div class="form-group">
                    <label for="odometer">里程数 (km):</label>
                    <input type="number" id="odometer" name="odometer" step="0.1" placeholder="请输入里程数" required>
                </div>
                <div class="form-group">
                    <label for="fuel_amount">加油量 (L):</label>
                    <input type="number" id="fuel_amount" name="fuel_amount" step="0.01" placeholder="请输入加油量" required>
                </div>
                <div class="form-group">
                    <label for="fuel_price">油价 (元/L):</label>
                    <input type="number" id="fuel_price" name="fuel_price" step="0.01" placeholder="请输入油价" required>
                </div>
                <div class="form-group">
                    <label for="station">加油站 (可选):</label>
                    <input type="text" id="station" name="station" placeholder="请输入加油站名称">
                </div>
                <div class="form-group">
                    <label for="note">备注 (可选):</label>
                    <textarea id="note" name="note" placeholder="请输入备注"></textarea>
                </div>
                <button type="submit">添加记录</button>
            </form>
        </div>
        
        <div id="records" class="tab-content">
            <h2>📋 加油记录</h2>
            {% if records %}
            <table>
                <thead>
                    <tr>
                        <th>日期</th>
                        <th>里程(km)</th>
                        <th>加油量(L)</th>
                        <th>油价(¥/L)</th>
                        <th>费用(¥)</th>
                        <th>加油站</th>
                        <th>备注</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    {% for record in records %}
                    <tr>
                        <td>{{ record.date }}</td>
                        <td>{{ record.odometer }}</td>
                        <td>{{ record.fuel_amount }}</td>
                        <td>{{ record.fuel_price }}</td>
                        <td>{{ record.cost }}</td>
                        <td>{{ record.station if record.station else '-' }}</td>
                        <td>{{ record.note if record.note else '-' }}</td>
                        <td>
                            <button class="btn-danger" onclick="deleteRecord({{ loop.index0 }})">删除</button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p>暂无加油记录</p>
            {% endif %}
        </div>
        
        <div id="efficiency" class="tab-content">
            <h2>📊 油耗详情</h2>
            {% if efficiencies %}
            <table>
                <thead>
                    <tr>
                        <th>日期</th>
                        <th>行驶距离(km)</th>
                        <th>耗油量(L)</th>
                        <th>油耗(L/100km)</th>
                        <th>效率(km/L)</th>
                    </tr>
                </thead>
                <tbody>
                    {% for eff in efficiencies %}
                    <tr>
                        <td>{{ eff.date }}</td>
                        <td>{{ eff.distance }}</td>
                        <td>{{ eff.fuel_used }}</td>
                        <td>{{ eff.consumption_l_per_100km }}</td>
                        <td>{{ eff.efficiency_km_per_l }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p>暂无油耗数据（需要至少2条记录才能计算油耗）</p>
            {% endif %}
        </div>
        
        <div id="stats" class="tab-content">
            <h2>📈 统计信息</h2>
            <div class="card">
                <h3>总览</h3>
                <ul>
                    <li><strong>总记录数:</strong> {{ stats.total_records }}</li>
                    <li><strong>总花费:</strong> ¥{{ "%.2f"|format(stats.total_cost) }}</li>
                    <li><strong>总加油量:</strong> {{ "%.2f"|format(stats.total_fuel) }}L</li>
                    <li><strong>平均油价:</strong> ¥{{ "%.2f"|format(stats.average_price) }}/L</li>
                    <li><strong>总行驶里程:</strong> {{ "%.2f"|format(stats.total_distance) }}km</li>
                    <li><strong>平均油耗:</strong> {{ "%.2f"|format(stats.average_consumption) }}L/100km</li>
                    {% if stats.first_date and stats.last_date %}
                    <li><strong>记录期间:</strong> {{ stats.first_date }} 至 {{ stats.last_date }}</li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </div>

    <script>
        // Tab 切换功能
        function showTab(tabName) {
            // 隐藏所有 tab 内容
            const tabContents = document.querySelectorAll('.tab-content');
            tabContents.forEach(content => content.classList.remove('active'));
            
            // 移除所有 tab 的激活状态
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // 显示选中的 tab 内容
            document.getElementById(tabName).classList.add('active');
            
            // 设置选中的 tab 为激活状态
            event.target.classList.add('active');
        }
        
        // 添加记录表单提交
        document.getElementById('addForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const recordData = {};
            for (let [key, value] of formData.entries()) {
                recordData[key] = value;
            }
            
            fetch('/api/add_record', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(recordData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('记录添加成功！');
                    this.reset();
                    location.reload(); // 刷新页面以显示新记录
                } else {
                    alert('添加失败: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('添加失败，请检查网络连接');
            });
        });
        
        // 删除记录
        function deleteRecord(index) {
            if (confirm('确定要删除这条记录吗？')) {
                fetch('/api/delete_record/' + index, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('记录删除成功！');
                        location.reload(); // 刷新页面以更新记录列表
                    } else {
                        alert('删除失败: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('删除失败，请检查网络连接');
                });
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    stats = tracker.get_statistics()
    records = tracker.get_records()
    efficiencies = tracker.calculate_fuel_efficiency()
    
    # 获取最近的记录用于仪表盘展示
    recent_records = sorted(records, key=lambda x: x["date"], reverse=True)
    
    return render_template_string(
        index_template,
        stats=stats,
        records=records,
        efficiencies=efficiencies,
        recent_records=recent_records,
        today=datetime.now().strftime('%Y-%m-%d')
    )


@app.route('/api/add_record', methods=['POST'])
def add_record():
    try:
        data = request.json
        tracker.add_record(
            date=data['date'],
            odometer=float(data['odometer']),
            fuel_amount=float(data['fuel_amount']),
            fuel_price=float(data['fuel_price']),
            station=data.get('station', ''),
            note=data.get('note', '')
        )
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route('/api/delete_record/<int:index>', methods=['DELETE'])
def delete_record(index):
    try:
        if tracker.delete_record(index):
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "无效的记录索引"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


if __name__ == '__main__':
    print("燃油追踪应用启动中...")
    print("请在浏览器中访问 http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)