import csv
import time
from avp_stream import VisionProStreamer
import numpy as np

avp_ip = "10.31.181.201"   # example IP
s = VisionProStreamer(ip=avp_ip, record=True)

# 设置时间步（秒）
time_step = 0.1

# 创建并打开 CSV 文件用于写入
with open('hand_movement_data.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # 写入 CSV 文件的头部
    headers = ['timestamp']
    headers += [f'head_{i}_{j}' for i in range(1) for j in range(16)]  # head (1,4,4)
    headers += [f'right_wrist_{i}_{j}' for i in range(1) for j in range(16)]  # right_wrist (1,4,4)
    headers += [f'left_wrist_{i}_{j}' for i in range(1) for j in range(16)]  # left_wrist (1,4,4)
    headers += [f'right_fingers_{i}_{j}' for i in range(25) for j in range(16)]  # right_fingers (25,4,4)
    headers += [f'left_fingers_{i}_{j}' for i in range(25) for j in range(16)]  # left_fingers (25,4,4)
    headers += [
        'right_pinch_distance', 'left_pinch_distance', 
        'right_wrist_roll', 'left_wrist_roll'
    ]

    csv_writer.writerow(headers)

    start_time = time.time()

    while True:
        r = s.latest

        # 记录当前时间戳
        current_time = time.time() - start_time

        # 将数据转换为合适的格式进行写入
        head = r['head'].reshape(-1).tolist()  # 展平为一维列表
        right_wrist = r['right_wrist'].reshape(-1).tolist()
        left_wrist = r['left_wrist'].reshape(-1).tolist()
        right_fingers = r['right_fingers'].reshape(-1).tolist()
        left_fingers = r['left_fingers'].reshape(-1).tolist()

        # 其他数据是标量，可以直接写入
        right_pinch_distance = r['right_pinch_distance']
        left_pinch_distance = r['left_pinch_distance']
        right_wrist_roll = r['right_wrist_roll']
        left_wrist_roll = r['left_wrist_roll']

        # 将所有数据合并为一行
        csv_row = [current_time] + head + right_wrist + left_wrist + right_fingers + left_fingers + [
            right_pinch_distance, left_pinch_distance, 
            right_wrist_roll, left_wrist_roll
        ]

        # 写入数据行
        csv_writer.writerow(csv_row)

        # 打印数据（可选）
        print(f'Time = {current_time:.2f}s', r['head'], r['right_wrist'], r['right_fingers'])

        # 等待下一个时间步
        time.sleep(time_step)
