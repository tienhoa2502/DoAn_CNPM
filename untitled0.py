import json

with open('TheB.json', 'r', encoding='utf-8') as f:
  data = json.load(f)

print(type(data))
print(data)
import matplotlib.pyplot as plt

# Trích xuất dữ liệu từ biến data
href_values = [item['href'] for item in data]
title_values = [item['title'] for item in data]

# Tạo biểu đồ đường
plt.plot(href_values, title_values)
plt.hreflabel('href-axis')
plt.titlelabel('titel-axis')
plt.title('Data Visualization')

# Hiển thị biểu đồ
plt.savefig('data_visualization.png')
