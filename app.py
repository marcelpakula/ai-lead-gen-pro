import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, date

st.set_page_config(page_title="AI Lead Gen PRO", layout="wide", page_icon="🔥")

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
.stTabs [data-baseweb="tab-list"] { background: #f1f5f9 !important; border-radius: 10px !important; padding: 4px !important; }
.stTabs [aria-selected="true"] { background: #ffffff !important; color: #2563eb !important; font-weight: 700 !important; border-radius: 8px !important; }
.stProgress > div > div { background: linear-gradient(90deg, #2563eb, #7c3aed) !important; border-radius: 10px !important; }
.kpi-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 1.3rem 1.5rem; text-align: center; box-shadow: 0 1px 6px rgba(0,0,0,0.06); }
.kpi-val { font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 700; color: #2563eb; }
.kpi-val-red { color: #dc2626 !important; }
.kpi-val-orange { color: #d97706 !important; }
.kpi-val-purple { color: #7c3aed !important; }
.kpi-val-green { color: #16a34a !important; }
.kpi-label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.4rem; font-weight: 600; }
.info-box { background: #eff6ff; border: 1px solid #bfdbfe; border-left: 3px solid #2563eb; border-radius: 8px; padding: 0.9rem 1.1rem; font-size: 0.85rem; color: #1d4ed8; line-height: 1.6; }
.warning-box { background: #fff7ed; border: 1px solid #fed7aa; border-left: 3px solid #ea580c; border-radius: 8px; padding: 0.9rem 1.1rem; font-size: 0.85rem; color: #9a3412; line-height: 1.6; }
.success-box { background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 3px solid #16a34a; border-radius: 8px; padding: 0.9rem 1.1rem; font-size: 0.85rem; color: #14532d; line-height: 1.6; }
.insight-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.insight-title { font-weight: 700; color: #0f172a; font-size: 0.9rem; margin-bottom: 0.4rem; }
.insight-text { color: #475569; font-size: 0.85rem; line-height: 1.6; }
.quote-card { background: #fafafa; border-left: 3px solid #7c3aed; border-radius: 0 8px 8px 0; padding: 0.8rem 1rem; margin-bottom: 0.6rem; font-style: italic; color: #374151; font-size: 0.85rem; }
.competitor-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.8rem; }
.competitor-card-global { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.ads-card { background: linear-gradient(135deg, #eff6ff 0%, #f5f3ff 100%); border: 1px solid #c7d2fe; border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 1rem; }
.ads-headline { font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; font-weight: 700; color: #1e40af; margin-bottom: 0.5rem; }
.place-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.8rem; }
.place-type { background: #eff6ff; color: #2563eb; border-radius: 20px; padding: 2px 10px; font-size: 0.72rem; font-weight: 700; white-space: nowrap; }
.better-tag { background: #f0fdf4; color: #16a34a; border-radius: 20px; padding: 2px 10px; font-size: 0.72rem; font-weight: 700; white-space: nowrap; border: 1px solid #bbf7d0; }
.worse-tag { background: #fff7ed; color: #ea580c; border-radius: 20px; padding: 2px 10px; font-size: 0.72rem; font-weight: 700; white-space: nowrap; border: 1px solid #fed7aa; }
.app-title { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: #0f172a; letter-spacing: -0.02em; }
.accent { color: #2563eb; }
.app-sub { font-size: 0.88rem; color: #94a3b8; margin-top: 0.3rem; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.2rem 0; }
.section-header { font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 700; color: #1e293b; margin-bottom: 1rem; }
.login-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; padding: 3rem 2.5rem; max-width: 460px; margin: 4rem auto; box-shadow: 0 4px 24px rgba(0,0,0,0.08); text-align: center; }
.skany-bar { background: #f1f5f9; border-radius: 10px; padding: 0.7rem 1rem; font-size: 0.8rem; color: #475569; text-align: center; margin-top: 0.5rem; }
.action-item { background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 3px solid #16a34a; border-radius: 0 8px 8px 0; padding: 8px 12px; margin-bottom: 6px; font-size: .85rem; color: #14532d; }
</style>
""", unsafe_allow_html=True)

def get_sheet_config():
    try:
        return st.secrets["SHEETS_API_URL"], st.secrets["SHEETS_API_TOKEN"]
    except:
        return None, None

def get_keys():
    try:
        return st.secrets["ANTHROPIC_API_KEY"], st.secrets["SERPER_API_KEY"]
    except:
        return None, None

AK, SK = get_keys()

WOJEWODZTWA = ["Dolnoslaskie","Kujawsko-Pomorskie","Lubelskie","Lubuskie","Lodzkie","Malopolskie","Mazowieckie","Opolskie","Podkarpackie","Podlaskie","Pomorskie","Slaskie","Swietokrzyskie","Warminsko-Mazurskie","Wielkopolskie","Zachodniopomorskie"]
SIECIOWKI = ["mcdonald","kfc","burger king","biedronka","lidl","zabka","orlen","bp","shell","ikea","media markt","rossmann","douglas","reserved","h&m","zara","deichmann","pepco","action","neonet","decathlon","leroy merlin","castorama","obi ","jysk","empik"]

# ── GOOGLE SHEETS (Apps Script Web App) — baza kodow z odczytem i zapisem ──
def weryfikuj_kod(kod_input):
    url, token = get_sheet_config()
    if not url or not token:
        return False, "Brak konfiguracji bazy kodow (SHEETS_API_URL/SHEETS_API_TOKEN).", None
    try:
        resp = requests.get(url, params={"token": token, "kod": kod_input.upper()}, timeout=15)
        row = resp.json()
    except Exception as e:
        return False, f"Blad polaczenia z baza kodow: {str(e)[:120]}", None

    if row.get("error") == "not_found":
        return False, "Nieprawidlowy kod dostepu.", None
    if row.get("error"):
        return False, f"Blad bazy kodow: {row.get('error')}", None

    if str(row.get("aktywny","")).upper() != "TAK":
        return False, "Ten kod zostal dezaktywowany.", None
    try:
        data_wygasniecia = datetime.strptime(str(row["data_wygasniecia"]), "%Y-%m-%d").date()
        if date.today() > data_wygasniecia:
            return False, f"Kod wygasl {data_wygasniecia}.", None
    except:
        pass
    skany_wykorzystane = int(row.get("skany_wykorzystane", 0) or 0)
    max_skanow = int(row.get("max_skanow", 50) or 50)
    if skany_wykorzystane >= max_skanow:
        return False, f"Wykorzystales wszystkie skany ({max_skanow}/{max_skanow}).", None
    return True, "OK", {
        "kod": str(row["kod"]),
        "wiersz": row["_row"],
        "skany_wykorzystane": skany_wykorzystane,
        "max_skanow": max_skanow,
        "pozostalo": max_skanow - skany_wykorzystane,
        "data_wygasniecia": str(row.get("data_wygasniecia", ""))
    }

def zapisz_skan(kod_info):
    """Zwieksza licznik skanow w arkuszu o 1 — trwale, dla wszystkich sesji."""
    url, token = get_sheet_config()
    if not url or not token:
        return False
    try:
        resp = requests.post(url, json={
            "token": token,
            "row": kod_info["wiersz"],
            "value": kod_info["skany_wykorzystane"] + 1
        }, timeout=15)
        return resp.json().get("ok", False)
    except Exception:
        return False

if "zalogowany" not in st.session_state: st.session_state.zalogowany = False
if "kod_info" not in st.session_state: st.session_state.kod_info = None
if "historia" not in st.session_state: st.session_state.historia = []
if "tryb_modulu" not in st.session_state: st.session_state.tryb_modulu = "B2B"

if not st.session_state.zalogowany:
    st.markdown('<div class="login-card"><div style="font-family:Space Grotesk,sans-serif;font-size:1.8rem;font-weight:700;color:#0f172a;margin-bottom:.5rem">🔥 AI Lead Gen PRO</div><div style="font-size:.9rem;color:#94a3b8;margin-bottom:2rem">Automatyczny skaner B2B + B2C z analizą Claude AI<br>Wpisz swój kod dostępu aby kontynuować</div></div>', unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        kod_input = st.text_input("Kod dostępu", placeholder="np. BETA2026").strip().upper()
        if st.button("🔓 ZALOGUJ SIĘ", type="primary", use_container_width=True):
            if not kod_input:
                st.error("Wpisz kod dostępu!")
            else:
                with st.spinner("Weryfikuję..."):
                    ok, komunikat, info = weryfikuj_kod(kod_input)
                if ok:
                    st.session_state.zalogowany = True
                    st.session_state.kod_info = info
                    st.rerun()
                else:
                    st.error(f"❌ {komunikat}")
        st.markdown('<div style="text-align:center;font-size:.8rem;color:#94a3b8;margin-top:1rem">Nie masz kodu? <a href="#" style="color:#2563eb">Kup dostęp za 97 zł/miesiąc</a></div>', unsafe_allow_html=True)
    st.stop()

info = st.session_state.kod_info
pozostalo = info["pozostalo"]

# ── HELPER: bezpieczny parser JSON ──
def safe_parse_json(text):
    """Wyciąga JSON z tekstu nawet jeśli Claude dodał komentarz przed/po albo odpowiedź zostala ucieta."""
    import re
    text = text.strip()
    start = text.find("{")
    if start == -1:
        return None
    end = text.rfind("}")
    candidate = text[start:end+1] if end > start else text[start:]
    try:
        return json.loads(candidate)
    except:
        pass

    # Próba naprawy — usuń znaki kontrolne
    candidate_clean = re.sub(r'[\x00-\x1f\x7f]', ' ', candidate)
    try:
        return json.loads(candidate_clean)
    except:
        pass

    # Próba naprawy uciętego JSON-a: obetnij do ostatniego bezpiecznego przecinka
    # poza stringami i dodomknij wszystkie otwarte nawiasy
    raw = text[start:]
    stack = []
    in_str = False
    esc = False
    last_safe = -1
    for i, ch in enumerate(raw):
        if esc:
            esc = False
            continue
        if ch == '\\' and in_str:
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch in '{[':
            stack.append(ch)
        elif ch in '}]':
            if stack: stack.pop()
        if ch == ',':
            last_safe = i

    if not stack or last_safe == -1:
        return None
    repaired = raw[:last_safe] + ''.join('}' if c == '{' else ']' for c in reversed(stack))
    try:
        return json.loads(repaired)
    except:
        return None

# ── HELPER: wywołanie Claude z systemowym promptem ──
def claude_call(system_prompt, user_prompt, ak, max_tokens=800, model="claude-haiku-4-5"):
    """Wywołuje Claude API z system promptem wymuszającym czysty JSON."""
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": ak, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        json={
            "model": model,
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        },
        timeout=90
    )
    r.raise_for_status()
    return r.json()["content"][0]["text"]

# ── FUNKCJE B2B ──
def generuj_zapytania_b2b(branza, lok, ak, tryb):
    if tryb == "Szybki (1 zapytanie)": return [branza + " " + lok]
    elif tryb == "Sredni (3 zapytania)": return [branza + " " + lok, "uslugi " + branza + " " + lok, branza + " " + lok + " tani"]
    if not ak: return [branza + " " + lok, "uslugi " + branza + " " + lok]
    try:
        tekst = claude_call(
            "Odpowiadasz TYLKO listą zapytań oddzielonych średnikiem. Bez żadnego innego tekstu.",
            f"Wygeneruj 6 różnych zapytań Google Maps dla branży: {branza} w lokalizacji: {lok}. TYLKO zapytania oddzielone średnikiem.",
            ak, 200
        )
        return [z.strip() for z in tekst.split(";") if z.strip()][:6]
    except:
        return [branza + " " + lok, "uslugi " + branza + " " + lok]

def jest_sieciowka(nazwa): return any(s in nazwa.lower() for s in SIECIOWKI)

def szukaj_maps(q, sk, limit=10):
    try:
        r = requests.post("https://google.serper.dev/maps", headers={"X-API-KEY": sk, "Content-Type": "application/json"}, json={"q": q, "gl": "pl", "hl": "pl", "num": limit}, timeout=12)
        return [{"nazwa": p.get("title","?"), "telefon": p.get("phoneNumber","brak"), "www": p.get("website","brak"), "opinie": p.get("ratingCount",0), "ocena": p.get("rating",0), "adres": p.get("address","?"), "kategoria": p.get("category","")} for p in r.json().get("places",[])]
    except: return []

def szukaj_web(q, sk, limit=10):
    try:
        r = requests.post("https://google.serper.dev/search", headers={"X-API-KEY": sk, "Content-Type": "application/json"}, json={"q": q + " kontakt telefon", "gl": "pl", "hl": "pl", "num": limit}, timeout=12)
        return [{"nazwa": p.get("title","?"), "telefon": "sprawdz na stronie", "www": p.get("link","brak"), "opinie": 0, "ocena": 0, "adres": p.get("snippet","")[:100], "kategoria": ""} for p in r.json().get("organic",[])]
    except: return []

def weryfikuj_strone(url):
    if not url or url in ["brak","sprawdz na stronie",""]: return {"dziala": False, "ssl": False, "ocena_www": 0, "problemy": ["Brak strony WWW"], "ma_rezerwacje": False, "ma_social": False}
    try:
        r = requests.get(url, timeout=7, headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"}, allow_redirects=True)
        ssl = url.startswith("https"); t = r.text.lower(); problemy = []
        if not ssl: problemy.append("Brak SSL")
        if "viewport" not in t: problemy.append("Brak mobile")
        if not any(x in t for x in ["form","kontakt","contact"]): problemy.append("Brak formularza")
        if not any(x in t for x in ["facebook","instagram","tiktok"]): problemy.append("Brak social media")
        if len(t) < 2000: problemy.append("Uboga tresc")
        if not any(x in t for x in ["cena","cennik","price"]): problemy.append("Brak cennika")
        ma_rez = any(x in t for x in ["booksy","calendly","rezerwacja","booking"])
        if not ma_rez: problemy.append("Brak rezerwacji online")
        return {"dziala": True, "ssl": ssl, "ocena_www": max(1, 10-len(problemy)), "problemy": problemy, "ma_rezerwacje": ma_rez, "ma_social": any(x in t for x in ["facebook","instagram","tiktok"])}
    except: return {"dziala": False, "ssl": False, "ocena_www": 0, "problemy": ["Strona niedostepna"], "ma_rezerwacje": False, "ma_social": False}

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

def analiza_claude_b2b(f, branza, ak, wer, score):
    FALLBACK = {"problem": "Brak analizy AI", "sms": "Dzien dobry! Budujemy strony dla firm z branzy " + branza + ". Czy moge przedstawic oferte?", "call": "Dzien dobry, dzwonie w sprawie strony internetowej. Czy maja Panstwo chwile?", "email_temat": "Propozycja wspolpracy", "email_tresc": "Dzien dobry, chcielibysmy przedstawic oferte na strone WWW.", "followup1": "Czy mieli Panstwo okazje zapoznac sie z nasza oferta?", "followup2": "To ostatnia wiadomosc — czy moge pomoc?", "szansa": 50}
    if not ak: return FALLBACK
    try:
        prob_str = ", ".join(wer["problemy"]) if wer["problemy"] else "brak problemow"
        user_prompt = f"""Firma: {f["nazwa"]}
Branża: {branza}
Ocena WWW: {wer["ocena_www"]}/10
Liczba opinii: {f["opinie"]}
Problemy strony: {prob_str}

Zwróć JSON z polami: problem, sms, call, email_temat, email_tresc, followup1, followup2, szansa"""

        tekst = claude_call(
            'Jesteś ekspertem od cold outreach B2B. Odpowiadasz WYŁĄCZNIE czystym JSON bez żadnego tekstu przed ani po. Format: {"problem": "max 10 slow", "sms": "SMS do 160 znakow", "call": "3 zdania", "email_temat": "max 8 slow", "email_tresc": "5 zdan", "followup1": "2 zdania", "followup2": "2 zdania", "szansa": liczba_0_100}',
            user_prompt, ak, 500
        )
        wynik = safe_parse_json(tekst)
        if wynik is None: return FALLBACK
        # Uzupełnij brakujące klucze fallbackiem
        for k, v in FALLBACK.items():
            if k not in wynik or not wynik[k]:
                wynik[k] = v
        return wynik
    except:
        return FALLBACK

# ── FUNKCJE B2C ──
def serper_search(query, sk, num=10):
    try:
        r = requests.post("https://google.serper.dev/search", headers={"X-API-KEY": sk, "Content-Type": "application/json"}, json={"q": query, "gl": "pl", "hl": "pl", "num": num}, timeout=12)
        return r.json()
    except: return {}

def zbierz_dane_b2c(produkt, problem, lok, sk, msg_placeholder):
    dane = {"popyt": [], "glos_klienta": [], "konkurencja_globalna": [], "raw_snippets": []}

    msg_placeholder.info("🔍 Analizuję popyt rynkowy...")
    for q in [produkt + " polska", problem + " jak rozwiazac", produkt + " opinie", produkt + " gdzie kupic", problem + " forum"]:
        wynik = serper_search(q, sk, 5)
        for item in wynik.get("organic", []):
            dane["raw_snippets"].append({"zrodlo": item.get("title",""), "tresc": item.get("snippet",""), "link": item.get("link",""), "query": q})
        if wynik.get("relatedSearches"):
            for rs in wynik["relatedSearches"][:3]:
                dane["popyt"].append(rs.get("query",""))

    msg_placeholder.info("💬 Zbieram głos klienta z forów i recenzji...")
    for q in [produkt + " opinie forum", problem + " site:wizaz.pl OR site:kafeteria.pl OR site:forum.gazeta.pl", '"' + problem + '" co pomaga', produkt + " allegro opinie"]:
        wynik = serper_search(q, sk, 5)
        for item in wynik.get("organic", []):
            if any(x in item.get("link","").lower() for x in ["forum","opinie","allegro","olx","ceneo","reddit","wizaz","kafeteria"]):
                dane["glos_klienta"].append({"zrodlo": item.get("title",""), "cytat": item.get("snippet",""), "link": item.get("link","")})
            dane["raw_snippets"].append({"zrodlo": item.get("title",""), "tresc": item.get("snippet",""), "link": item.get("link",""), "query": q})

    msg_placeholder.info("🌍 Szukam globalnych konkurentów sprzedających ten produkt...")
    # Szukamy sklepów na całym świecie sprzedających ten sam produkt
    for q in [
        produkt + " buy online shop",
        produkt + " shopify store",
        produkt + " best seller amazon",
        produkt + " ecommerce site:shopify.com OR site:amazon.com OR site:etsy.com",
        "buy " + produkt + " site:.com",
        produkt + " reviews trustpilot",
        produkt + " sklep online najlepszy",
        produkt + " aliexpress OR amazon",
        produkt + " ranking najlepszych marek Polska",
        produkt + " lider rynku Polska",
    ]:
        wynik = serper_search(q, sk, 5)
        for item in wynik.get("organic", []):
            link = item.get("link","").lower()
            # Kategoryzuj typ sklepu
            if "shopify.com" in link or "myshopify" in link: typ = "Shopify"
            elif "amazon" in link: typ = "Amazon"
            elif "etsy" in link: typ = "Etsy"
            elif "aliexpress" in link: typ = "AliExpress"
            elif "ebay" in link: typ = "eBay"
            elif "allegro" in link: typ = "Allegro"
            elif "ceneo" in link or "opineo" in link or "trustpilot" in link: typ = "Recenzje"
            elif any(x in link for x in ["sklep","shop","store","buy","kup"]): typ = "Sklep online"
            else: typ = "Strona WWW"
            dane["konkurencja_globalna"].append({
                "typ": typ,
                "nazwa": item.get("title","")[:80],
                "opis": item.get("snippet","")[:200],
                "link": item.get("link","")
            })
            dane["raw_snippets"].append({"zrodlo": item.get("title",""), "tresc": item.get("snippet",""), "link": item.get("link",""), "query": q})

    return dane

def analiza_ai_b2c(produkt, problem, lok, grupa, budzet, dane, ak):
    FALLBACK = {
        "mapa_popytu": {"wielkosc": "Brak danych — dodaj klucz Anthropic API", "sezonowosc": "Brak danych", "slowa_kluczowe": ["brak"], "insight": "Dodaj klucz API w secrets"},
        "glos_klienta": {"glowny_bol": "Brak danych", "obawy": ["Dodaj klucz API"], "motywatory": ["Dodaj klucz API"], "cytaty": ["Dodaj klucz Anthropic API zeby zobaczyc analize"]},
        "mapa_konkurencji": {"gracze": ["Brak danych"], "slabe_strony": "Dodaj klucz API", "luka_rynkowa": "Dodaj klucz API"},
        "analiza_globalna": {"co_robia_dobrze": ["Brak danych"], "co_robia_zle": ["Brak danych"], "luka": "Brak danych", "jak_wygrac": ["Brak danych"]},
        "strategia": {"kanal_1": "Meta Ads", "kanal_1_opis": "Dodaj klucz API", "kanal_2": "Grupy FB", "kanal_2_opis": "Dodaj klucz API", "kanal_3": "TikTok", "kanal_3_opis": "Dodaj klucz API", "budzet_start": "Dodaj klucz API"},
        "meta_ads": [{"wariant": "Wariant 1", "headline": "Przykladowy naglowek", "primary": "Przykladowy tekst reklamy. Dodaj klucz Anthropic API.", "cta": "Kup teraz"}]
    }
    if not ak: return FALLBACK

    try:
        # Ogranicz dane do rozsądnej ilości żeby nie przekroczyć limitu tokenów
        snippets_str = "\n".join([f"- [{s['zrodlo'][:40]}]: {s['tresc'][:100]}" for s in dane["raw_snippets"][:25]])
        konkurencja_str = "\n".join([f"- [{k['typ']}] {k['nazwa'][:50]}: {k['opis'][:100]}" for k in dane["konkurencja_globalna"][:15]])

        user_prompt = f"""PRODUKT: {produkt}
PROBLEM KLIENTA: {problem}
RYNEK: {lok}
GRUPA: {grupa}
BUDZET MIESIECZNY NA REKLAMY: {budzet}

DANE Z INTERNETU (skrócone):
{snippets_str}

GLOBALNA KONKURENCJA ZNALEZIONA:
{konkurencja_str}"""

        system_prompt = """Jesteś ekspertem od marketingu cyfrowego. Odpowiadasz WYŁĄCZNIE czystym JSON — zero tekstu przed ani po, zero komentarzy, zero markdown.

Struktura JSON którą musisz zwrócić:
{
  "mapa_popytu": {
    "wielkosc": "string",
    "sezonowosc": "string",
    "slowa_kluczowe": ["string", "string", "string", "string", "string"],
    "insight": "string"
  },
  "glos_klienta": {
    "glowny_bol": "string",
    "obawy": ["string", "string", "string"],
    "motywatory": ["string", "string", "string"],
    "cytaty": ["string", "string", "string"]
  },
  "mapa_konkurencji": {
    "gracze": ["string", "string", "string"],
    "slabe_strony": "string",
    "luka_rynkowa": "string"
  },
  "analiza_globalna": {
    "co_robia_dobrze": ["string", "string", "string"],
    "co_robia_zle": ["string", "string", "string"],
    "luka": "string",
    "jak_wygrac": ["string", "string", "string", "string", "string"]
  },
  "strategia": {
    "kanal_1": "string",
    "kanal_1_opis": "string",
    "kanal_2": "string",
    "kanal_2_opis": "string",
    "kanal_3": "string",
    "kanal_3_opis": "string",
    "budzet_start": "string - jesli podano konkretny budzet miesieczny, podaj DOKLADNY podzial tego budzetu miedzy kanaly (kwoty w PLN), jesli 'Nie wiem / brak budzetu' zaproponuj realny budzet startowy"
  },
  "meta_ads": [
    {"wariant": "Wariant 1 - Bol", "headline": "max 40 znakow", "primary": "2-3 zdania", "cta": "string"},
    {"wariant": "Wariant 2 - Rozwiazanie", "headline": "max 40 znakow", "primary": "2-3 zdania", "cta": "string"},
    {"wariant": "Wariant 3 - Dowod spoleczny", "headline": "max 40 znakow", "primary": "2-3 zdania", "cta": "string"}
  ]
}"""

        tekst = claude_call(system_prompt, user_prompt, ak, 8000)
        wynik = safe_parse_json(tekst)
        if wynik is None:
            FALLBACK["mapa_popytu"]["insight"] = "Blad parsowania JSON. Sprobuj ponownie."
            return FALLBACK

        # Uzupełnij brakujące klucze fallbackiem
        for k, v in FALLBACK.items():
            if k not in wynik:
                wynik[k] = v

        return wynik
    except Exception as e:
        FALLBACK["mapa_popytu"]["insight"] = f"Blad API: {str(e)[:100]}"
        return FALLBACK

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("## Panel uzytkownika")
    st.markdown("---")
    max_s = info["max_skanow"]; wykorzystane = info["skany_wykorzystane"]; procent = int((wykorzystane / max_s) * 100) if max_s > 0 else 0
    kolor = "kpi-val-green" if pozostalo > 10 else ("kpi-val-orange" if pozostalo > 3 else "kpi-val-red")
    st.markdown(f'<div class="kpi-card"><div class="kpi-val {kolor}">{pozostalo}</div><div class="kpi-label">Skanow pozostalo</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(procent / 100)
    st.markdown(f'<div class="skany-bar">Kod: <b>{info["kod"]}</b> | {wykorzystane}/{max_s} | Wygasa: {info["data_wygasniecia"]}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Ustawienia B2B")
    tryb_skanu = st.radio("Tryb skanu", ["Szybki (1 zapytanie)", "Sredni (3 zapytania)", "Masowy (6 zapytan AUTO)"])
    mf = st.slider("Max firm per zapytanie", 5, 20, 10)
    zrodla = st.multiselect("Zrodla", ["Google Maps", "Google Web"], default=["Google Maps"])
    st.markdown("---")
    st.markdown("### Filtry B2B")
    bw = st.checkbox("Tylko BEZ strony WWW")
    bt = st.checkbox("Tylko Z telefonem", value=True)
    wykl = st.checkbox("Wykluczaj sieciowki", value=True)
    weryfikuj_www = st.checkbox("Weryfikuj strony WWW", value=True)
    min_score = st.slider("Min AI Score", 0, 99, 45)
    mo = st.slider("Maks opinii", 10, 500, 200)
    min_op = st.slider("Min opinii", 0, 100, 0)
    sort = st.radio("Sortuj po", ["AI Score", "Najmniej opinii", "Najslabsza WWW"])
    st.markdown("---")
    st.markdown("### Tryb lokalizacji")
    tryb_lok = st.radio("Wybierz tryb", ["Konkretne miasto", "Gmina / Powiat", "Wojewodztwo", "Kod pocztowy"])
    st.markdown("---")
    if st.button("Wyloguj sie", use_container_width=True):
        st.session_state.zalogowany = False; st.session_state.kod_info = None; st.session_state.historia = []; st.rerun()
    if st.session_state.historia:
        st.markdown("---"); st.markdown("### Historia")
        for h in reversed(st.session_state.historia[-5:]):
            st.markdown("- **" + h["branza"] + "** / " + h["lok"] + " -> " + str(h["wyniki"]) + " (" + h["czas"] + ")")

c1h, c2h = st.columns([3,1])
with c1h:
    st.markdown('<div class="app-title">AI Lead Gen <span class="accent">PRO</span></div><div class="app-sub">Automatyczny skaner B2B + B2C Intelligence — Analiza rynku, Głos klienta, Mapa konkurencji, Gotowe reklamy</div>', unsafe_allow_html=True)
with c2h:
    st.markdown('<div style="text-align:right;padding-top:.5rem"><span style="background:#f0fdf4;color:#16a34a;border:1.5px solid #16a34a;border-radius:20px;padding:5px 16px;font-size:.72rem;font-weight:700">v3.1 LIVE</span></div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

if pozostalo <= 5:
    st.markdown(f'<div class="warning-box">⚠️ Zostało Ci tylko <b>{pozostalo} skanów</b>. Odnów subskrypcję.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

mc1, mc2, _ = st.columns([1.3, 1.5, 3])
with mc1:
    if st.button("B2B — Znajdź firmy do oferty", type="primary" if st.session_state.tryb_modulu=="B2B" else "secondary", use_container_width=True):
        st.session_state.tryb_modulu = "B2B"; st.rerun()
with mc2:
    if st.button("B2C — Intelligence rynkowy", type="primary" if st.session_state.tryb_modulu=="B2C" else "secondary", use_container_width=True):
        st.session_state.tryb_modulu = "B2C"; st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# MODUL B2B
# ══════════════════════════════════════════
if st.session_state.tryb_modulu == "B2B":
    st.markdown('<div class="section-header">B2B — Znajdz lokalne firmy ktore potrzebuja Twoich uslug</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: branza = st.text_input("Branza / Nisza", placeholder="np. Dekarz, Salon urody, Fotograf...")
    with col2:
        lok = ""
        if tryb_lok == "Konkretne miasto": lok = st.text_input("Miasto", placeholder="np. Warszawa, Krakow...")
        elif tryb_lok == "Gmina / Powiat": lok = st.text_input("Gmina / Powiat", placeholder="np. Gmina Piaseczno...")
        elif tryb_lok == "Wojewodztwo": lok = "woj. " + st.selectbox("Wojewodztwo", WOJEWODZTWA)
        else:
            kc1, kc2 = st.columns(2)
            with kc1: kp = st.text_input("Kod pocztowy", placeholder="02-001")
            with kc2: pr = st.selectbox("Promien", ["5 km","10 km","25 km","50 km"])
            lok = kp + " (+" + pr + ")"
    st.markdown("<br>", unsafe_allow_html=True)
    _, bc, _ = st.columns([1,2,1])
    with bc: go_b2b = st.button("URUCHOM MASOWY SKAN B2B", type="primary", use_container_width=True, disabled=(pozostalo <= 0))

    if go_b2b:
        if not branza.strip(): st.error("Wpisz branze!"); st.stop()
        if not SK: st.error("Brak klucza Serper!"); st.stop()
        bar = st.progress(0); msg = st.empty(); stats_box = st.empty()
        wszystkie = []; widziane = set()
        msg.info("Generuje zapytania..."); bar.progress(5)
        zapytania = generuj_zapytania_b2b(branza, lok, AK, tryb_skanu)
        for i, zap in enumerate(zapytania):
            bar.progress(int(10 + 35 * i / len(zapytania))); msg.info("Skanuje (" + str(i+1) + "/" + str(len(zapytania)) + "): " + zap)
            if "Google Maps" in zrodla:
                for f in szukaj_maps(zap, SK, mf):
                    k2 = f["nazwa"].lower().strip()
                    if k2 not in widziane: widziane.add(k2); wszystkie.append(f)
            if "Google Web" in zrodla:
                for f in szukaj_web(zap, SK, mf):
                    k2 = f["nazwa"].lower().strip()
                    if k2 not in widziane: widziane.add(k2); wszystkie.append(f)
            stats_box.info("Zebrano " + str(len(wszystkie)) + " firm...")
        bar.progress(50); msg.info("Weryfikuje " + str(len(wszystkie)) + " firm...")
        rows = []
        for i, f in enumerate(wszystkie):
            if wykl and jest_sieciowka(f["nazwa"]): continue
            if bw and f["www"] not in ["brak","sprawdz na stronie",""]: continue
            if bt and f["telefon"] in ["brak","","sprawdz na stronie"]: continue
            if f["opinie"] > mo or f["opinie"] < min_op: continue
            bar.progress(50 + int(40 * i / max(len(wszystkie),1))); msg.info("Analizuje: " + f["nazwa"])
            wer = weryfikuj_strone(f["www"]) if weryfikuj_www else {"dziala": True, "ssl": False, "ocena_www": 5, "problemy": [], "ma_rezerwacje": False, "ma_social": False}
            score = oblicz_score(f, wer)
            if score < min_score: continue
            ai = analiza_claude_b2b(f, branza, AK, wer, score)
            rows.append({"Status": status_leada(score), "Nazwa": f["nazwa"], "Telefon": f["telefon"], "WWW": f["www"], "Adres": f["adres"], "Opinie": f["opinie"], "Ocena Google": f["ocena"], "Ocena strony": wer["ocena_www"], "SSL": "TAK" if wer["ssl"] else "NIE", "Rezerwacja": "TAK" if wer["ma_rezerwacje"] else "NIE", "Problemy WWW": " | ".join(wer["problemy"]) if wer["problemy"] else "OK", "AI Score": score, "Szansa %": ai.get("szansa",50), "Problem": ai.get("problem",""), "SMS": ai.get("sms",""), "Call": ai.get("call",""), "Email temat": ai.get("email_temat",""), "Email tresc": ai.get("email_tresc",""), "Followup 1": ai.get("followup1",""), "Followup 2": ai.get("followup2","")})
        bar.progress(100); msg.empty(); stats_box.empty(); bar.empty()
        if not rows: st.warning("Brak wynikow. Zmien filtry."); st.stop()
        df = pd.DataFrame(rows)
        if sort == "AI Score": df = df.sort_values("AI Score", ascending=False)
        elif sort == "Najmniej opinii": df = df.sort_values("Opinie", ascending=True)
        else: df = df.sort_values("Ocena strony", ascending=True)
        df = df.reset_index(drop=True)
        zapisz_skan(st.session_state.kod_info)
        st.session_state.kod_info["skany_wykorzystane"] += 1; st.session_state.kod_info["pozostalo"] -= 1
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
            for _, row in df.head(25).iterrows():
                with st.expander(row["Status"] + " | " + row["Nazwa"] + " — " + row["Telefon"] + " | Score: " + str(row["AI Score"]) + "/99"):
                    ca, cb = st.columns(2)
                    with ca: st.markdown("**SMS:**"); st.info(row["SMS"]); st.caption("Problem: " + row["Problem"])
                    with cb: st.markdown("**Cold Call:**"); st.success(row["Call"])
        with tab3:
            for _, row in df.head(25).iterrows():
                with st.expander(row["Status"] + " | " + row["Nazwa"] + " | Score: " + str(row["AI Score"]) + "/99"):
                    st.markdown("**Email — Temat: " + row["Email temat"] + "**"); st.warning(row["Email tresc"])
                    st.markdown("**Follow-up 1 (dzien 3):**"); st.info(row["Followup 1"])
                    st.markdown("**Follow-up 2 (dzien 7):**"); st.error(row["Followup 2"])
        with tab4:
            st.markdown("### TOP 5 do kontaktu TERAZ")
            top5 = df[df["Status"]=="HOT"].head(5) if len(df[df["Status"]=="HOT"]) >= 3 else df.head(5)
            for _, row in top5.iterrows():
                ta, tb, tc = st.columns([1,1,2])
                with ta: st.markdown("**" + row["Nazwa"] + "**"); st.markdown("Tel: `" + row["Telefon"] + "`")
                with tb: st.markdown("Score: **" + str(row["AI Score"]) + "/99**"); st.caption(row["Problem"])
                with tc: st.info("SMS: " + row["SMS"])
                st.markdown("<hr>", unsafe_allow_html=True)
        with tab5:
            ta, tb, tc = st.columns(3)
            with ta:
                st.markdown("**Rozklad statusow:**")
                for s,c in df["Status"].value_counts().items(): st.markdown("- " + str(s) + ": **" + str(c) + "**")
            with tb:
                st.markdown("**Najczestsze problemy:**")
                ap = []
                for p in df["Problemy WWW"]: ap.extend([x.strip() for x in str(p).split("|") if x.strip() and x.strip() != "OK"])
                for p,c in pd.Series(ap).value_counts().head(6).items(): st.markdown("- " + str(p) + ": **" + str(c) + "x**")
            with tc:
                st.markdown("**Statystyki:**")
                st.markdown("- Bez WWW: **" + str(bez_www) + "**")
                st.markdown("- HOT: **" + str(hot) + "**, WARM: **" + str(warm) + "**")
        with tab6:
            ec1, ec2 = st.columns(2)
            with ec1: st.download_button("Pobierz pelna baze CSV", df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"), file_name="leady_B2B_" + branza + ".csv", mime="text/csv", use_container_width=True)
            with ec2:
                df_hw = df[df["Status"].isin(["HOT","WARM"])]
                st.download_button("Pobierz HOT + WARM", df_hw.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"), file_name="HOT_WARM_" + branza + ".csv", mime="text/csv", use_container_width=True)

# ══════════════════════════════════════════
# MODUL B2C
# ══════════════════════════════════════════
else:
    st.markdown('<div class="section-header">B2C Intelligence — Pelna analiza rynku dla Twojego produktu</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">🧠 Skanuję Google, Allegro, fora i recenzje żeby dać Ci pełny obraz rynku — kim jest Twój klient, gdzie siedzi, jak do niego dotrzeć i jak pokonać globalną konkurencję.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    bc1, bc2 = st.columns(2)
    with bc1:
        produkt_b2c = st.text_input("Twoj produkt / usluga", placeholder="np. Poduszka ortopedyczna, Kurs online gotowania...")
        problem_b2c = st.text_input("Problem klienta ktory rozwiazujesz", placeholder="np. Chroniczny bol pleców, Brak czasu na gotowanie...")
    with bc2:
        lok_b2c = st.text_input("Rynek docelowy", placeholder="np. Polska, Warszawa, cala Europa...")
        grupa_b2c = st.selectbox("Glowna grupa docelowa", ["Wszyscy","Kobiety 25-35","Kobiety 35-50","Mamy z dziecmi","Seniorzy 60+","Mezczyzni 25-45","Przedsiebiorcy","Studenci","Sportowcy"])
        budzet_b2c = st.selectbox("Twoj miesieczny budzet na reklamy", ["Nie wiem / brak budzetu","Do 500 zl","500 - 1500 zl","1500 - 5000 zl","5000 - 15000 zl","Ponad 15000 zl"])

    st.markdown("<br>", unsafe_allow_html=True)
    _, bbc, _ = st.columns([1,2,1])
    with bbc:
        go_b2c = st.button("URUCHOM PELNA ANALIZE RYNKU B2C", type="primary", use_container_width=True, disabled=(pozostalo <= 0))

    if go_b2c:
        if not produkt_b2c.strip() or not problem_b2c.strip(): st.error("Wpisz produkt i problem!"); st.stop()
        if not SK: st.error("Brak klucza Serper!"); st.stop()

        bar_b2c = st.progress(0)
        msg_b2c = st.empty()

        msg_b2c.info("Uruchamiam pelna analize rynku — moze zajac 30-60 sekund...")
        bar_b2c.progress(5)

        dane = zbierz_dane_b2c(produkt_b2c, problem_b2c, lok_b2c, SK, msg_b2c)
        bar_b2c.progress(70)

        msg_b2c.info("Claude AI syntetyzuje dane i tworzy strategie...")
        wyniki_ai = analiza_ai_b2c(produkt_b2c, problem_b2c, lok_b2c, grupa_b2c, budzet_b2c, dane, AK)
        bar_b2c.progress(95)

        zapisz_skan(st.session_state.kod_info)
        st.session_state.kod_info["skany_wykorzystane"] += 1
        st.session_state.kod_info["pozostalo"] -= 1
        bar_b2c.progress(100); msg_b2c.empty(); bar_b2c.empty()

        st.success(f"Analiza gotowa! Zebrano dane z {len(dane['raw_snippets'])} zrodel.")
        st.markdown("<br>", unsafe_allow_html=True)

        # ── 5 ZAKŁADEK — nowa struktura ──
        t1, t2, t3, t4, t5 = st.tabs([
            "📊 Mapa Popytu",
            "💬 Glos Klienta",
            "🏪 Mapa Konkurencji",
            "🌍 Analiza Konkurencji Globalnej",
            "🎯 Strategia + Meta Ads"
        ])

        # ── TAB 1: MAPA POPYTU ──
        with t1:
            st.markdown("### 📊 Mapa Popytu Rynkowego")
            mp = wyniki_ai.get("mapa_popytu", {})
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f'<div class="insight-card"><div class="insight-title">📈 Wielkosc rynku</div><div class="insight-text">{mp.get("wielkosc","brak")}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="insight-card"><div class="insight-title">📅 Sezonowosc</div><div class="insight-text">{mp.get("sezonowosc","brak")}</div></div>', unsafe_allow_html=True)
            with col_b:
                st.markdown(f'<div class="insight-card"><div class="insight-title">💡 Kluczowy insight</div><div class="insight-text">{mp.get("insight","brak")}</div></div>', unsafe_allow_html=True)
                slowa = mp.get("slowa_kluczowe", [])
                if slowa:
                    slowa_html = " • ".join([str(s) for s in slowa if s])
                    st.markdown(f'<div class="insight-card"><div class="insight-title">🔑 Top slowa kluczowe</div><div class="insight-text">{slowa_html}</div></div>', unsafe_allow_html=True)
            if dane["popyt"]:
                st.markdown("#### 🔍 Powiazane zapytania z Google")
                cols = st.columns(3)
                for i, q in enumerate(dane["popyt"][:9]):
                    with cols[i % 3]:
                        st.markdown(f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:8px 12px;margin-bottom:8px;font-size:.85rem;color:#374151">🔎 {q}</div>', unsafe_allow_html=True)

        # ── TAB 2: GŁOS KLIENTA ──
        with t2:
            st.markdown("### 💬 Głos Klienta — Co naprawdę mówią o tym problemie")
            gk = wyniki_ai.get("glos_klienta", {})
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f'<div class="insight-card"><div class="insight-title">😤 Glowny bol klienta</div><div class="insight-text">{gk.get("glowny_bol","brak")}</div></div>', unsafe_allow_html=True)
                st.markdown("**😰 Obawy przed zakupem:**")
                for ob in gk.get("obawy", []):
                    if ob: st.markdown(f'<div style="background:#fff7ed;border-left:3px solid #ea580c;border-radius:0 8px 8px 0;padding:8px 12px;margin-bottom:6px;font-size:.85rem">⚠️ {ob}</div>', unsafe_allow_html=True)
            with col_b:
                st.markdown("**✅ Co motywuje do zakupu:**")
                for mot in gk.get("motywatory", []):
                    if mot: st.markdown(f'<div style="background:#f0fdf4;border-left:3px solid #16a34a;border-radius:0 8px 8px 0;padding:8px 12px;margin-bottom:6px;font-size:.85rem">💪 {mot}</div>', unsafe_allow_html=True)
            st.markdown("#### 📝 Cytaty z internetu — Prawdziwy głos klienta")
            for cytat in gk.get("cytaty", []):
                if cytat: st.markdown(f'<div class="quote-card">"{cytat}"</div>', unsafe_allow_html=True)
            if dane["glos_klienta"]:
                st.markdown("#### 🔗 Zrodla gdzie ludzie rozmawiaja o tym problemie")
                for item in dane["glos_klienta"][:8]:
                    st.markdown(f'<div class="place-card"><span class="place-type">Forum/Recenzja</span><div><b style="font-size:.85rem">{item["zrodlo"][:60]}</b><br><span style="font-size:.8rem;color:#64748b">{item["cytat"][:120]}...</span></div></div>', unsafe_allow_html=True)

        # ── TAB 3: MAPA KONKURENCJI ──
        with t3:
            st.markdown("### 🏪 Mapa Konkurencji Lokalnej")
            mk = wyniki_ai.get("mapa_konkurencji", {})
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f'<div class="insight-card"><div class="insight-title">🎯 Luka rynkowa do wykorzystania</div><div class="insight-text">{mk.get("luka_rynkowa","brak")}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="insight-card"><div class="insight-title">😤 Slabe strony konkurencji</div><div class="insight-text">{mk.get("slabe_strony","brak")}</div></div>', unsafe_allow_html=True)
            with col_b:
                st.markdown("**🏆 Glowni gracze na rynku:**")
                for gracz in mk.get("gracze", []):
                    if gracz: st.markdown(f'<div class="competitor-card"><b style="font-size:.85rem">🏪 {gracz}</b></div>', unsafe_allow_html=True)

        # ── TAB 4: ANALIZA KONKURENCJI GLOBALNEJ (NOWA) ──
        with t4:
            st.markdown("### 🌍 Analiza Konkurencji Globalnej")
            st.markdown('<div class="info-box">Przeanalizowałem sklepy i firmy sprzedające ten sam produkt na świecie (Shopify, Amazon, Allegro). Oto co robią dobrze, co robią źle i jak możesz ich pokonać.</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            ag = wyniki_ai.get("analiza_globalna", {})

            # Wyniki AI — co robią dobrze vs źle
            col_good, col_bad = st.columns(2)
            with col_good:
                st.markdown("#### ✅ Co robi konkurencja dobrze")
                for item in ag.get("co_robia_dobrze", []):
                    if item: st.markdown(f'<div style="background:#f0fdf4;border-left:3px solid #16a34a;border-radius:0 8px 8px 0;padding:8px 12px;margin-bottom:6px;font-size:.85rem;color:#14532d">✅ {item}</div>', unsafe_allow_html=True)
            with col_bad:
                st.markdown("#### ❌ Co robi konkurencja źle (Twoja szansa)")
                for item in ag.get("co_robia_zle", []):
                    if item: st.markdown(f'<div style="background:#fff7ed;border-left:3px solid #ea580c;border-radius:0 8px 8px 0;padding:8px 12px;margin-bottom:6px;font-size:.85rem;color:#9a3412">❌ {item}</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Luka rynkowa
            luka = ag.get("luka", "")
            if luka:
                st.markdown(f'<div class="insight-card" style="border-left:3px solid #7c3aed"><div class="insight-title">🎯 Główna luka rynkowa którą możesz wypełnić</div><div class="insight-text" style="font-size:.95rem">{luka}</div></div>', unsafe_allow_html=True)

            # Lista akcji "zrób to lepiej od nich"
            jak_wygrac = ag.get("jak_wygrac", [])
            if jak_wygrac:
                st.markdown("#### 🏆 Lista akcji — Zrób to lepiej od globalnej konkurencji")
                for i, akcja in enumerate(jak_wygrac, 1):
                    if akcja: st.markdown(f'<div class="action-item">✅ <b>{i}.</b> {akcja}</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Znalezione sklepy z linkami
            if dane["konkurencja_globalna"]:
                st.markdown("#### 🔗 Znalezieni globalni konkurenci — przejrzyj ich sklepy")
                st.markdown(f'<div class="success-box">Znaleziono <b>{len(dane["konkurencja_globalna"])} stron</b> sprzedających podobny produkt. Kliknij linki żeby przejrzeć jak to robią.</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                # Grupuj według typu
                typy_glob = {}
                for k in dane["konkurencja_globalna"]:
                    t = k["typ"]
                    if t not in typy_glob: typy_glob[t] = []
                    typy_glob[t].append(k)

                ikony_glob = {"Shopify": "🛍️", "Amazon": "📦", "Etsy": "🎨", "AliExpress": "🇨🇳", "eBay": "🔨", "Allegro": "🛒", "Recenzje": "⭐", "Sklep online": "🌐", "Strona WWW": "💻"}

                for typ, items in sorted(typy_glob.items(), key=lambda x: -len(x[1])):
                    ikona = ikony_glob.get(typ, "🌐")
                    st.markdown(f"**{ikona} {typ} ({len(items)} znalezionych)**")
                    for item in items[:6]:
                        st.markdown(f'''<div class="competitor-card-global">
                            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem">
                                <div style="flex:1">
                                    <b style="font-size:.88rem;color:#0f172a">{item["nazwa"]}</b><br>
                                    <span style="font-size:.8rem;color:#64748b;line-height:1.5">{item["opis"]}</span>
                                </div>
                                <a href="{item["link"]}" target="_blank" style="background:#eff6ff;color:#2563eb;border:1px solid #bfdbfe;border-radius:6px;padding:4px 12px;font-size:.75rem;font-weight:700;white-space:nowrap;text-decoration:none">Przejrzyj →</a>
                            </div>
                        </div>''', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                # Eksport
                df_glob = pd.DataFrame(dane["konkurencja_globalna"])
                st.download_button(
                    "📥 Pobierz listę globalnych konkurentów CSV",
                    df_glob.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
                    file_name=f"konkurencja_globalna_{produkt_b2c}.csv",
                    mime="text/csv"
                )

        # ── TAB 5: STRATEGIA + META ADS ──
        with t5:
            st.markdown("### 🎯 Strategia wejscia na rynek + Gotowe reklamy Meta Ads")
            strat = wyniki_ai.get("strategia", {})
            st.markdown("#### 📋 Rekomendowane kanaly (kolejnosc ataku)")
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.markdown(f'<div class="insight-card"><div class="insight-title">🥇 {strat.get("kanal_1","Kanal 1")}</div><div class="insight-text">{strat.get("kanal_1_opis","")}</div></div>', unsafe_allow_html=True)
            with col_s2:
                st.markdown(f'<div class="insight-card"><div class="insight-title">🥈 {strat.get("kanal_2","Kanal 2")}</div><div class="insight-text">{strat.get("kanal_2_opis","")}</div></div>', unsafe_allow_html=True)
            with col_s3:
                st.markdown(f'<div class="insight-card"><div class="insight-title">🥉 {strat.get("kanal_3","Kanal 3")}</div><div class="insight-text">{strat.get("kanal_3_opis","")}</div></div>', unsafe_allow_html=True)
            if strat.get("budzet_start"):
                st.markdown(f'<div class="warning-box">💰 <b>Rekomendowany budzet startowy:</b> {strat.get("budzet_start","")}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📣 3 Gotowe zestawy reklamowe Meta Ads")
            st.markdown('<div class="info-box">Skopiuj i wklej bezposrednio do Facebook Ads Manager. Przetestuj wszystkie 3 warianty i zostaw ten ktory ma najlepszy CTR.</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            for ad in wyniki_ai.get("meta_ads", []):
                st.markdown(f'<div class="ads-card"><div style="font-size:.72rem;color:#6366f1;font-weight:700;text-transform:uppercase;margin-bottom:.5rem">{ad.get("wariant","")}</div><div class="ads-headline">{ad.get("headline","")}</div><div style="font-size:.88rem;color:#374151;margin:.6rem 0;line-height:1.6">{ad.get("primary","")}</div><div style="background:#2563eb;color:white;display:inline-block;padding:6px 16px;border-radius:6px;font-size:.8rem;font-weight:700">{ad.get("cta","")}</div></div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div style="text-align:center;font-size:.72rem;color:#cbd5e1">AI Lead Gen PRO v3.1 — B2B + B2C Intelligence — Powered by Claude AI + Serper.dev</div>', unsafe_allow_html=True)
