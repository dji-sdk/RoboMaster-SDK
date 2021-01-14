echo=1/*>nul&@cls
@echo off
setlocal enableDelayedExpansion
::runas administrator
%1 start "" mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cls
::setlocal
::setlocal
call :setdir
call :configx86orx64

echo ------------------------------------------------------
echo                visualcppbuildtools_full                  
echo ------------------------------------------------------
::-----------------下面是目录切换定义区域------------------
::在管理员模式执行时，默认路径变更，此处将目录切换回来
:setdir
set char=%~dp0%
%char:~0,2%
cd  %~dp0%

::call :installexePackage ./VisualCppRedist_AIO_20200707.exe
::call :installexePackage ./visualcppbuildtools_full.exe
::-----------------下面是查找当前路径下的python环境------------------
set num=1
set /a num=0
for /f %%i in ('where python ^| find /i "python.exe"') do (
	set /a num+=1
)

:while
if %num% gtr 0 (
	set /a num-=1
	for /f %%i in ('where python ^| find /i "python.exe"') do (
		set ip=%%i
	)
	goto :set_path
) else (
	goto :out
)


:set_path
echo "%ip:~0,-10%"
setlocal EnableDelayedExpansion
set path
set $line=%path%
set $line=%$line: =#%
set $line=%$line:;= %
set $line=%$line:)=^^)%
set $newpath=
for %%a in (%$line%) do echo %%a | find /i "%ip:~0,-10%" || set $newpath=!$newpath!;%%a
set $newpath=!$newpath:#= !
set $newpath=!$newpath:^^=!
set path=!$newpath:~1! /m
set path=!$newpath:~1!
goto :while

:out
call :installexePackage ./python-3.7.8-amd64.exe
start iexplore "https://robomaster-dev.readthedocs.io/zh_CN/latest/index.html"
echo success install robomaster sdk
pause
goto :eof
::-----------------下面是版本函数定义区域------------------
:configx86orx64
IF %PROCESSOR_ARCHITECTURE% == AMD64 (
	set versionFlag=win64
	echo window 64bit
) else ( 
	set versionFlag=win32
	echo can not support window 32bit
	pause
)

echo Windows Version: %versionFlag%
if %versionFlag%==win32 (
	echo can not install robomaster sdk in win32
	pause
)
goto :eof

::-----------------下面是安装函数定义区域------------------
:installexePackage
echo Source:      "%~f1"
echo Strat installing "%~f1"...
start /wait %~f1
::exec /i "%~f1" /passive
echo install "%~1" OK!
echo ------------------------------------------------------
goto :eof
