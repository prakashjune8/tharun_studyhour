$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$ShortcutPath = Join-Path $DesktopPath "ScholasticPulse Version 1 (Baseline).lnk"
$TargetPath = "d:\THARUN PROJECT\VERSION_1_WORKPLACE\dist\ScholasticPulse_V1.exe"
$WorkingDir = "d:\THARUN PROJECT\VERSION_1_WORKPLACE"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $WorkingDir
$Shortcut.Description = "ScholasticPulse Version 1 - Safe Reboot / Reset Baseline"
$Shortcut.Save()

Write-Output "Desktop shortcut for Version 1 created: $ShortcutPath"
