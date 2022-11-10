@echo off

title XML Formatter
chcp 65001

@REM In case of SendTo, input folder path is already passed.
if "%~1"=="" (set /p "path_in=File or Folder: ") else (set "path_in=%~1")
set path_in=%path_in:"=%
echo path_in=[%path_in%]

@REM absolute path to xml_format.exe
@REM %~dp0 will return the Drive and Path to the batch script including the ending backslash
@REM Assumption: python.exe is already registered in PATH.
set "app=%~dp0xml_format.py"
set app=%app:"=%
set app=python.exe "%app%"
echo app=[%app%]

@REM get switch
set /p "sw= -f, -t, --format, or --test: "
echo sw=[%sw%]

@REM get output folder
set /p "dir_out=output folder: "
set dir_out=%dir_out:"=%
echo dir_out=[%dir_out%]

@REM construct the statement
@REM paths are enclosed in double quotes
set statement=%app% %sw% -i "%path_in%" -o "%dir_out%"
echo statement=[%statement%]
echo Wait for the application to start...
%statement%

pause
