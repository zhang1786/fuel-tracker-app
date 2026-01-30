import pandas as pd
import numpy as np
from datetime import datetime

# 读取现有的CSV数据
csv_data = """谈话人,职位,谈话对象,职务,谈话时间,谈话地点,对谈话人的意见建议,对谈话对象的意见建议,谈话人签字,谈话对象签字,记录人签字
张XX,榆阳区气象局党组书记、局长,李XX,榆阳区气象局党组成员、副局长,2025年12月15日,局会议室,""1.建议在工作中更加注重年轻干部培养；2.建议加强与其他部门的沟通协调。"",""1.在党建工作中要进一步压实责任，加强理论学习；2.在业务工作中要更加注重创新发展的思路和举措。""",张XX,李XX,王XX
张XX,榆阳区气象局党组书记、局长,赵XX,榆阳区气象局党组成员、纪检组长,2025年12月16日,局办公室,""1.建议进一步加强党风廉政建设工作；2.建议加大对基层工作的支持力度。"",""1.在纪检工作中要敢于监督、善于监督；2.在日常管理中要注意方式方法。""",张XX,赵XX,王XX
张XX,榆阳区气象局党组书记、局长,孙XX,榆阳区气象局党组成员、副局长,2025年12月17日,局会议室,""1.建议进一步提升业务管理水平；2.建议加强对青年职工的关怀。"",""1.在分管工作中要统筹兼顾各方需求；2.在具体执行中要注重细节把控。""",张XX,孙XX,王XX
张XX,榆阳区气象局党组书记、局长,马XX,榆阳区气象局党组成员、副局长,2025年12月18日,局办公室,""1.建议在业务发展方面加大创新力度；2.建议加强对外交流合作。"",""1.在工作中要进一步提高执行力；2.在团队建设中要发挥更好的引领作用。""",张XX,马XX,王XX
张XX,榆阳区气象局党组书记、局长,刘XX,榆阳区气象局党组成员、副局长,2025年12月19日,局会议室,""1.建议在队伍建设方面加大力度；2.建议提升应急处置能力。"",""1.在工作中要强化责任担当意识；2.在实际操作中要更加严谨细致。""",张XX,刘XX,王XX"""

# 将CSV数据写入临时文件
with open('/tmp/temp_talk_records.csv', 'w', encoding='utf-8-sig') as f:
    f.write(csv_data)

# 读取CSV文件
df = pd.read_csv('/tmp/temp_talk_records.csv', encoding='utf-8-sig')

# 创建Excel文件
with pd.ExcelWriter('talk_records.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='谈话记录')
    
    # 获取工作簿对象以进行格式化
    workbook = writer.book
    worksheet = writer.sheets['谈话记录']
    
    # 自动调整列宽
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)  # 限制最大宽度为50
        worksheet.column_dimensions[column_letter].width = adjusted_width

print("Excel文件已创建: talk_records.xlsx")