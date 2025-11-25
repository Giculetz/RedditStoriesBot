@echo off
setlocal enabledelayedexpansion

set "this_dir=%~dp0"
set "output_file=%this_dir%output_folder.txt"

if not exist "%output_file%" (
    echo Nu s-a gasit output_folder.txt
    pause
    exit /b
)

set /p target_folder=<"%output_file%"

if not exist "%target_folder%" (
    echo Folderul specificat in output_folder.txt nu exista: %target_folder%
    pause
    exit /b
)

cd /d "%target_folder%"

for /d %%F in (*) do (
    set "folder_name=%%F"
    echo(!folder_name! | findstr /c:"-postat" >nul
    if errorlevel 1 (
        set "all_mp4_postat=true"
        rem Verificam daca exista fisiere mp4
        set "mp4_found=false"
        for %%A in ("%%F\*.mp4") do (
            set "mp4_found=true"
            set "file_name=%%~nxA"
            echo(!file_name! | findstr /c:"-postat" >nul
            if errorlevel 1 (
                set "all_mp4_postat=false"
            )
        )
        if "!mp4_found!"=="true" if "!all_mp4_postat!"=="true" (
            ren "%%F" "%%F-postat"
            echo Redenumit folderul %%F in %%F-postat
        )
    )
)

echo Proces terminat.
exit 0
