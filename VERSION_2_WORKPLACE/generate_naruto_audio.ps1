$ErrorActionPreference = "Stop"

$audioDir = "d:\THARUN PROJECT\assets\naruto_audio"
if (-not (Test-Path $audioDir)) {
    New-Item -ItemType Directory -Path $audioDir -Force | Out-Null
}

$quotes = @(
    @{
        id = "quote_01"
        character = "Naruto Uzumaki"
        role = "Seventh Hokage • Hero of the Leaf"
        category = "Morale & Grit"
        theme = "Never Give Up • Nindo"
        quote = "I'm not gonna run away, I never go back on my word! That's my nindo, my ninja way! Dattebayo! Let's conquer this study session, Tharun!"
        speech_text = "I am not gonna run away, I never go back on my word! That is my ninja way! Dattebayo! Let us conquer this study session, Tharun!"
        file = "quote_01.wav"
    },
    @{
        id = "quote_02"
        character = "Naruto Uzumaki"
        role = "Seventh Hokage • Hero of the Leaf"
        category = "Morale & Grit"
        theme = "Changing Your Destiny"
        quote = "If you don't like the hand that fate dealt you, don't just accept it. Have the courage to change it! Solve this next problem right now!"
        speech_text = "If you don't like the hand that fate dealt you, don't just accept it. Have the courage to change it! Solve this next problem right now!"
        file = "quote_02.wav"
    },
    @{
        id = "quote_03"
        character = "Naruto Uzumaki"
        role = "Seventh Hokage • Hero of the Leaf"
        category = "Money Management"
        theme = "Gama-chan Wallet & Value of Money"
        quote = "Every single coin in my Gama-chan frog wallet was earned through sweat and hard training! Never waste your money on foolish junk, Tharun. Save your coins and invest them in your future skills!"
        speech_text = "Every single coin in my frog wallet was earned through sweat and hard training! Never waste your money on foolish junk, Tharun. Save your coins and invest them in your future skills!"
        file = "quote_03.wav"
    },
    @{
        id = "quote_04"
        character = "Naruto Uzumaki"
        role = "Seventh Hokage • Hero of the Leaf"
        category = "Success & Mastery"
        theme = "Belief in Your Brain"
        quote = "Hard work is worthless for those that don't believe in themselves! Believe in your own brain, stay focused, and victory is yours!"
        speech_text = "Hard work is worthless for those that don't believe in themselves! Believe in your own brain, stay focused, and victory is yours!"
        file = "quote_04.wav"
    },
    @{
        id = "quote_05"
        character = "Kakashi Hatake"
        role = "Copy Ninja • Sixth Hokage"
        category = "Morale & Grit"
        theme = "Duty & Consistency"
        quote = "Those who break the rules are scum, that's true. But those who abandon their duties and goals are worse than scum. Stay disciplined and finish your timetable!"
        speech_text = "Those who break the rules are scum, that is true. But those who abandon their duties and goals are worse than scum. Stay disciplined and finish your timetable!"
        file = "quote_05.wav"
    },
    @{
        id = "quote_06"
        character = "Kakashi Hatake"
        role = "Copy Ninja • Sixth Hokage"
        category = "Success & Mastery"
        theme = "Calm Composure Under Pressure"
        quote = "Don't look away from difficult challenges. If you keep your head cool and breathe, even the most complex exam question will reveal its solution."
        speech_text = "Do not look away from difficult challenges. If you keep your head cool and breathe, even the most complex exam question will reveal its solution."
        file = "quote_06.wav"
    },
    @{
        id = "quote_07"
        character = "Kakashi Hatake"
        role = "Copy Ninja • Sixth Hokage"
        category = "Money Management"
        theme = "Resource & Wealth Stewardship"
        quote = "A true shinobi treats money and time as finite tactical resources. Just like managing your chakra reserves in battle, manage your pocket money with foresight and discipline. Waste nothing."
        speech_text = "A true shinobi treats money and time as finite tactical resources. Just like managing your chakra reserves in battle, manage your pocket money with foresight and discipline. Waste nothing."
        file = "quote_07.wav"
    },
    @{
        id = "quote_08"
        character = "Kakashi Hatake"
        role = "Copy Ninja • Sixth Hokage"
        category = "Success & Mastery"
        theme = "Advance Preparation Wins Battles"
        quote = "In battle, preparation decides the victor before swords even clash. Finish your homework slabs today, Tharun, and tomorrow's exam will be an easy victory."
        speech_text = "In battle, preparation decides the victor before swords even clash. Finish your homework slabs today, Tharun, and tomorrow's exam will be an easy victory."
        file = "quote_08.wav"
    },
    @{
        id = "quote_09"
        character = "Jiraiya"
        role = "The Toad Sage • Legendary Sannin"
        category = "Morale & Grit"
        theme = "Valuing Every Minute"
        quote = "A ninja's life is not measured by how many years you live, but by what you accomplish with your heart. Make every study minute count, Tharun!"
        speech_text = "A ninja's life is not measured by how many years you live, but by what you accomplish with your heart. Make every study minute count, Tharun!"
        file = "quote_09.wav"
    },
    @{
        id = "quote_10"
        character = "Jiraiya"
        role = "The Toad Sage • Legendary Sannin"
        category = "Money Management"
        theme = "True Wealth vs Showing Off"
        quote = "Listen closely, Tharun! Wealth isn't about showing off shiny toys to impress strangers. True financial mastery means living below your means, saving your rewards, and letting your wealth quietly grow like sage chakra!"
        speech_text = "Listen closely, Tharun! Wealth is not about showing off shiny toys to impress strangers. True financial mastery means living below your means, saving your rewards, and letting your wealth quietly grow like sage chakra!"
        file = "quote_10.wav"
    },
    @{
        id = "quote_11"
        character = "Jiraiya"
        role = "The Toad Sage • Legendary Sannin"
        category = "Morale & Grit"
        theme = "Guts to Never Give Up"
        quote = "The true measure of a shinobi isn't how talented you are when things are easy. It is having the guts to never give up when the math problem gets tough!"
        speech_text = "The true measure of a shinobi is not how talented you are when things are easy. It is having the guts to never give up when the math problem gets tough!"
        file = "quote_11.wav"
    },
    @{
        id = "quote_12"
        character = "Jiraiya"
        role = "The Toad Sage • Legendary Sannin"
        category = "Money Management"
        theme = "Budgeting and Financial Freedom"
        quote = "A fool spends their money the minute it touches their palms and spends their life running after pennies. A master plans their budget, saves for tomorrow, and walks in total freedom!"
        speech_text = "A fool spends their money the minute it touches their palms and spends their life running after pennies. A master plans their budget, saves for tomorrow, and walks in total freedom!"
        file = "quote_12.wav"
    },
    @{
        id = "quote_13"
        character = "Might Guy"
        role = "Konoha's Sublime Green Beast"
        category = "Morale & Grit"
        theme = "Hard Work Beats Talent"
        quote = "A failure will surpass even a born genius through sheer unrelenting hard work! Look at me, Tharun! Let the passionate power of youth explode in your studies!"
        speech_text = "A failure will surpass even a born genius through sheer unrelenting hard work! Look at me, Tharun! Let the passionate power of youth explode in your studies!"
        file = "quote_13.wav"
    },
    @{
        id = "quote_14"
        character = "Might Guy"
        role = "Konoha's Sublime Green Beast"
        category = "Success & Mastery"
        theme = "Quiet Practice When Nobody Looks"
        quote = "It is not about being born lucky! It is about how many hours of quiet practice you put in when everyone else is playing! Push for 10 more minutes!"
        speech_text = "It is not about being born lucky! It is about how many hours of quiet practice you put in when everyone else is playing! Push for ten more minutes!"
        file = "quote_14.wav"
    },
    @{
        id = "quote_15"
        character = "Might Guy"
        role = "Konoha's Sublime Green Beast"
        category = "Money Management"
        theme = "Iron Will Over Financial Temptation"
        quote = "Youth is strong, but disciplined habits are unbreakable! Resisting silly temptations to spend money is the ultimate test of iron willpower! Guard your savings like your ninja tools!"
        speech_text = "Youth is strong, but disciplined habits are unbreakable! Resisting silly temptations to spend money is the ultimate test of iron willpower! Guard your savings like your ninja tools!"
        file = "quote_15.wav"
    },
    @{
        id = "quote_16"
        character = "Iruka Umino"
        role = "First Academy Mentor • Headmaster"
        category = "Success & Mastery"
        theme = "Daily Incremental Progress"
        quote = "Great shinobi are never made in a single afternoon. Day by day, concept by concept, textbook page by page—that is how champions are built. I believe in you, Tharun!"
        speech_text = "Great shinobi are never made in a single afternoon. Day by day, concept by concept, textbook page by page, that is how champions are built. I believe in you, Tharun!"
        file = "quote_16.wav"
    },
    @{
        id = "quote_17"
        character = "Iruka Umino"
        role = "First Academy Mentor • Headmaster"
        category = "Morale & Grit"
        theme = "Inner Strength For Loved Ones"
        quote = "When you work hard to honor your family and build your future, an extraordinary strength awakens inside you. Keep pushing, you are doing great!"
        speech_text = "When you work hard to honor your family and build your future, an extraordinary strength awakens inside you. Keep pushing, you are doing great!"
        file = "quote_17.wav"
    },
    @{
        id = "quote_18"
        character = "Minato Namikaze"
        role = "The Yellow Flash • Fourth Hokage"
        category = "Success & Mastery"
        theme = "Precision Over Rushing"
        quote = "Speed without precision is meaningless. In exams, read every question carefully, double-check your steps, and execute with flawless confidence."
        speech_text = "Speed without precision is meaningless. In exams, read every question carefully, double-check your steps, and execute with flawless confidence."
        file = "quote_18.wav"
    },
    @{
        id = "quote_19"
        character = "Minato Namikaze"
        role = "The Yellow Flash • Fourth Hokage"
        category = "Morale & Grit"
        theme = "Calm Under Extreme Pressure"
        quote = "True strength is shown when the pressure rises. Keep your breathing steady, trust your preparation, and claim your victory!"
        speech_text = "True strength is shown when the pressure rises. Keep your breathing steady, trust your preparation, and claim your victory!"
        file = "quote_19.wav"
    },
    @{
        id = "quote_20"
        character = "Tsunade Senju"
        role = "Fifth Hokage • Legendary Sannin"
        category = "Money Management"
        theme = "Financial Prudence & Anti-Gambling"
        quote = "Gambling and careless spending are a fool's trap! A real leader budgets every coin, saves for rainy days, and values financial security above all vanity!"
        speech_text = "Careless spending is a fool's trap! A real leader budgets every coin, saves for rainy days, and values financial security above all vanity!"
        file = "quote_20.wav"
    },
    @{
        id = "quote_21"
        character = "Tsunade Senju"
        role = "Fifth Hokage • Legendary Sannin"
        category = "Morale & Grit"
        theme = "Mistakes Are Training Data"
        quote = "Making a mistake on a test is just data for your comeback. Stand back up, analyze where you slipped, and become unstoppable!"
        speech_text = "Making a mistake on a test is just data for your comeback. Stand back up, analyze where you slipped, and become unstoppable!"
        file = "quote_21.wav"
    },
    @{
        id = "quote_22"
        character = "Asuma Sarutobi"
        role = "Elite Jonin Mentor • Guardian Twelve"
        category = "Success & Mastery"
        theme = "Protecting the Future 'King'"
        quote = "The 'King' of Konoha isn't the Hokage or the commanders. The 'King' is the next generation—you, Tharun! Your knowledge and wisdom are what will shape the future!"
        speech_text = "The King of our village is not the Hokage or the commanders. The King is the next generation, you, Tharun! Your knowledge and wisdom are what will shape the future!"
        file = "quote_22.wav"
    },
    @{
        id = "quote_23"
        character = "Asuma Sarutobi"
        role = "Elite Jonin Mentor • Guardian Twelve"
        category = "Money Management"
        theme = "Strategic Investment Over Cheap Thrills"
        quote = "In shogi, sacrificing pieces for quick thrills loses the game. The same is true with money and study time—trade short-term comfort for lifelong mastery and financial strength!"
        speech_text = "In chess and shogi, sacrificing pieces for quick thrills loses the game. The same is true with money and study time. Trade short-term comfort for lifelong mastery and financial strength!"
        file = "quote_23.wav"
    },
    @{
        id = "quote_24"
        character = "Yamato Sensei"
        role = "Wood Release Master • Team Yamato"
        category = "Success & Mastery"
        theme = "Deep Academic Roots"
        quote = "Deep roots weather the strongest hurricanes. Build your academic foundation in Math, Science, and Languages today, and nothing in life will ever shake you!"
        speech_text = "Deep roots weather the strongest hurricanes. Build your academic foundation in Math, Science, and Languages today, and nothing in life will ever shake you!"
        file = "quote_24.wav"
    }
)

Write-Host "Synthesizing 24 Naruto Shinobi Audio Tracks into $audioDir..."

Add-Type -AssemblyName System.Speech

foreach ($item in $quotes) {
    $outPath = Join-Path -Path $audioDir -ChildPath $item.file
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    try {
        # Select voice if available
        $voices = $synth.GetInstalledVoices() | Where-Object { $_.Enabled }
        if ($voices.Count -gt 0) {
            # alternate between first and second voice for character variety
            if ($item.character -match "Tsunade") {
                $femaleVoice = $voices | Where-Object { $_.VoiceInfo.Gender -eq "Female" -or $_.VoiceInfo.Name -match "Zira|Hazel" } | Select-Object -First 1
                if ($femaleVoice) { $synth.SelectVoice($femaleVoice.VoiceInfo.Name) }
            } elseif ($item.character -match "Guy|Naruto") {
                $synth.Rate = 1 # energetic
            } else {
                $synth.Rate = 0 # poised mentor
            }
        }
        $synth.SetOutputToWaveFile($outPath)
        $synth.Speak($item.speech_text)
        Write-Host "  -> Generated: $($item.file) ($($item.character) - $($item.theme))"
    } finally {
        $synth.Dispose()
    }
}

# Save structured manifest
$manifestPath = Join-Path -Path $audioDir -ChildPath "quotes_manifest.json"
$quotes | ConvertTo-Json -Depth 5 | Set-Content -Path $manifestPath -Encoding utf8
Write-Host "Manifest saved to $manifestPath"
Write-Host "Total audio files created: $($quotes.Count)"
