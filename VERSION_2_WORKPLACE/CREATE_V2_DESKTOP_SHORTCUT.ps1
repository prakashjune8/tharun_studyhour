$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath('Desktop')
$ShortcutPath = Join-Path $DesktopPath "ScholasticPulse Version 2 (Shinobi Edition).lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "d:\THARUN PROJECT\VERSION_2_WORKPLACE\dist\ScholasticPulse_V2.exe"
$Shortcut.WorkingDirectory = "d:\THARUN PROJECT\VERSION_2_WORKPLACE"
$Shortcut.Description = "ScholasticPulse Version 2 - Tharun's Habit & Time Balancer (Naruto Shinobi Edition)"
$Shortcut.Save()
Write-Host "Created Desktop Shortcut: $ShortcutPath"
