Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

currentDir = fso.GetParentFolderName(WScript.ScriptFullName)
exePath = currentDir & "\dist\ScholasticPulse.exe"

If fso.FileExists(exePath) Then
    WshShell.Run """" & exePath & """", 1, False
Else
    WshShell.Run "pythonw """ & currentDir & "\study_balancer.py""", 0, False
End If
