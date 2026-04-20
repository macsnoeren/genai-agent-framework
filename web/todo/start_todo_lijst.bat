@echo off
setlocal

:: Verkrijg de huidige datum in YYYYMMDD formaat
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set current_date=%datetime:~0,8%

set target_dir=..\..\data\input\todos
set target_file=%target_dir%\%current_date%-todo.txt

:: Maak de directory aan als deze nog niet bestaat
if not exist "%target_dir%" mkdir "%target_dir%"

:: Start notepad met het nieuwe bestand
start notepad "%target_file%"