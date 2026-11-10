# تشغيل:  pip install edge-tts   ثم   python make_audio.py
# ينشئ مجلد audio بجانب index.html بكل الملفات المطلوبة (٢٨ حرفاً × ٥ ملفات + ٢ تشجيع)
# الصوت: مصري (ar-EG) بسرعة أبطأ قليلاً. للصوت الذكر غيّر VOICE إلى ar-EG-ShakirNeural
import asyncio, os
import edge_tts

VOICE = "ar-EG-SalmaNeural"
RATE = "-25%"
OUT = "audio"

# الحرف، اسمه، الكلمة (بالتشكيل)
L = [("أ","أَلِف","أَرْنَب"),("ب","بَاء","بَطَّة"),("ت","تَاء","تُفَّاحَة"),("ث","ثَاء","ثَعْلَب"),
("ج","جِيم","جَمَل"),("ح","حَاء","حِصَان"),("خ","خَاء","خَرُوف"),("د","دَال","دَجَاجَة"),
("ذ","ذَال","ذُرَة"),("ر","رَاء","رَادِيُو"),("ز","زَاي","زَرَافَة"),("س","سِين","سَمَكَة"),
("ش","شِين","شَمْس"),("ص","صَاد","صَارُوخ"),("ض","ضَاد","ضِفْدَع"),("ط","طَاء","طَائِرَة"),
("ظ","ظَاء","ظَرْف"),("ع","عَيْن","عِنَب"),("غ","غَيْن","غَزَال"),("ف","فَاء","فِيل"),
("ق","قَاف","قَمَر"),("ك","كَاف","كِتَاب"),("ل","لَام","لَيْمُون"),("م","مِيم","مَوْزَة"),
("ن","نُون","نَحْلَة"),("ه","هَاء","هَدِيَّة"),("و","وَاو","وَرْدَة"),("ي","يَاء","يَد")]

items = {"good": "أَحْسَنْت! بَارَكَ اللهُ فِيك", "retry": "حَاوِلْ مَرَّةً أُخْرَى"}
for i, (ch, name, word) in enumerate(L, 1):
    k = f"l{i:02d}"
    items[f"{k}_name"] = name
    items[f"{k}_fatha"] = ch + "َ"
    items[f"{k}_damma"] = ch + "ُ"
    items[f"{k}_kasra"] = ch + "ِ"
    items[f"{k}_word"] = word

async def one(sem, fn, text):
    path = os.path.join(OUT, fn + ".mp3")
    if os.path.exists(path):
        return
    async with sem:
        await edge_tts.Communicate(text, VOICE, rate=RATE).save(path)
        print("✓", fn, text)

async def main():
    os.makedirs(OUT, exist_ok=True)
    sem = asyncio.Semaphore(4)
    await asyncio.gather(*(one(sem, f, t) for f, t in items.items()))
    print("تم. عدد الملفات:", len(items))

asyncio.run(main())
