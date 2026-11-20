"""Build www/data/daily.json: a hand-picked list of well-known hadith from Sahih al-Bukhari and Sahih Muslim.
Each entry is found by an Arabic phrase, the chain of narrators is cut off, and it must have Arabic, Bengali and English.
Usage: build_daily.py <data_dir> <out_json>"""
import json, re, random, sys

D, OUT = sys.argv[1], sys.argv[2]
DIAC = re.compile(r'[ً-ٰٟـ]')
def norm(s):
    s = DIAC.sub('', s).replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ٱ', 'ا').replace('ى', 'ي')
    return re.sub(r'\s+', ' ', re.sub(r'[،,:.;"“”()\[\]\-ـ؟?!]', ' ', s)).strip()

def strip_chain(ar):
    toks = ar.split()
    nt = [norm(t) for t in toks]
    m = next((i for i, t in enumerate(nt) if re.fullmatch(r'[لبوف]?(النبي|رسول)', t)), None)
    if m is None: return None
    j = max((i for i in range(m) if nt[i] == 'عن'), default=None)
    if j is None:                      # no 'on the authority of': start at the nearest 'كان/قال/سمعت/أن'
        j = max((i for i in range(m) if nt[i] in ('كان', 'قال', 'سمعت', 'ان')), default=m)
    elif j + 1 == m:
        j2 = max((i for i in range(j) if nt[i] == 'عن'), default=None)
        if j2 is not None: j = j2
    return ' '.join(toks[j:])

# (topic, Arabic phrase). Every phrase is normalised the same way as the data before matching.
PHRASES = """
لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه
المسلم من سلم المسلمون من لسانه ويده
من كان يؤمن بالله واليوم الآخر فليقل خيرا أو ليصمت
الكلمة الطيبة صدقة
ليس الشديد بالصرعة
خيركم من تعلم القرآن وعلمه
الطهور شطر الإيمان
أدومها وإن قل
من سلك طريقا يلتمس فيه علما
إن الله رفيق يحب الرفق
لا تحاسدوا ولا تباغضوا
إياكم والظن فإن الظن أكذب الحديث
من دل على خير فله مثل أجر فاعله
اتقوا النار ولو بشق تمرة
حبيبتان إلى الرحمن
زبد البحر
المؤمن القوي خير وأحب إلى الله من المؤمن الضعيف
ما نقصت صدقة من مال
الحياء من الإيمان
إن من خياركم أحسنكم أخلاقا
من كان في حاجة أخيه كان الله في حاجته
المسلم أخو المسلم لا يظلمه ولا يسلمه
من نفس عن مسلم كربة
كن في الدنيا كأنك غريب أو عابر سبيل
نعمتان مغبون فيهما كثير من الناس الصحة والفراغ
قال لا تغضب
فليكرم ضيفه
فليكرم جاره
الساعي على الأرملة والمسكين
أنا وكافل اليتيم في الجنة
أمك ثم أمك ثم أمك
عليكم بالصدق فإن الصدق يهدي إلى البر
آية المنافق ثلاث
إن الله لا ينظر إلى صوركم وأموالكم ولكن ينظر إلى قلوبكم
يسروا ولا تعسروا وبشروا ولا تنفروا
مثل الصلوات الخمس كمثل نهر جار
من صلى البردين دخل الجنة
من صام رمضان إيمانا واحتسابا غفر له ما تقدم من ذنبه
الصيام جنة
ما من مسلم يغرس غرسا
لا تحقرن من المعروف شيئا
أفشوا السلام بينكم
تطعم الطعام وتقرأ السلام على من عرفت ومن لم تعرف
إن الله كتب الإحسان على كل شيء
أعوذ بك من الهم والحزن
من يرد الله به خيرا يفقهه في الدين
بلغوا عني ولو آية
إذا مات الإنسان انقطع عنه عمله إلا من ثلاثة
اتقوا الظلم فإن الظلم ظلمات يوم القيامة
ليس الغنى عن كثرة العرض ولكن الغنى غنى النفس
فلينظر إلى من هو أسفل منه
عجبا لأمر المؤمن إن أمره كله خير
ما يصيب المسلم من نصب ولا وصب
الصبر عند الصدمة الأولى
من أحب أن يبسط له في رزقه وينسأ له في أثره فليصل رحمه
لا يدخل الجنة قاطع
من ستر مسلما ستره الله
رحم الله رجلا سمحا إذا باع
ما كان عن ظهر غنى
اليد العليا خير من اليد السفلى
ما أكل أحد طعاما قط خيرا من أن يأكل من عمل يده
إن في الجنة بابا يقال له الريان
من قام ليلة القدر إيمانا واحتسابا
لا حسد إلا في اثنتين
إذا مرض العبد أو سافر كتب له مثل ما كان يعمل مقيما صحيحا
من عاد مريضا لم يزل في خرفة الجنة
حق المسلم على المسلم خمس
ذكرك أخاك بما يكره
إن الله طيب لا يقبل إلا طيبا
من تصدق بعدل تمرة من كسب طيب
سبعة يظلهم الله
الإيمان بضع وسبعون شعبة
بني الإسلام على خمس
اللهم أصلح لي ديني
اللهم إني أسألك الهدى والتقى والعفاف والغنى
ليتكلم بالكلمة من رضوان الله
من يضمن لي ما بين لحييه وما بين رجليه أضمن له الجنة
إذا لم تستحي فاصنع ما شئت
الحياء لا يأتي إلا بخير
ما زال جبريل يوصيني بالجار
حتى تحابوا
من لا يرحم لا يرحم
إنما الأعمال بالنيات
الدين النصيحة
مثل الحي والميت
لا إله إلا الله وحده لا شريك له له الملك وله الحمد
اللهم أعط منفقا خلفا
إني أحب فلانا فأحبه
من أحب لقاء الله أحب الله لقاءه
الآيتين من آخر سورة البقرة
لا يرحم الله من لا يرحم الناس
المؤمن للمؤمن كالبنيان يشد بعضه بعضا
في توادهم وتراحمهم وتعاطفهم
إن الله كتب الحسنات والسيئات
تعاهدوا هذا القرآن
الماهر بالقرآن
أقرب ما يكون العبد من ربه وهو ساجد
من صلى علي واحدة صلى الله عليه عشرا
تسعة وتسعين اسما
أشد فرحا بتوبة عبده
يبسط يده بالليل ليتوب مسيء النهار
ما تواضع أحد لله إلا رفعه الله
مثقال ذرة من كبر
من بنى لله مسجدا
بسبع وعشرين درجة
من صلى الصبح فهو في ذمة الله
الصلاة على وقتها
""".strip().split('\n')

books = {b: {l: json.load(open(f'{D}/{b}.{l}.json', encoding='utf-8')) for l in ('ar', 'bn', 'en')} for b in ('bukhari', 'muslim')}
norm_ar = {b: {k: norm(v) for k, v in p['ar'].items()} for b, p in books.items()}
CHAINONLY = re.compile(r"(same (chain|authorit|isnad)|narrated it on the same|by another chain|as above|like the above|with the same)", re.I)

picked, used, missing = [], set(), []
for ph in PHRASES:
    nph = norm(ph)
    best = None
    for b, p in books.items():
        for k, t in norm_ar[b].items():
            if nph not in t or not re.fullmatch(r'\d+', k) or (b, k) in used: continue
            if k not in p['bn'] or k not in p['en'] or CHAINONLY.search(p['en'][k]): continue
            ar = strip_chain(p['ar'][k])
            if not ar or len(ar) > 680 or len(p['en'][k]) > 900 or len(p['bn'][k]) > 1000: continue
            if best is None or len(ar) < len(best[3]):
                best = (b, k, ph, ar)
    if best is None:
        missing.append(ph); continue
    b, k, ph, ar = best
    used.add((b, k))
    picked.append({'b': b, 'n': int(k), 'ar': ar, 'bn': books[b]['bn'][k].strip(), 'en': books[b]['en'][k].strip()})

# dedupe by English text (the same hadith can appear twice under different phrases)
seen, out = set(), []
for x in picked:
    key = re.sub(r'\W+', '', x['en'].lower())[:80]
    if key in seen: continue
    seen.add(key); out.append(x)
random.Random(20261120).shuffle(out)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('phrases', len(PHRASES), '| found', len(picked), '| after dedupe', len(out), '| not found:', len(missing))
for m in missing: print('  MISSING:', m)
print('---- check (book #n | English start) ----')
for x in sorted(out, key=lambda z: (z['b'], z['n'])):
    print(f"{x['b'][:3]} {x['n']:5} | {x['en'][:105]}")
