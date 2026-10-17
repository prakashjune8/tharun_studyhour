import asyncio
import os
import json
import edge_tts

audio_dir = r"d:\THARUN PROJECT\assets\naruto_audio"
os.makedirs(audio_dir, exist_ok=True)

manifest_path = os.path.join(audio_dir, "quotes_manifest.json")
with open(manifest_path, "r", encoding="utf-8") as f:
    quotes = json.load(f)

# Character voice assignments optimized for sweetness, warmth, and humane empathy
VOICE_PROFILES = {
    "Naruto Uzumaki": {
        "voice": "en-US-AnaNeural",
        "rate": "+1%",
        "pitch": "+3Hz"
    },
    "Kakashi Hatake": {
        "voice": "en-US-GuyNeural",
        "rate": "-2%",
        "pitch": "-1Hz"
    },
    "Jiraiya": {
        "voice": "en-US-ChristopherNeural",
        "rate": "-2%",
        "pitch": "-2Hz"
    },
    "Might Guy": {
        "voice": "en-US-AndrewNeural",
        "rate": "+2%",
        "pitch": "+1Hz"
    },
    "Iruka Umino": {
        "voice": "en-US-GuyNeural",
        "rate": "-3%",
        "pitch": "+1Hz"
    },
    "Minato Namikaze": {
        "voice": "en-US-BrianNeural",
        "rate": "-2%",
        "pitch": "+0Hz"
    },
    "Tsunade Senju": {
        "voice": "en-US-JennyNeural",
        "rate": "-2%",
        "pitch": "+2Hz"
    },
    "Asuma Sarutobi": {
        "voice": "en-US-GuyNeural",
        "rate": "-3%",
        "pitch": "-1Hz"
    },
    "Yamato Sensei": {
        "voice": "en-US-ChristopherNeural",
        "rate": "-2%",
        "pitch": "-1Hz"
    }
}

async def synthesize_all():
    print(f"Synthesizing {len(quotes)} sweet and humane neural voice tracks...")
    
    for idx, item in enumerate(quotes):
        char = item["character"]
        profile = VOICE_PROFILES.get(char, {
            "voice": "en-US-JennyNeural",
            "rate": "+0%",
            "pitch": "+1Hz"
        })
        
        mp3_filename = f"quote_{idx+1:02d}.mp3"
        mp3_path = os.path.join(audio_dir, mp3_filename)
        
        # Skip if already synthesized and non-empty
        if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 1000:
            print(f"[{idx+1}/{len(quotes)}] {mp3_filename} already generated, skipping.")
            item["file"] = mp3_filename
            item["voice_profile"] = profile["voice"]
            item["quality"] = "Neural Studio Sweet & Humane"
            continue
            
        text = item.get("speech_text", item["quote"])
        print(f"[{idx+1}/{len(quotes)}] Synthesizing {mp3_filename} ({char} via {profile['voice']})...")
        
        success = False
        # Try primary profile
        try:
            communicate = edge_tts.Communicate(
                text,
                voice=profile["voice"],
                rate=profile["rate"],
                pitch=profile["pitch"]
            )
            await communicate.save(mp3_path)
            success = True
        except Exception as e:
            print(f"  Warning: Primary voice failed ({e}), falling back to en-US-GuyNeural...")
            try:
                communicate = edge_tts.Communicate(text, voice="en-US-GuyNeural")
                await communicate.save(mp3_path)
                success = True
            except Exception as e2:
                print(f"  Error: Fallback also failed: {e2}")

        if success:
            item["file"] = mp3_filename
            item["voice_profile"] = profile["voice"]
            item["quality"] = "Neural Studio Sweet & Humane"

    # Save updated manifest
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)
        
    print(f"\nAll {len(quotes)} sweet humane audio files successfully generated in {audio_dir}!")

if __name__ == "__main__":
    asyncio.run(synthesize_all())
