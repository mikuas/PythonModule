# coding:utf-8
import glob
from moviepy import *

# 获取文件路径列表（这里只取前 10 个图片）
filePath = glob.glob(r"C:\Users\Administrator\OneDrive\Pictures\*.jpg")[:20]

newFile = []

for file in filePath:
    if ImageClip(file).size == (2880, 1800):
        newFile.append(file)

# 使用图片序列创建视频，并设置帧率为每秒 0.5 帧
# video = ImageSequenceClip(newFile, fps=1/2)
video = ImageSequenceClip(newFile, fps=1/2)

audio = AudioFileClip(r"E:\Temp\BiliVideos\【hjm】晴天.mp3")
audio = audio.subclipped(0, len(newFile) * 2)

text = TextClip(font=r'C:\Windows\Fonts\Arial.ttf', text='Hello World', font_size=64, color='white')
text = text.with_duration(len(newFile) * 2)
text = text.with_position('center')
"""
'center'：文本在屏幕的中央。

'top'：文本放置在顶部中心。

'bottom'：文本放置在底部中心。

'left'：文本放置在左侧中间。

'right'：文本放置在右侧中间。

'top-left'：文本放置在左上角。

'top-right'：文本放置在右上角。

'bottom-left'：文本放置在左下角。
"""

print(glob.glob(r'C:\Windows\Fonts\*.ttf'))

video = CompositeVideoClip([video, text])

video = video.with_audio(audio)

# 导出视频文件到指定路径
video.write_videofile("E:\\new.mp4", codec='libx264')
