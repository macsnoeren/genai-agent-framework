@echo off
xcopy ..\..\data\output\todos\todo_master_list.jsonl
echo Webserver wordt gestart vanuit de master map...
REM cd /d "%~dp0"
REM Start de browser met de juiste URL naar de todo pagina
start http://localhost:8000/index.html
REM Start de Python HTTP server op de standaard poort 8000
C:/Users/macsnoer/AppData/Local/Microsoft/WindowsApps/python3.13.exe server.py