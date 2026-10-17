param(
    [string]$Text = "Believe in your dreams, Tharun!",
    [string]$OutFile = "d:\THARUN PROJECT\assets\naruto_audio\temp_online.wav"
)
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $s.SetOutputToWaveFile($OutFile)
    $s.Speak($Text)
} finally {
    $s.Dispose()
}
Write-Host "Audio synthesized to $OutFile"
