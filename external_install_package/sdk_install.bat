@echo off
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
start cmd /k "pip install -i https://pypi.tuna.tsinghua.edu.cn/simple robomaster"