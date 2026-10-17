$ErrorActionPreference = "Stop"

$audioDir = "d:\THARUN PROJECT\assets\naruto_audio"
$manifestPath = Join-Path $audioDir "quotes_manifest.json"

if (-not (Test-Path $manifestPath)) {
    Write-Error "Manifest not found: $manifestPath"
    exit 1
}

$raw = Get-Content -Path $manifestPath -Raw -Encoding utf8
$quotes = $raw | ConvertFrom-Json

Write-Host "Synthesizing $($quotes.Count) Naruto audio tracks from manifest..."

Add-Type -AssemblyName System.Speech

$voices = @()
try {
    $tempSynth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $voices = $tempSynth.GetInstalledVoices() | Where-Object { $_.Enabled }
    $tempSynth.Dispose()
} catch {}

foreach ($item in $quotes) {
    $outPath = Join-Path $audioDir $item.file
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    try {
        if ($voices.Count -gt 0) {
            if ($item.character -match "Tsunade") {
                $fem = $voices | Where-Object { $_.VoiceInfo.Gender -eq "Female" -or $_.VoiceInfo.Name -match "Zira|Hazel" } | Select-Object -First 1
                if ($fem) { $synth.SelectVoice($fem.VoiceInfo.Name) }
            } elseif ($item.character -match "Guy|Naruto") {
                $synth.Rate = 1
            } else {
                $synth.Rate = 0
            }
        }
        $synth.SetOutputToWaveFile($outPath)
        $synth.Speak($item.speech_text)
        Write-Host "  -> Generated: $($item.file) [$($item.character) - $($item.theme)]"
    } finally {
        $synth.Dispose()
    }
}

Write-Host "All audio files successfully generated in $audioDir"
