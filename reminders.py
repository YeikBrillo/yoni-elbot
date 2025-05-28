import os
import datetime
import requests
from bs4 import BeautifulSoup

# justo al principio de reminders.py
print("🚀 DEBUG: arranca reminders.py")
if os.getenv("FORCE_TEST") == "1":
    send("🧪 Mensaje de prueba: Yoni el bot funciona.")


# ─── CONFIGURACIÓN ───────────────────────────────────────────────────────────
TOKEN   = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

INICIO_LUZ  = datetime.date(2025, 3, 28)
INICIO_AGUA = datetime.date(2025, 2, 12)
CICLO_LUZ   = 31
CICLO_AGUA  = 64


def send(message):
    """Envía mensaje por Telegram (solo el texto proporcionado)."""
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    requests.post(url, data={'chat_id': CHAT_ID, 'text': message})


def check_internet():
    # Pago de internet el día 20 de cada mes
    if datetime.date.today().day == 20:
        send("📶 Mamonaa acuérdate de pagar el internet hoy!")


def check_meters():
    hoy = datetime.date.today()
    # Luz: cada 31 días exactos
    delta_luz = (hoy - INICIO_LUZ).days % CICLO_LUZ
    if delta_luz == 0:
        send(f"📸 Illo acuérdate de echarle una fotito al contador de luz (cerca de {hoy.strftime('%d/%m/%Y')}).")
    # Agua: cada 64 días exactos
    delta_agua = (hoy - INICIO_AGUA).days % CICLO_AGUA
    if delta_agua == 0:
        send(f"📸 Illo acuérdate de echarle una fotito al contador de agua (cerca de {hoy.strftime('%d/%m/%Y')}).")


def check_matches():
    mañana = datetime.date.today() + datetime.timedelta(days=1)
    resp = requests.get("https://www.malagacf.com/partidos")
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for card in soup.select("div.card-match"):
        fecha_txt = card.select_one(".date-match").text.strip()
        estadio   = card.select_one(".stadium").text.strip()
        try:
            fecha = datetime.datetime.strptime(fecha_txt, "%d/%m/%Y").date()
        except ValueError:
            continue
        if estadio.lower().startswith("la rosaleda") and fecha == mañana:
            send("⚽ Novea.. Mañana juega el Málaga en casa. Si no tienes q coger el coxe, no lo muevas!")
            break


if __name__ == "__main__":
    check_internet()
    check_meters()
    check_matches()

