# Creates a Desktop Shortcut for ScholasticPulse Version 3 (Exam & AI Edition)
$wsh = New-Object -ComObject WScript.Shell
$desktop = [System.Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop "ScholasticPulse Version 3 (Exam & AI Edition).lnk"
$shortcut = $wsh.CreateShortcut($shortcutPath)

$v3Dir = "D:\THARUN PROJECT\VERSION_3_WORKPLACE"
$exePath = Join-Path $v3Dir "dist\ScholasticPulse_V3.exe"
if (-not (Test-Path $exePath)) {
    $exePath = Join-Path $v3Dir "ScholasticPulse_V3.exe"
}
if (-not (Test-Path $exePath)) {
    $exePath = Join-Path $v3Dir "LAUNCH_V3_APP.bat"
}

$shortcut.TargetPath = $exePath
$shortcut.WorkingDirectory = $v3Dir
$shortcut.Description = "Tharun's ScholasticPulse Version 3 - Anti-Daydreaming Host Examination & Gemini Evaluator"
$shortcut.Save()

Write-Output "Created Desktop Shortcut: $shortcutPath -> $exePath"
