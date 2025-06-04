# coding:utf-8
import os

def createQrcFile(resourceDir, outputQrcPath, prefix="/"):
    with open(outputQrcPath, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE RCC><RCC version="1.0">\n')
        f.write(f'  <qresource prefix="{prefix}">\n')

        for root, _, files in os.walk(resourceDir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), resourceDir)
                rel_path = rel_path.replace("\\", "/")  # 兼容 Windows 路径
                f.write(f'    <file>{rel_path}</file>\n')

        f.write('  </qresource>\n')
        f.write('</RCC>\n')

    print(f"✅ QRC 文件已写入到: {outputQrcPath}")

if __name__ == '__main__':
    createQrcFile("date", "date/resources.qrc")