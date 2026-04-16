@echo off
echo Initialiseren van mappenstructuur voor GenAI Agent Framework...

if not exist "data\input" mkdir "data\input"
if not exist "data\output" mkdir "data\output"
if not exist "data\done" mkdir "data\done"
if not exist "data\reports" mkdir "data\reports"
if not exist "templates" mkdir "templates"
if not exist "agents" mkdir "agents"

echo.
echo Setup voltooid. Je kunt nu bestanden in data/input plaatsen.