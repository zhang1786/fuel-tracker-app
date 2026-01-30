#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单燃油追踪服务器
使用Python内置的http.server创建一个简单的Web界面
"""

import json
import os
from datetime import datetime
from urllib.parse import parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
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


tracker = FuelTrackerSimple()


class FuelTrackerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = self.generate_index_page()
            self.wfile.write(html.encode('utf-8'))
        elif self.path == '/api/records':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            records = tracker.get_records()
            self.wfile.write(json.dumps(records, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/api/efficiency':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            efficiency = tracker.calculate_fuel_efficiency()
            self.wfile.write(json.dumps(efficiency, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            stats = tracker.get_statistics()
            self.wfile.write(json.dumps(stats, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        if self.path == '/api/add_record':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # 解析表单数据
            parsed_data = parse_qs(post_data)
            
            try:
                date = parsed_data.get('date', [''])[0]
                odometer = float(parsed_data.get('odometer', [0])[0])
                fuel_amount = float(parsed_data.get('fuel_amount', [0])[0])
                fuel_price = float(parsed_data.get('fuel_price', [0])[0])
                station = parsed_data.get('station', [''])[0]
                note = parsed_data.get('note', [''])[0]
                
                tracker.add_record(date, odometer, fuel_amount, fuel_price, station, note)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = json.dumps({"success": True}, ensure_ascii=False)
                self.wfile.write(response.encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = json.dumps({"success": False, "message": str(e)}, ensure_ascii=False)
                self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def generate_index_page(self):
        stats = tracker.get_statistics()
        records = tracker.get_records()
        efficiencies = tracker.calculate_fuel_efficiency()
        recent_records = sorted(records, key=lambda x: x["date"], reverse=True)[:5]
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>燃油追踪应用</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        .card {{
            background-color: #f9f9f9;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #007bff;
        }}
        .form-group {{
            margin-bottom: 15px;
        }}
        label {{
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }}
        input, textarea {{
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }}
        button {{
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }}
        button:hover {{
            background-color: #0056b3;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .stat-card {{
            background-color: #e9f7ef;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #28a745;
        }}
        .stat-label {{
            font-size: 14px;
            color: #666;
        }}
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
        .tabs {{
            display: flex;
            margin-bottom: 20px;
            overflow-x: auto;
        }}
        .tab {{
            padding: 10px 20px;
            background-color: #eee;
            cursor: pointer;
            border: 1px solid #ddd;
            border-bottom: none;
            border-radius: 5px 5px 0 0;
            margin-right: 5px;
            white-space: nowrap;
        }}
        .tab.active {{
            background-color: #007bff;
            color: white;
        }}
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
                    <div class="stat-value">{stats['total_records']}</div>
                    <div class="stat-label">总记录数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">¥{stats['total_cost']:.2f}</div>
                    <div class="stat-label">总花费</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['total_distance']:.2f}km</div>
                    <div class="stat-label">总里程</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['average_consumption']:.2f}L/100km</div>
                    <div class="stat-label">平均油耗</div>
                </div>
            </div>
            
            <div class="card">
                <h3>📈 最近加油记录</h3>
                {self.generate_recent_records_table(recent_records)}
            </div>
        </div>
        
        <div id="add" class="tab-content">
            <h2>➕ 添加加油记录</h2>
            <form id="addForm" method="post" action="/api/add_record">
                <div class="form-group">
                    <label for="date">日期:</label>
                    <input type="date" id="date" name="date" value="{datetime.now().strftime('%Y-%m-%d')}" required>
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
            {self.generate_full_records_table(records)}
        </div>
        
        <div id="efficiency" class="tab-content">
            <h2>📊 油耗详情</h2>
            {self.generate_efficiency_table(efficiencies)}
        </div>
        
        <div id="stats" class="tab-content">
            <h2>📈 统计信息</h2>
            <div class="card">
                <h3>总览</h3>
                <ul>
                    <li><strong>总记录数:</strong> {stats['total_records']}</li>
                    <li><strong>总花费:</strong> ¥{stats['total_cost']:.2f}</li>
                    <li><strong>总加油量:</strong> {stats['total_fuel']:.2f}L</li>
                    <li><strong>平均油价:</strong> ¥{stats['average_price']:.2f}/L</li>
                    <li><strong>总行驶里程:</strong> {stats['total_distance']:.2f}km</li>
                    <li><strong>平均油耗:</strong> {stats['average_consumption']:.2f}L/100km</li>
                    {f'<li><strong>记录期间:</strong> {stats["first_date"]} 至 {stats["last_date"]}</li>' if stats['first_date'] and stats['last_date'] else ''}
                </ul>
            </div>
        </div>
    </div>

    <script>
        // Tab 切换功能
        function showTab(tabName) {{
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
        }}
        
        // 添加记录表单提交
        document.getElementById('addForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            
            const formData = new FormData(this);
            const params = new URLSearchParams();
            for (const pair of formData.entries()) {{
                params.append(pair[0], pair[1]);
            }}
            
            fetch('/api/add_record', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/x-www-form-urlencoded',
                }},
                body: params
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    alert('记录添加成功！');
                    this.reset();
                    location.reload(); // 刷新页面以显示新记录
                }} else {{
                    alert('添加失败: ' + data.message);
                }}
            }})
            .catch(error => {{
                console.error('Error:', error);
                alert('添加失败，请检查网络连接');
            });
        }});
        
        // 设置默认日期为今天
        document.getElementById('date').value = new Date().toISOString().split('T')[0];
    </script>
</body>
</html>
        """
        return html

    def generate_recent_records_table(self, records):
        if not records:
            return '<p>暂无加油记录</p>'
        
        table_html = """
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
        """
        
        for record in records:
            station = record['station'] if record['station'] else '-'
            table_html += f"""
                <tr>
                    <td>{record['date']}</td>
                    <td>{record['odometer']}</td>
                    <td>{record['fuel_amount']}</td>
                    <td>{record['cost']}</td>
                    <td>{station}</td>
                </tr>
            """
        
        table_html += """
            </tbody>
        </table>
        """
        return table_html

    def generate_full_records_table(self, records):
        if not records:
            return '<p>暂无加油记录</p>'
        
        table_html = """
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
                </tr>
            </thead>
            <tbody>
        """
        
        for record in records:
            station = record['station'] if record['station'] else '-'
            note = record['note'] if record['note'] else '-'
            table_html += f"""
                <tr>
                    <td>{record['date']}</td>
                    <td>{record['odometer']}</td>
                    <td>{record['fuel_amount']}</td>
                    <td>{record['fuel_price']}</td>
                    <td>{record['cost']}</td>
                    <td>{station}</td>
                    <td>{note}</td>
                </tr>
            """
        
        table_html += """
            </tbody>
        </table>
        """
        return table_html

    def generate_efficiency_table(self, efficiencies):
        if not efficiencies:
            return '<p>暂无油耗数据（需要至少2条记录才能计算油耗）</p>'
        
        table_html = """
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
        """
        
        for eff in efficiencies:
            table_html += f"""
                <tr>
                    <td>{eff['date']}</td>
                    <td>{eff['distance']}</td>
                    <td>{eff['fuel_used']}</td>
                    <td>{eff['consumption_l_per_100km']}</td>
                    <td>{eff['efficiency_km_per_l']}</td>
                </tr>
            """
        
        table_html += """
            </tbody>
        </table>
        """
        return table_html


def run_server(port=5000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, FuelTrackerHandler)
    print(f"燃油追踪应用启动中...")
    print(f"请在浏览器中访问 http://localhost:{port}")
    print("按 Ctrl+C 停止应用")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n应用已停止")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()