# from ffprobe3 import FFProbe

video_path = 'D:\\anime\\hositsuku\\1.mp4'
video_path = 'C:\\Users\\AAO\\Videos\\123.mp4'

import subprocess
import json

def find_metadata_location(video_path):
    # 使用ffprobe命令获取视频文件信息
    cmd = ['ffprobe', '-show_format', '-of', 'json', video_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 解析ffprobe输出
    output = json.loads(result.stdout)
    print(result)

    # 检查输出中是否包含元数据信息
    if 'format' in output and 'tags' in output['format']:
        metadata = output['format']['tags']
        print("Metadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")
    else:
        print("Metadata not found in video file")

# 调用函数并传入视频文件路径
# video_path = 'path_to_your_video.mp4'
find_metadata_location(video_path)
