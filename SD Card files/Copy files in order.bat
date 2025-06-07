@echo off
setlocal enabledelayedexpansion

:: Set SD card drive (change this if needed!)
set "DEST=H:\"

echo ============================================
echo Preparing to copy files to SD card (%DEST%)
echo Root files 0001–0073
echo ============================================

if not exist "%DEST%" (
    echo ERROR: Destination %DEST% not found!
    pause
    exit /b
)

:: Copy root files in order
echo Copying root files (0001.mp3 to 0073.mp3)...
for %%F in (0001.mp3 0002.mp3 0003.mp3 0004.mp3 0005.mp3 0006.mp3 0007.mp3 0008.mp3 0009.mp3 0010.mp3 0011.mp3 0012.mp3 0013.mp3 0014.mp3 0015.mp3 0016.mp3 0017.mp3 0018.mp3 0019.mp3 0020.mp3 0021.mp3 0022.mp3 0023.mp3 0024.mp3 0025.mp3 0026.mp3 0027.mp3 0028.mp3 0029.mp3 0030.mp3 0031.mp3 0032.mp3 0033.mp3 0034.mp3 0035.mp3 0036.mp3 0037.mp3 0038.mp3 0039.mp3 0040.mp3 0041.mp3 0042.mp3 0043.mp3 0044.mp3 0045.mp3 0046.mp3 0047.mp3 0048.mp3 0049.mp3 0050.mp3 0051.mp3 0052.mp3 0053.mp3 0054.mp3 0055.mp3 0056.mp3 0057.mp3 0058.mp3 0059.mp3 0060.mp3 0061.mp3 0062.mp3 0063.mp3 0064.mp3 0065.mp3 0066.mp3 0067.mp3 0068.mp3 0069.mp3 0070.mp3 0071.mp3 0072.mp3 0073.mp3) do (
    if exist "%%F" (
        echo Copying: %%F
        copy /Y "%%F" "%DEST%" >nul
    )
)


echo ============================================
echo All files copied successfully.
echo ============================================
echo Safely eject the SD card before use!
pause
