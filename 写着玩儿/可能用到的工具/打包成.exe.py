# coding:utf-8
# 将当前的pycode转化为exe，需安装PyQt， pyinstaller
import os
import os.path

# Ui文件所在路径
dir = './'


def code2exe(pyfile):
    cmd = 'pyinstaller -F -w {pyfile}'.format(pyfile=pyfile)  # -F 打包为单独的exe文件； -w 使用窗口显示； -D 生成目录（！！！不常用，可以删除）
    os.system(cmd)


if __name__ == "__main__":
    code2exe('main.py')