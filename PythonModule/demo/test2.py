from moviepy import *
import glob

video = VideoFileClip(r"E:\Temp\哈基米倒反天罡居然捕食哈基鹰？.mp4")

print(video.duration)

print(f'宽度: {video.w}')
print(f'高度: {video.h}')
print(f'帧率: {video.fps}')
print(f'总帧数: {video.reader.n_frames}')
print(f'名称: {video.reader.filename}')

# 清除音量
# video = video.without_audio()

# 截取
# video = video.subclipped(0, 5)
# 输出
# video = video.write_videofile('E:\\Temp\\new.mp4', codec='libx264')
# 裁剪画面区域
# video.cropped()
# 删除某一段
# video.with_section_cut_out()
# 缩放尺寸
# video.resized()
# 设置帧率
# video.with_fps(30)
# 设置时长
# video.with_duration(1000)
# 倍数
# video.with_speed_scaled(2.0)
# 设置播放器延迟起始时间
# video.with_start()
# 播放结束时间
# video.with_end()


# 获取音频对象
# video.audio
# 去掉音频
# video.without_audio()
# 加上音频
# video.with_audio()
# 调整音量
# video.with_volume_scaled(1.5)


# 创建文字clip
TextClip('text', font_size=24, color='white')
# 合成多个视频/文字/图层
CompositeVideoClip([video, TextClip('text')])
# 拼接多个视频
concatenate_videoclips([video, video])
# 加载图片进视频
ImageClip('xxx.png')
# 设置图层位置
video.with_position('center')

# 旋转画面
# video.rotated(180)

# 获取文件夹中所有图片
glob.glob('path/*.png') # 获取xxx.png

# 图片转视频
ImageClip('xxx.png', duration=5)
# 多张图片转视频
ImageSequenceClip(['path'], fps=1/2) # 每张图片2s

# 导出gif
video.write_gif('out.gif')
# 截图
video.save_frame('out.png', t=5)

video.subclipped(
    5,
    15
).write_videofile(
    'E:\\Temp\\new.mp4',
    codec='libx264', # h264(mp4) copy(拷贝)
    audio_codec='aac'
)