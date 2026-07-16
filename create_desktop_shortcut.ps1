# Creates a desktop shortcut for the DFM Inspector
# Run once: powershell -ExecutionPolicy Bypass -File create_desktop_shortcut.ps1

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$launcherPath = Join-Path $projectDir "DFM_Inspector_Launcher.bat"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "DFM Inspector.lnk"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $launcherPath
$shortcut.WorkingDirectory = $projectDir
$shortcut.Description = "Launch DFM Inspector - Manufacturing Design Analysis Tool"
$shortcut.IconLocation = "shell32.dll,13"
$shortcut.WindowStyle = 1
$shortcut.Save()

Write-Host ""
Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host "  Desktop shortcut created successfully!" -ForegroundColor Green
Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Shortcut location: $shortcutPath" -ForegroundColor White
Write-Host "Double-click 'DFM Inspector' on your desktop to launch." -ForegroundColor White
Write-Host ""
