import os
import datetime
import requests
from bs4 import BeautifulSoup

# ─── CONFIGURACIÓN ───────────────────────────────────────────────────────────
TOKEN   = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

INICIO_LUZ  = datetime.date(2025, 3, 28)
INICIO_AGUA = datetime.date(2025, 2, 12)
CICLO_LUZ   = 31
CICLO_AGUA  = 64

def send(message):
    """Envía mensaje por Telegram con prefijo ‘Yoni el bot’."""
    full = f"🤖 Yoni el bot:\n{message}"
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    requests.post(url, data={'chat_id': CHAT_ID, 'text': full})

def check_internet():
    if datetime.date.today().day == 1:
        send("📶 Mamonaa acuérdate de pagar el internet HOY!")

def check_meters():
    hoy = datetime.date.today()
    # Cálculo de desviación de ciclo
    delta_luz  = (hoy - INICIO_LUZ).days % CICLO_LUZ
    delta_agua = (hoy - INICIO_AGUA).days % CICLO_AGUA

    # Luz: mensajes personalizados
    if delta_luz in (30, 31, 32):  # días 30, 31 y 32
        send(f"💡 Illo, acuérdate de echarle fotito al contador de LUZ (aprox. {hoy.strftime('%d/%m/%Y')}).")

    # Agua: mensajes personalizados
    if delta_agua in (63, 64, 65):  # días 63, 64 y 65
        send(f"💧 Illo, acuérdate de echarle fotito al contador de AGUA (aprox. {hoy.strftime('%d/%m/%Y')}).")

def check_matches():
    mañana = datetime.date.today() + datetime.timedelta(days=1)
    resp = requests.get("https://www.malagacf.com/partidos")
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # Ajusta los selectores si cambian:
    for card in soup.select("div.card-match"):
        fecha_txt = card.select_one(".date-match").text.strip()   # ej. "31/05/2025"
        estadio   = card.select_one(".stadium").text.strip()      # ej. "La Rosaleda"
        try:
            fecha = datetime.datetime.strptime(fecha_txt, "%d/%m/%Y").date()
        except:
            continue
        if estadio.lower().startswith("la rosaleda") and fecha == mañana:
            send("⚽ Novea.. Mañana juega el Málaga en casa. No muevas el coxe si no hace falta!")
            break

if __name__ == "__main__":
    check_internet()
    check_meters()
    check_matches()
