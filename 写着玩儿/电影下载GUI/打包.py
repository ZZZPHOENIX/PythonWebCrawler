# coding:utf-8
import os
import os.path

dir = './'


def code2exe(pyfile):
    #cmd = 'pyinstaller -F -w {pyfile} --icon={iconpath}'.format(iconpath='./images/icon.ico', pyfile=pyfile)  # -F 打包为单独的exe文件； -w 使用窗口显示； -D 生成目录（！！！不常用，可以删除）
    cmd = 'pyinstaller -w {pyfile} --icon={iconpath}'.format(iconpath='./images/icon.ico', pyfile=pyfile)
    os.system(cmd)


if __name__ == "__main__":
    code2exe('main.py')