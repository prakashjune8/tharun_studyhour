$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath('Desktop')
$ShortcutPath = Join-Path -Path $DesktopPath -ChildPath "ScholasticPulse Class 8.lnk"

# Target executable preference: dist\ScholasticPulse.exe if built, otherwise pythonw launcher
$ExePath = "d:\THARUN PROJECT\dist\ScholasticPulse.exe"
$BatPath = "d:\THARUN PROJECT\LAUNCH_APP.bat"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
if (Test-Path $ExePath) {
    $Shortcut.TargetPath = $ExePath
    $Shortcut.WorkingDirectory = "d:\THARUN PROJECT"
    $Shortcut.Description = "Class 8 Study Routine & Timetable Balancer"
} else {
    $Shortcut.TargetPath = $BatPath
    $Shortcut.WorkingDirectory = "d:\THARUN PROJECT"
    $Shortcut.Description = "Class 8 Study Routine & Timetable Balancer"
}
$Shortcut.Save()
Write-Host "✅ Desktop shortcut created successfully on Desktop: $ShortcutPath"
