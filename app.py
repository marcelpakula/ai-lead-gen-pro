import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime

st.set_page_config(page_title="AI Lead Gen PRO", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; background-color: #f8fafc !important; color: #1e293b !important; }
.main .block-container { padding-top: 1.5rem; max-width: 1200px; }
section[data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #e2e8f0 !important; }
section[data-testid="stSidebar"] * { color: #475569 !important; }
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color: #1e293b !important; }
div[data-testid="stButton"] > button[kind="primary"] { background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%) !important; color: #ffffff !important; border: none !important; border-radius: 10px !important; font-size: 1rem !important; font-weight: 700 !important; width: 100% !important; box-shadow: 0 4px 14px rgba(37,99,235,0.3) !important; }
div[data-testid="stButton"] > button[kind="secondary"] { background: #ffffff !important; color: #2563eb !important; border: 1.5px solid #2563eb !important; border-radius: 8px !important; font-weight: 600 !important; }
div[data-testid="stDownloadButton"] > button { background: #f0fdf4 !important; color: #16a34a !important; border: 1.5px solid #16a34a !important; border-radius: 8px !important; font-weight: 600 !important; width: 100% !important; }
.stDataFrame thead th { background: #f1f5f9 !important; color: #2563eb !important; font-size: 0.72rem !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { color: #2563eb !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 1.9rem !important; font-weight: 700 !important; }
.stTabs [data-baseweb="tab-list"] { background: #f1f5f9 !important; border-radius: 10px !important; padding: 4px !important; }
.stTabs [aria-selected="true"] { background: #ffffff !important; color: #2563eb !important; font-weight: 700 !important; }
.stProgress > div > div { background: linear-gradient(90deg, #2563eb, #7c3aed) !important; border-radius: 10px !important; }
.kpi-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 1.3rem 1.5rem; text-align: center; box-shadow: 0 1px 6px rgba(0,0,0,0.06); }
.kpi-val { font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 700; color: #2563eb; }
.kpi-val-red { color: #dc2626 !important; }
.kpi-val-orange { color: #d97706 !important; }
.kpi-val-purple { color: #7c3aed !important; }
.kpi-label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.4rem; font-weight: 600; }
.info-box { background: #eff6ff; border: 1px solid #bfdbfe; border-left: 3px solid #2563eb; border-radius: 8px; padding: 0.9rem 1.1rem; font-size: 0.85rem; color: #1d4ed8; line-height: 1.6; }
.app-title { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: #0f172a; letter-spacing: -0.02em; }
.accent { color: #2563eb; }
.app-sub { font-size: 0.88rem; color: #94a3b8; margin-top: 0.3rem; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.2rem 0; }
.section-header { font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 700; color: #1e293b; margin-bottom: 1rem; }
.prod-badge { background: #f0fdf4; color: #16a34a; border: 1.5px solid #16a34a; border-radius: 20px; padding: 4px 14px; font-size: 0.72rem; font-weight: 700; }
.dev-badge { background: #fff7ed; color: #ea580c; border: 1.5px solid #ea580c; border-radius: 20px; padding: 4px 14px; font-size: 0.72rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── KLUCZE API ──
def get_keys():
    try:
        ak = st.secrets["ANTHROPIC_API_KEY"]
        sk = st.secrets["SERPER_API_KEY"]
        return ak, sk, True
    except:
        return None, None, False

AK_SECRET, SK_SECRET, TRYB_PROD = get_keys()

if "historia" not in st.session_state:
    st.session_state.historia = []
if "tryb_modulu" not in st.session_state:
    st.session_state.tryb_modulu = "B2B"

WOJEWODZTWA = ["Dolnoslaskie","Kujawsko-Pomorskie","Lubelskie","Lubuskie","Lodzkie","Malopolskie","Mazowieckie","Opolskie","Podkarpackie","Podlaskie","Pomorskie","Slaskie","Swietokrzyskie","Warminsko-Mazurskie","Wielkopolskie","Zachodniopomorskie"]
SIECIOWKI = ["mcdonald","kfc","burger king","biedronka","lidl","zabka","orlen","bp","shell","ikea","media markt","rossmann","douglas","reserved","h&m","zara","deichmann","pepco","action","neonet","decathlon","leroy merlin","castorama","obi ","jysk","empik"]

def generuj_zapytania_b2b(branza, lok, ak, tryb):
    if tryb == "Szybki (1 zapytanie)":
        return [branza + " " + lok]
    elif tryb == "Sredni (3 zapytania)":
        return [branza + " " + lok, "uslugi " + branza + " " + lok, branza + " " + lok + " tani"]
    try:
        r = requests.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key": ak, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": "claude-haiku-4-5", "max_tokens": 250, "messages": [{"role": "user", "content": "Wygeneruj 6 roznych zapytan Google Maps dla branzy: " + branza + " w lokalizacji: " + lok + ". TYLKO zapytania oddzielone srednikiem."}]}, timeout=15)
        tekst = r.json()["content"][0]["text"]
        return [z.strip() for z in tekst.split(";") if z.strip()][:6]
    except:
        return [branza + " " + lok, "uslugi " + branza + " " + lok, branza + " " + lok + " tani"]

def jest_sieciowka(nazwa):
    return any(s in nazwa.lower() for s in SIECIOWKI)

def szukaj_maps(q, sk, limit=10):
    try:
        r = requests.post("https://google.serper.dev/maps", headers={"X-API-KEY": sk, "Content-Type": "application/json"}, json={"q": q, "gl": "pl", "hl": "pl", "num": limit}, timeout=12)
        return [{"nazwa": p.get("title","?"), "telefon": p.get("phoneNumber","brak"), "www": p.get("website","brak"), "opinie": p.get("ratingCount",0), "ocena": p.get("rating",0), "adres": p.get("address","?"), "kategoria": p.get("category","")} for p in r.json().get("places",[])]
    except:
        return []

def szukaj_web(q, sk, limit=10):
    try:
        r = requests.post("https://google.serper.dev/search", headers={"X-API-KEY": sk, "Content-Type": "application/json"}, json={"q": q + " kontakt telefon", "gl": "pl", "hl": "pl", "num": limit}, timeout=12)
        return [{"nazwa": p.get("title","?"), "telefon": "sprawdz na stronie", "www": p.get("link","brak"), "opinie": 0, "ocena": 0, "adres": p.get("snippet","")[:100], "kategoria": ""} for p in r.json().get("organic",[])]
    except:
        return []

def weryfikuj_strone(url):
    if not url or url in ["brak","sprawdz na stronie",""]:
        return {"dziala": False, "ssl": False, "ocena_www": 0, "problemy": ["Brak strony WWW"], "ma_rezerwacje": False, "ma_social": False}
    try:
        r = requests.get(url, timeout=7, headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"}, allow_redirects=True)
        ssl = url.startswith("https")
        t = r.text.lower()
        problemy = []
        if not ssl: problemy.append("Brak SSL")
        if "viewport" not in t: problemy.append("Brak mobile")
        if not any(x in t for x in ["form","kontakt","contact"]): problemy.append("Brak formularza")
        if not any(x in t for x in ["facebook","instagram","tiktok"]): problemy.append("Brak social media")
        if len(t) < 2000: problemy.append("Uboga tresc")
        if not any(x in t for x in ["cena","cennik","price"]): problemy.append("Brak cennika")
        ma_rez = any(x in t for x in ["booksy","calendly","rezerwacja","booking"])
        if not ma_rez: problemy.append("Brak rezerwacji online")
        return {"dziala": True, "ssl": ssl, "ocena_www": max(1, 10-len(problemy)), "problemy": problemy, "ma_rezerwacje": ma_rez, "ma_social": any(x in t for x in ["facebook","instagram","tiktok"])}
    except:
        return {"dziala": False, "ssl": False, "ocena_www": 0, "problemy": ["Strona niedostepna"], "ma_rezerwacje": False, "ma_social": False}

def oblicz_score(f, wer):
    s = 40
    if f["www"] in ["brak","sprawdz na stronie",""]: s += 30
    elif not wer["dziala"]: s += 25
    elif wer["ocena_www"] <= 3: s += 20
    elif wer["ocena_www"] <= 5: s += 12
    elif wer["ocena_www"] <= 7: s += 6
    if f["opinie"] == 0: s += 15
    elif f["opinie"] < 10: s += 12
    elif f["opinie"] < 30: s += 7
    elif f["opinie"] < 80: s += 3
    if 0 < f["ocena"] < 3.5: s += 8
    if not wer["ssl"]: s += 5
    if not wer["ma_rezerwacje"]: s += 5
    return min(s, 99)

def status_leada(score):
    if score >= 80: return "HOT"
    elif score >= 60: return "WARM"
    else: return "COLD"

def analiza_claude(f, branza, ak, wer, score):
    if not ak:
        return {"problem": "Brak klucza API", "sms": "Dzien dobry!", "call": "Dzien dobry!", "email_temat": "Wspolpraca", "email_tresc": "Dzien dobry", "followup1": "Followup", "followup2": "Ostatni", "szansa": 40}
    try:
        prob_str = ", ".join(wer["problemy"]) if wer["problemy"] else "brak"
        prompt = "Firma: " + f["nazwa"] + ", branza: " + branza + ", WWW ocena: " + str(wer["ocena_www"]) + "/10, opinie: " + str(f["opinie"]) + ", problemy: " + prob_str + ". JSON: {\"problem\": \"max 10 slow\", \"sms\": \"SMS 160 znakow\", \"call\": \"3 zdania\", \"email_temat\": \"max 8 slow\", \"email_tresc\": \"5 zdan\", \"followup1\": \"2 zdania\", \"followup2\": \"2 zdania\", \"szansa\": liczba}"
        r = requests.post("https://api.anthropic.com/v1/messages", headers={"x-api-key": ak, "anthropic-version": "2023-06-01", "content-type": "application/json"}, json={"model": "claude-haiku-4-5", "max_tokens": 600, "messages": [{"role": "user", "content": prompt}]}, timeout=20)
        t = r.json()["content"][0]["text"]
        return json.loads(t[t.find("{"):t.rfind("}")+1])
    except:
        return {"problem": "Blad", "sms": "Dzien dobry!", "call": "Dzien dobry!", "email_temat": "Wspolpraca", "email_tresc": "Dzien dobry", "followup1": "Followup", "followup2": "Ostatni", "szansa": 40}

def generuj_b2c(produkt, problem, lok, ak):
    if not ak:
        return [problem + " " + lok, "gdzie kupic " + produkt, produkt + " opinie", "jak rozwiazac " + problem, produkt + " najtaniej"]
    try:
        r = requests.post("https://api.anthropic.com/v1/messages", headers={"x-api-key": ak, "anthropic-version": "2023-06-01", "content-type": "application/json"}, json={"model": "claude-haiku-4-5", "max_tokens": 200, "messages": [{"role": "user", "content": "Produkt: " + produkt + ". Problem: " + problem + ". Lokalizacja: " + lok + ". 5 zapytan Google oddzielonych srednikiem."}]}, timeout=15)
        t = r.json()["content"][0]["text"]
        return [z.strip() for z in t.split(";") if z.strip()][:5]
    except:
        return [problem + " " + lok, produkt + " gdzie kupic"]

def szukaj_b2c(q, sk):
    try:
        r = requests.post("https://google.serper.dev/search", headers={"X-API-KEY": sk, "Content-Type": "application/json"}, json={"q": q, "gl": "pl", "hl": "pl", "num": 10}, timeout=12)
        wyniki = []
        for p in r.json().get("organic",[]):
            u = p.get("link","").lower()
            if "facebook.com/groups" in u: typ = "Grupa FB"
            elif "facebook.com" in u: typ = "Facebook"
            elif "instagram.com" in u: typ = "Instagram"
            elif "allegro" in u: typ = "Allegro"
            elif "olx.pl" in u: typ = "OLX"
            elif "forum" in u: typ = "Forum"
            elif "youtube.com" in u: typ = "YouTube"
            else: typ = "Strona WWW"
            wyniki.append({"typ": typ, "zrodlo": p.get("title","?"), "opis": p.get("snippet","")[:200], "link": p.get("link","")})
        return wyniki
    except:
        return []

def analiza_b2c(produkt, problem, wyniki, ak):
    if not ak:
        return {"gdzie_sa_klienci": "Grupy Facebook, fora tematyczne, OLX", "jak_dotrzec": "Meta Ads targetowane, posty w grupach", "hook_reklamowy": "Masz problem z " + problem + "? Mamy rozwiazanie!", "opis_klienta": "Osoba szukajaca: " + problem, "kanaly_priorytet": "1. Meta Ads  2. Grupy FB  3. TikTok", "cta": "Zamow " + produkt + " z darmowa dostawa"}
    try:
        zr = "\n".join(["- " + w["typ"] + ": " + w["zrodlo"] for w in wyniki[:8]])
        r = requests.post("https://api.anthropic.com/v1/messages", headers={"x-api-key": ak, "anthropic-version": "2023-06-01", "content-type": "application/json"}, json={"model": "claude-haiku-4-5", "max_tokens": 500, "messages": [{"role": "user", "content": "Produkt: " + produkt + "\nProblem: " + problem + "\nZrodla:\n" + zr + "\nJSON: {\"gdzie_sa_klienci\": \"2-3 zdania\", \"jak_dotrzec\": \"3 zdania\", \"hook_reklamowy\": \"1 zdanie\", \"opis_klienta\": \"2 zdania\", \"kanaly_priorytet\": \"lista top 3 jako string np. 1. Meta Ads 2. Grupy FB 3. TikTok\", \"cta\": \"max 15 slow\"}"}]}, timeout=20)
        t = r.json()["content"][0]["text"]
        wynik = json.loads(t[t.find("{"):t.rfind("}")+1])
        kp = wynik.get("kanaly_priorytet", "")
        if isinstance(kp, list):
            wynik["kanaly_priorytet"] = " | ".join([str(x) for x in kp])
        return wynik
    except:
        return {"gdzie_sa_klienci": "Blad", "jak_dotrzec": "Blad", "hook_reklamowy": "Blad", "opis_klienta": "Blad", "kanaly_priorytet": "Blad", "cta": "Blad"}

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("## Konfiguracja")
    st.markdown("---")
    if TRYB_PROD:
        st.markdown('<span class="prod-badge">✅ TRYB PRODUKCJA</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("Klucze API aktywne. Mozesz skanowac!")
        ak = AK_SECRET
        sk_key = SK_SECRET
    else:
        st.markdown('<span class="dev-badge">🔧 TRYB DEWELOPERSKI</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        ak = st.text_input("Klucz Anthropic API", type="password", placeholder="sk-ant-api03-...")
        sk_key = st.text_input("Klucz Serper API", type="password", placeholder="z serper.dev...")
        c1, c2 = st.columns(2)
        with c1: st.markdown("Claude: " + ("OK" if ak else "BRAK"))
        with c2: st.markdown("Serper: " + ("OK" if sk_key else "BRAK"))
    st.markdown("---")
    st.markdown("### Ustawienia B2B")
    tryb_skanu = st.radio("Tryb skanu", ["Szybki (1 zapytanie)", "Sredni (3 zapytania)", "Masowy (6 zapytan AUTO)"])
    mf = st.slider("Max firm per zapytanie", 5, 20, 10)
    zrodla = st.multiselect("Zrodla", ["Google Maps", "Google Web"], default=["Google Maps"])
    st.markdown("---")
    st.markdown("### Filtry")
    bw = st.checkbox("Tylko BEZ strony WWW")
    bt = st.checkbox("Tylko Z telefonem", value=True)
    wykl = st.checkbox("Wykluczaj sieciowki", value=True)
    weryfikuj = st.checkbox("Weryfikuj strony WWW", value=True)
    min_score = st.slider("Min AI Score", 0, 99, 45)
    mo = st.slider("Maks opinii", 10, 500, 200)
    min_op = st.slider("Min opinii", 0, 100, 0)
    sort = st.radio("Sortuj po", ["AI Score", "Najmniej opinii", "Najslabsza WWW"])
    st.markdown("---")
    st.markdown("### Tryb lokalizacji")
    tryb_lok = st.radio("Wybierz tryb", ["Konkretne miasto", "Gmina / Powiat", "Wojewodztwo", "Kod pocztowy"])
    if st.session_state.historia:
        st.markdown("---")
        st.markdown("### Historia")
        for h in reversed(st.session_state.historia[-5:]):
            st.markdown("- **" + h["branza"] + "** / " + h["lok"] + " -> " + str(h["wyniki"]) + " (" + h["czas"] + ")")

c1h, c2h = st.columns([3,1])
with c1h:
    st.markdown('<div class="app-title">AI Lead Gen <span class="accent">PRO</span></div><div class="app-sub">Automatyczny skaner B2B + B2C - Analiza problemow - Gotowe skrypty - Sekwencje follow-up</div>', unsafe_allow_html=True)
with c2h:
    badge = '<span class="prod-badge">v2.2 LIVE</span>' if TRYB_PROD else '<span class="dev-badge">v2.2 DEV</span>'
    st.markdown('<div style="text-align:right;padding-top:.5rem">' + badge + '</div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

mc1, mc2, _ = st.columns([1.3, 1.5, 3])
with mc1:
    if st.button("B2B - Sprzedaje uslugi firmom", type="primary" if st.session_state.tryb_modulu=="B2B" else "secondary", use_container_width=True):
        st.session_state.tryb_modulu = "B2B"
        st.rerun()
with mc2:
    if st.button("B2C - Szukam kupujacych produkt", type="primary" if st.session_state.tryb_modulu=="B2C" else "secondary", use_container_width=True):
        st.session_state.tryb_modulu = "B2C"
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

if st.session_state.tryb_modulu == "B2B":
    st.markdown('<div class="section-header">B2B - Znajdz lokalne firmy ktore potrzebuja Twoich uslug</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        branza = st.text_input("Branza / Nisza", placeholder="np. Dekarz, Salon urody, Fotograf...")
    with col2:
        lok = ""
        if tryb_lok == "Konkretne miasto":
            lok = st.text_input("Miasto", placeholder="np. Warszawa, Krakow...")
        elif tryb_lok == "Gmina / Powiat":
            lok = st.text_input("Gmina / Powiat", placeholder="np. Gmina Piaseczno...")
        elif tryb_lok == "Wojewodztwo":
            lok = "woj. " + st.selectbox("Wojewodztwo", WOJEWODZTWA)
        else:
            kc1, kc2 = st.columns(2)
            with kc1: kp = st.text_input("Kod pocztowy", placeholder="02-001")
            with kc2: pr = st.selectbox("Promien", ["5 km","10 km","25 km","50 km"])
            lok = kp + " (+" + pr + ")"
    st.markdown("<br>", unsafe_allow_html=True)
    _, bc, _ = st.columns([1,2,1])
    with bc:
        go_b2b = st.button("URUCHOM MASOWY SKAN B2B", type="primary", use_container_width=True)
    if go_b2b:
        if not branza.strip(): st.error("Wpisz branze!"); st.stop()
        if not sk_key: st.error("Brak klucza Serper API!"); st.stop()
        bar = st.progress(0); msg = st.empty(); stats_box = st.empty()
        wszystkie = []; widziane = set()
        msg.info("Generuje zapytania...")
        bar.progress(5)
        zapytania = generuj_zapytania_b2b(branza, lok, ak, tryb_skanu)
        for i, zap in enumerate(zapytania):
            bar.progress(int(10 + 35 * i / len(zapytania)))
            msg.info("Skanuje (" + str(i+1) + "/" + str(len(zapytania)) + "): " + zap)
            if "Google Maps" in zrodla:
                for f in szukaj_maps(zap, sk_key, mf):
                    k2 = f["nazwa"].lower().strip()
                    if k2 not in widziane: widziane.add(k2); wszystkie.append(f)
            if "Google Web" in zrodla:
                for f in szukaj_web(zap, sk_key, mf):
                    k2 = f["nazwa"].lower().strip()
                    if k2 not in widziane: widziane.add(k2); wszystkie.append(f)
            stats_box.info("Zebrano " + str(len(wszystkie)) + " firm...")
        bar.progress(50)
        msg.info("Weryfikuje i analizuje " + str(len(wszystkie)) + " firm...")
        rows = []
        for i, f in enumerate(wszystkie):
            if wykl and jest_sieciowka(f["nazwa"]): continue
            if bw and f["www"] not in ["brak","sprawdz na stronie",""]: continue
            if bt and f["telefon"] in ["brak","","sprawdz na stronie"]: continue
            if f["opinie"] > mo: continue
            if f["opinie"] < min_op: continue
            bar.progress(50 + int(40 * i / max(len(wszystkie),1)))
            msg.info("Analizuje (" + str(i+1) + "/" + str(len(wszystkie)) + "): " + f["nazwa"])
            wer = weryfikuj_strone(f["www"]) if weryfikuj else {"dziala": True, "ssl": False, "ocena_www": 5, "problemy": [], "ma_rezerwacje": False, "ma_social": False}
            score = oblicz_score(f, wer)
            if score < min_score: continue
            ai = analiza_claude(f, branza, ak, wer, score)
            st_label = status_leada(score)
            rows.append({"Status": st_label, "Nazwa": f["nazwa"], "Telefon": f["telefon"], "WWW": f["www"], "Adres": f["adres"], "Opinie": f["opinie"], "Ocena Google": f["ocena"], "Ocena strony": wer["ocena_www"], "SSL": "TAK" if wer["ssl"] else "NIE", "Rezerwacja": "TAK" if wer["ma_rezerwacje"] else "NIE", "Problemy WWW": " | ".join(wer["problemy"]) if wer["problemy"] else "OK", "AI Score": score, "Szansa %": ai.get("szansa",50), "Problem": ai.get("problem",""), "SMS": ai.get("sms",""), "Call": ai.get("call",""), "Email temat": ai.get("email_temat",""), "Email tresc": ai.get("email_tresc",""), "Followup 1": ai.get("followup1",""), "Followup 2": ai.get("followup2","")})
        bar.progress(100); msg.empty(); stats_box.empty(); bar.empty()
        if not rows: st.warning("Brak wynikow. Zmien filtry."); st.stop()
        df = pd.DataFrame(rows)
        if sort == "AI Score": df = df.sort_values("AI Score", ascending=False)
        elif sort == "Najmniej opinii": df = df.sort_values("Opinie", ascending=True)
        else: df = df.sort_values("Ocena strony", ascending=True)
        df = df.reset_index(drop=True)
        st.session_state.historia.append({"branza": branza, "lok": lok, "wyniki": len(df), "czas": datetime.now().strftime("%H:%M")})
        hot = len(df[df["Status"]=="HOT"]); warm = len(df[df["Status"]=="WARM"])
        bez_www = len(df[df["WWW"].isin(["brak","sprawdz na stronie",""])]); sr_score = int(df["AI Score"].mean())
        st.success("Znaleziono " + str(len(df)) + " firm | " + branza + " | " + lok)
        st.markdown("<br>", unsafe_allow_html=True)
        k1,k2,k3,k4,k5 = st.columns(5)
        k1.markdown('<div class="kpi-card"><div class="kpi-val">' + str(len(df)) + '</div><div class="kpi-label">Firm lacznie</div></div>', unsafe_allow_html=True)
        k2.markdown('<div class="kpi-card"><div class="kpi-val kpi-val-red">' + str(hot) + '</div><div class="kpi-label">HOT leads</div></div>', unsafe_allow_html=True)
        k3.markdown('<div class="kpi-card"><div class="kpi-val kpi-val-orange">' + str(warm) + '</div><div class="kpi-label">WARM leads</div></div>', unsafe_allow_html=True)
        k4.markdown('<div class="kpi-card"><div class="kpi-val kpi-val-red">' + str(bez_www) + '</div><div class="kpi-label">Bez WWW</div></div>', unsafe_allow_html=True)
        k5.markdown('<div class="kpi-card"><div class="kpi-val kpi-val-purple">' + str(sr_score) + '</div><div class="kpi-label">Sr Score</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(["Tabela wynikow","SMS / Cold Call","Sekwencja Email","TOP 5","Analiza","Eksport"])
        with tab1:
            st.dataframe(df[["Status","Nazwa","Telefon","WWW","Opinie","Ocena Google","Ocena strony","SSL","Rezerwacja","AI Score","Szansa %","Problem","Problemy WWW"]], use_container_width=True, hide_index=True, column_config={"AI Score": st.column_config.ProgressColumn("AI Score", min_value=0, max_value=99, format="%d/99"), "Ocena strony": st.column_config.ProgressColumn("Ocena strony", min_value=0, max_value=10, format="%d/10"), "Szansa %": st.column_config.ProgressColumn("Szansa %", min_value=0, max_value=100, format="%d%%")})
        with tab2:
            st.markdown('<div class="info-box">Gotowe skrypty SMS i Cold Call dla kazdej firmy.</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            for _, row in df.head(25).iterrows():
                with st.expander(row["Status"] + " | " + row["Nazwa"] + " - " + row["Telefon"] + " | Score: " + str(row["AI Score"]) + "/99"):
                    ca, cb = st.columns(2)
                    with ca: st.markdown("**SMS:**"); st.info(row["SMS"]); st.caption("Problem: " + row["Problem"])
                    with cb: st.markdown("**Cold Call:**"); st.success(row["Call"])
        with tab3:
            st.markdown('<div class="info-box">Sekwencja 3 wiadomosci: Email + Follow-up dzien 3 + Follow-up dzien 7.</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            for _, row in df.head(25).iterrows():
                with st.expander(row["Status"] + " | " + row["Nazwa"] + " | Score: " + str(row["AI Score"]) + "/99"):
                    st.markdown("**Email - Temat: " + row["Email temat"] + "**"); st.warning(row["Email tresc"])
                    st.markdown("**Follow-up 1 (dzien 3):**"); st.info(row["Followup 1"])
                    st.markdown("**Follow-up 2 (dzien 7):**"); st.error(row["Followup 2"])
        with tab4:
            st.markdown("### TOP 5 Leadow do kontaktu TERAZ")
            top5 = df[df["Status"]=="HOT"].head(5) if len(df[df["Status"]=="HOT"]) >= 3 else df.head(5)
            for _, row in top5.iterrows():
                ta, tb, tc = st.columns([1,1,2])
                with ta: st.markdown("**" + row["Nazwa"] + "**"); st.markdown("Tel: `" + row["Telefon"] + "`"); st.markdown("WWW: " + row["WWW"])
                with tb: st.markdown("Opinie: " + str(row["Opinie"])); st.markdown("Score: **" + str(row["AI Score"]) + "/99**"); st.caption(row["Problem"])
                with tc: st.info("SMS: " + row["SMS"])
                st.markdown("<hr>", unsafe_allow_html=True)
        with tab5:
            st.markdown("### Analiza danych")
            ta, tb, tc = st.columns(3)
            with ta:
                st.markdown("**Rozklad statusow:**")
                for s,c in df["Status"].value_counts().items(): st.markdown("- " + str(s) + ": **" + str(c) + "** firm")
            with tb:
                st.markdown("**Najczestsze problemy:**")
                ap = []
                for p in df["Problemy WWW"]: ap.extend([x.strip() for x in str(p).split("|") if x.strip() and x.strip() != "OK"])
                for p,c in pd.Series(ap).value_counts().head(6).items(): st.markdown("- " + str(p) + ": **" + str(c) + "x**")
            with tc:
                st.markdown("**Statystyki:**")
                st.markdown("- Bez WWW: **" + str(bez_www) + "**")
                st.markdown("- Sr score: **" + str(sr_score) + "/99**")
                st.markdown("- HOT: **" + str(hot) + "**, WARM: **" + str(warm) + "**")
        with tab6:
            ec1, ec2 = st.columns(2)
            with ec1: st.download_button("Pobierz pelna baze CSV", df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"), file_name="leady_B2B_" + branza + ".csv", mime="text/csv", use_container_width=True)
            with ec2:
                df_hw = df[df["Status"].isin(["HOT","WARM"])]
                st.download_button("Pobierz tylko HOT + WARM", df_hw.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"), file_name="HOT_WARM_" + branza + ".csv", mime="text/csv", use_container_width=True)

else:
    st.markdown('<div class="section-header">B2C - Znajdz kupujacych Twoj produkt lub usluge</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Analizuje gdzie sa ludzie szukajacy rozwiazania problemu ktory Twoj produkt rozwiazuje.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    bc1, bc2 = st.columns(2)
    with bc1:
        produkt_b2c = st.text_input("Twoj produkt / usluga", placeholder="np. Poduszka ortopedyczna, Kurs gotowania...")
        problem_b2c = st.text_input("Problem klienta ktory rozwiazujesz", placeholder="np. Bol plecow, Brak czasu...")
    with bc2:
        lok_b2c = st.text_input("Lokalizacja (lub Polska)", placeholder="np. Warszawa, Polska...")
        grupa = st.selectbox("Grupa docelowa", ["Wszyscy","Kobiety 25-35","Kobiety 35-50","Mamy z dziecmi","Seniorzy 60+","Mezczyzni 25-45","Przedsiebiorcy","Studenci"])
    st.markdown("<br>", unsafe_allow_html=True)
    _, bbc, _ = st.columns([1,2,1])
    with bbc:
        go_b2c = st.button("URUCHOM SKAN B2C - Znajdz moich klientow", type="primary", use_container_width=True)
    if go_b2c:
        if not produkt_b2c.strip() or not problem_b2c.strip(): st.error("Wpisz produkt i problem!"); st.stop()
        if not sk_key: st.error("Brak klucza Serper API!"); st.stop()
        bar2 = st.progress(0); msg2 = st.empty()
        msg2.info("Claude analizuje gdzie sa Twoi klienci...")
        bar2.progress(10)
        zapytania_b2c = generuj_b2c(produkt_b2c, problem_b2c, lok_b2c, ak)
        wyniki_b2c = []; seen = set()
        for i, zap in enumerate(zapytania_b2c):
            bar2.progress(15 + int(35 * i / len(zapytania_b2c)))
            msg2.info("Szukam (" + str(i+1) + "/" + str(len(zapytania_b2c)) + "): " + zap)
            for w in szukaj_b2c(zap, sk_key):
                if w["link"] not in seen: seen.add(w["link"]); wyniki_b2c.append(w)
        bar2.progress(65); msg2.info("Claude tworzy strategie...")
        analiza = analiza_b2c(produkt_b2c, problem_b2c, wyniki_b2c, ak)
        bar2.progress(100); msg2.empty(); bar2.empty()
        st.success("Analiza gotowa! Znaleziono " + str(len(wyniki_b2c)) + " zrodel.")
        st.markdown("<br>", unsafe_allow_html=True)
        rc1, rc2 = st.columns(2)
        with rc1:
            st.markdown("### Profil idealnego klienta")
            st.markdown('<div class="info-box"><b>Kim jest?</b><br>' + str(analiza.get("opis_klienta","")) + '</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="info-box"><b>Gdzie go znalezc?</b><br>' + str(analiza.get("gdzie_sa_klienci","")) + '</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            kp_val = analiza.get("kanaly_priorytet","")
            if isinstance(kp_val, list): kp_val = " | ".join([str(x) for x in kp_val])
            st.markdown('<div class="info-box"><b>Priorytetowe kanaly:</b><br>' + str(kp_val) + '</div>', unsafe_allow_html=True)
        with rc2:
            st.markdown("### Strategia dotarcia")
            st.markdown('<div class="info-box"><b>Jak dotrzec?</b><br>' + str(analiza.get("jak_dotrzec","")) + '</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Haczyk reklamowy:**"); st.warning(str(analiza.get("hook_reklamowy","")))
            st.markdown("**Call to Action:**"); st.success(str(analiza.get("cta","")))
        st.markdown("<hr>", unsafe_allow_html=True)
        if wyniki_b2c:
            df_b2c = pd.DataFrame(wyniki_b2c)
            tb1, tb2 = st.tabs(["Tabela zrodel","Eksport"])
            with tb1:
                st.dataframe(df_b2c[["typ","zrodlo","opis","link"]], use_container_width=True, hide_index=True, column_config={"link": st.column_config.LinkColumn("Link"), "opis": st.column_config.TextColumn("Opis", width="large")})
            with tb2:
                st.download_button("Pobierz zrodla CSV", df_b2c.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"), file_name="b2c_" + produkt_b2c + ".csv", mime="text/csv", use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div style="text-align:center;font-size:.72rem;color:#cbd5e1">AI Lead Gen PRO v2.2 - B2B + B2C - Powered by Claude AI + Serper.dev</div>', unsafe_allow_html=True)
