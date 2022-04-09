@echo off

curl https://raw.githubusercontent.com/TabeFlipStudio/Dont-Get-Expelled/testy/gamefiles/version.txt -o %USERPROFILE%\Documents\Dont-Get-Expelled/temporary\version.txt 

set /p origin=< %USERPROFILE%\Documents\Dont-Get-Expelled\temporary\version.txt
# TODO: this the downloaded file


set /p local=< %USERPROFILE%\Documents\Dont-Get-Expelled\gamefiles\version.txt

if %mytextfile% == %mytextfile2% (
    echo "You have the latest version"
) else (
    echo You don't have the latest version
    echo.
    echo Downloading...

    rmdir /Q /s %USERPROFILE%\Documents\Dont-Get-Expelled

    mkdir %USERPROFILE%\Documents\Dont-Get-Expelled

    curl -L https://github.com/TabeFlipStudio/Dont-Get-Expelled/archive/refs/heads/testy.zip -o %USERPROFILE%\Documents\Dont-Get-Expelled\Dont-Get-Expelled.zip

    powershell expand-archive %USERPROFILE%\Documents\Dont-Get-Expelled\Dont-Get-Expelled.zip %USERPROFILE%\Documents\Dont-Get-Expelled\

    cd /d %USERPROFILE%\Desktop

    cd /d %USERPROFILE%\Documents\Dont-Get-Expelled

    del /Q /F Dont-Get-Expelled.zip

    move Dont-Get-Expelled-testy\gamefiles %USERPROFILE%\Documents\Dont-Get-Expelled\

    move gamefiles\bat-files\START-DoGeX.bat %USERPROFILE%\Desktop\

    move gamefiles\bat-files\uninstall-DoGeX.bat %USERPROFILE%\Documents\Dont-Get-Expelled\

    mkdir %USERPROFILE%\Documents\Dont-Get-Expelled\temporary

    rmdir /Q /s Dont-Get-Expelled-testy

    cls

)
    
pause
cd /d %USERPROFILE%\Documents\Dont-Get-Expelled\gamefiles

python dontgetexpelled.py && exit /B
