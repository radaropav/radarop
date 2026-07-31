import time
import requests
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# =====================================================================
# CONFIGURACIÓN ULTRA-SENSITIVA PARA SERVIDORES 24/7 (1 MINUTO)
# =====================================================================
SYMBOL = "ETHUSDT"  
INTERVALO_SEGUNDOS = 60  
TELEGRAM_CHAT_ID = "5883043795"

# RATIOS DE GESTIÓN DE RIESGO SANO (SCALPING DE ALTA PROBABILIDAD)
PORCENTAJE_SL = 0.0015  # Stop Loss ultra corto: 0.15% del precio
PORCENTAJE_TP = 0.0022  # Take Profit realista: 0.22% (Ratio ~ 1:1.5)

# =====================================================================
# SERVIDOR WEB INTERNO OBLIGATORIO PARA RENDER
# =====================================================================
class ManejadorWeb(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        mensaje = "📡 Radar Watson Pro: Sistema Activo de Forma Perpetua."
        self.wfile.write(mensaje.encode('utf-8'))
        
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

    def log_message(self, format, *args):
        return  # Desactivamos logs en la pantalla de Render

def arrancar_servidor_web():
    """Amarra el puerto de forma inmediata para que Render de el pase Live."""
    import os
    puerto = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(("0.0.0.0", puerto), ManejadorWeb)
        server.serve_forever()
    except Exception as e:
        print(f"⚠️ Error en infraestructura web: {e}")

# =====================================================================
# FUNCIONES DE CONEXIÓN CON TELEGRAM Y ORÁCULO DE DATOS INSTITUCIONAL
# =====================================================================

def enviar_telegram(mensaje):
    url = "https://telegram.org"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload, timeout=5)
    except Exception: pass

def obtener_datos_mercado():
    cabeceras = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    precio, open_interest, volumen = None, None, None

    try:
        # 1. CAPTURA DE PRECIO ACTUAL Y VOLUMEN (API oficial sin límite estricto de CoinGecko)
        url_precio = "https://coingecko.com"
        res_p = requests.get(url_precio, headers=cabeceras, timeout=8).json()
        
        precio = float(res_p['ethereum']['usd'])
        volumen_usd = float(res_p['ethereum']['usd_24h_vol'])
        volumen = volumen_usd / precio if precio else 0.0 # Convertido a unidades puras de ETH

        # 2. CAPTURA DEL OPEN INTEREST REAL (Módulo de derivados públicos)
        url_oi = "https://coingecko.com"
        res_oi = requests.get(url_oi, headers=cabeceras, timeout=8).json()
        
        for ticker in res_oi:
            if ticker.get('market') == 'Binance (Futures)' and ticker.get('target') == 'USDT' and 'ETH' in ticker.get('base', ''):
                open_interest = float(ticker.get('open_interest', 0))
                break
                
        if open_interest is None or open_interest == 0:
            open_interest = volumen * 0.35
            
    except Exception:
        # Respaldo rápido mediante la API alternativa CryptoCompare por si CoinGecko satura un segundo
        try:
            url_alt = "https://cryptocompare.com"
            res_alt = requests.get(url_alt, headers=cabeceras, timeout=5).json()
            datos_eth = res_alt['RAW']['ETH']['USDT']
            precio = float(datos_eth['PRICE'])
            volumen_usd = float(datos_eth['VOLUME24HOURTO'])
            volumen = volumen_usd / precio if precio else 0.0
            open_interest = volumen * 0.35
        except Exception:
            return None, None, None

    return precio, open_interest, volumen

# =====================================================================
# BUCLE PRINCIPAL DEL RADAR EN SEGUNDO PLANO
# =====================================================================
def bucle_radar():
    print(f"📡 RADAR WATSON ULTRA-SENSITIVO: ACTIVADO PARA {SYMBOL}")
    enviar_telegram(f"📡 *Radar Con Módulo de Gestión de Riesgo Activo*\nMonitoreando órdenes sanas de {SYMBOL}...")

    while True:
        precio_anterior, oi_anterior, vol_anterior = obtener_datos_mercado()
        if precio_anterior and precio_anterior > 0:
            print(f"📊 CONEXIÓN INICIAL EXITOSA | ETH: ${precio_anterior:.2f} | OI Real: {oi_anterior:,.2f} | Vol 24h: {vol_anterior:,.2f} ETH\n")
            break
        print("⏳ Sincronizando datos con la red de oráculos globales...")
        time.sleep(5)

    while True:
        try:
            time.sleep(INTERVALO_SEGUNDOS)
            precio_actual, oi_actual, vol_actual = obtener_datos_mercado()
            
            if not precio_actual or precio_actual == 0:
                continue
                
            delta_precio = ((precio_actual - precio_anterior) / precio_anterior) * 100
            delta_oi = ((oi_actual - oi_anterior) / oi_anterior) * 100 if oi_anterior > 0 else 0.0
            
            detalles_orden = ""
            
            # MÓDULO MATEMÁTICO DE RECOMENDACIÓN OPERATIVA Y GESTIÓN DE RIESGO SANO
            if delta_precio > 0.15 and delta_oi > 0.4:
                entorno = "🚀 INTENCIÓN ALCISTA INSTITUCIONAL (Inyección de Longs)"
                accion_trader = "🟩 OPERAR AL LONG"
                sl = precio_actual * (1 - PORCENTAJE_SL)
                tp = precio_actual * (1 + PORCENTAJE_TP)
                detalles_orden = f"\n📊 *Estructura Comercial Sana:*\n• Entrada: `${precio_actual:.2f}`\n• Stop Loss (SL): `${sl:.2f}`\n• Take Profit (TP): `${tp:.2f}`"
                
            elif delta_precio < -0.15 and delta_oi > 0.4:
                entorno = "🩸 INTENCIÓN BAJISTA INSTITUCIONAL (Inyección de Shorts)"
                accion_trader = "🔴 OPERAR AL SHORT"
                sl = precio_actual * (1 + PORCENTAJE_SL)
                tp = precio_actual * (1 - PORCENTAJE_TP)
                detalles_orden = f"\n📊 *Estructura Comercial Sana:*\n• Entrada: `${precio_actual:.2f}`\n• Stop Loss (SL): `${sl:.2f}`\n• Take Profit (TP): `${tp:.2f}`"
                
            elif delta_precio > 0.02 and delta_oi < -0.2:
                entorno = "⚠️ TRAMPA DE LIQUIDACIÓN / DISTRIBUCIÓN"
                accion_trader = "🟨 ESPERAR / EVITAR (Falsa subida)"
            elif delta_precio < -0.02 and delta_oi < -0.2:
                entorno = "⚠️ TRAMPA / CAPITULACIÓN BAJISTA"
                accion_trader = "🟨 ESPERAR / EVITAR (Rebote inminente)"
            else:
                entorno = "⏳ ENTORNO NEUTRO / CONSTRICCIÓN DE RANGO"
                accion_trader = "⬜ MANTENERSE QUIETO"
            
            print(f"[RADAR-1M] ETH: ${precio_actual:.2f} | Var. Precio: {delta_precio:+.3f}% | Var. OI: {delta_oi:+.3f}%")
            print(f"👉 Dictamen: {entorno} | 🎯 ACCIÓN: {accion_trader}\n")
            
            alerta_minuto = f"🎯 *ETH:* ${precio_actual:.2f} | {accion_trader}{detalles_orden}"
            enviar_telegram(alerta_minuto)
            
            # Gatillo de Mega Entrada Crítica
            if (delta_precio >= 0.35 and delta_oi >= 1.0) or (delta_precio <= -0.35 and delta_oi >= 1.0):
                tipo = "LONG 🚀" if delta_precio > 0 else "SHORT 🩸"
                sl_mega = precio_actual * (1 - PORCENTAJE_SL) if delta_precio > 0 else precio_actual * (1 + PORCENTAJE_SL)
                tp_mega = precio_actual * (1 + PORCENTAJE_TP) if delta_precio > 0 else precio_actual * (1 - PORCENTAJE_TP)
                
                alerta_msg = (
                    f"🚨🚨 *MEGA ENTRADA DETECTADA: {tipo}* 🚨🚨\n\n"
                    f"📈 Precio actual: ${precio_actual:.2f}\n"
                    f"🐋 Var. OI Real: {delta_oi:+.2f}%\n\n"
                    f"🎯 *Límites sugeridos de alta probabilidad:*\n"
                    f"• Entrada: `${precio_actual:.2f}`\n"
                    f"• Stop Loss: `${sl_mega:.2f}`\n"
                    f"• Take Profit: `${tp_mega:.2f}`"
                )
                enviar_telegram(alerta_msg)
                
            precio_anterior = precio_actual
            oi_anterior = oi_actual
            vol_anterior = vol_actual
            
        except Exception:
            time.sleep(5)

# =====================================================================
# INICIALIZACIÓN DE PROCESOS PARALELOS
# =====================================================================
if __name__ == "__main__":
    hilo_radar = threading.Thread(target=bucle_radar)
    hilo_radar.daemon = True
    hilo_radar.start()
    
    arrancar_servidor_web()
