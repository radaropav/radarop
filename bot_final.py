import time
import requests
import json
import sys
import threading
import os
import yfinance as yf

# =====================================================================
# CONFIGURACIÓN COMPLETA UNIFICADA SIN ENLACES CORRUPTOS
# =====================================================================
SYMBOL = "ETH-USD"  # Servidor Yahoo global inmune a geobloqueos
INTERVALO_SEGUNDOS = 60  

# Enlace de API indestructible anclado a tu canal privado
URL_DIRECTA_TELEGRAM = "https://telegram.org"
TELEGRAM_CHAT_ID = "-1004335003036"  # ID de tu canal Bunkerop

PORCENTAJE_SL = 0.0015  
PORCENTAJE_TP = 0.0022  

# =====================================================================
# CONEXIONES DIRECTAS DE PRODUCCIÓN
# =====================================================================

def enviar_telegram(mensaje):
    """Despacha alertas sin depender de variables automáticas."""
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try: 
        res = requests.post(URL_DIRECTA_TELEGRAM, json=payload, timeout=5)
        if res.status_code != 200:
            print(f"❌ Error en API Telegram (Canal): {res.text}")
        else:
            print("🟩 Mensaje enviado al canal de Telegram.")
    except Exception as e: 
        print(f"❌ Fallo de red en enviar_telegram: {e}")

def obtener_datos_mercado():
    """Descarga de datos pura a través de Yahoo Finance."""
    try:
        ticker = yf.Ticker(SYMBOL)
        datos = ticker.history(period="1d", interval="1m")
        if not datos.empty:
            precio = float(datos['Close'].iloc[-1])
            volumen = float(datos['Volume'].iloc[-1]) if 'Volume' in datos.columns else 15000000.0
            open_interest = volumen * 0.35
            return precio, open_interest, volumen
    except Exception as e:
        print(f"⚠️ Error en oráculo Yahoo Finance: {e}")
    return None, None, None

# =====================================================================
# RADAR PRINCIPAL EN SEGUNDO PLANO
# =====================================================================
def ejecutar_bucle_radar():
    print(f"📡 RADAR WATSON GLOBAL ACTIVADO PARA {SYMBOL}")
    enviar_telegram(f"📡 *Radar Perpetuo Operativo*\nMonitoreando ETH de forma persistente en la nube...")

    precio_anterior, oi_anterior, vol_anterior = obtener_datos_mercado()
    if not precio_anterior:
        precio_anterior, oi_anterior, vol_anterior = 1899.00, 500000.0, 15000000.0
    print(f"📊 CONEXIÓN INICIAL ESTABILIZADA | ETH: {precio_anterior:.2f}\n")

    while True:
        try:
            time.sleep(INTERVALO_SEGUNDOS)
            precio_actual, oi_actual, vol_actual = obtener_datos_mercado()
            
            if not precio_actual:
                continue
                
            delta_precio = ((precio_actual - precio_anterior) / precio_anterior) * 100
            delta_oi = ((oi_actual - oi_anterior) / oi_anterior) * 100 if oi_anterior > 0 else 0.0
            
            detalles_orden = ""
            
            if delta_precio > 0.15 and delta_oi > 0.4:
                entorno = "🚀 INTENCIÓN ALCISTA INSTITUCIONAL"
                accion_trader = "🟩 OPERAR AL LONG"
                sl = precio_actual * (1 - PORCENTAJE_SL)
                tp = precio_actual * (1 + PORCENTAJE_TP)
                detalles_orden = f"\n📊 *Estructura:* Entrada: `${precio_actual:.2f}` | SL: `${sl:.2f}` | TP: `${tp:.2f}`"
            elif delta_precio < -0.15 and delta_oi > 0.4:
                entorno = "🩸 INTENCIÓN BAJISTA INSTITUCIONAL"
                accion_trader = "🔴 OPERAR AL SHORT"
                sl = precio_actual * (1 + PORCENTAJE_SL)
                tp = precio_actual * (1 - PORCENTAJE_TP)
                detalles_orden = f"\n📊 *Estructura:* Entrada: `${precio_actual:.2f}` | SL: `${sl:.2f}` | TP: `${tp:.2f}`"
            else:
                entorno = "⏳ ENTORNO NEUTRO"
                accion_trader = "⬜ MANTENERSE QUIETO"
            
            print(f"[RADAR] ETH: ${precio_actual:.2f} | Var: {delta_precio:+.3f}%")
            
            if accion_trader != "⬜ MANTENERSE QUIETO":
                alerta_minuto = f"🎯 *ETH:* ${precio_actual:.2f} | {accion_trader}{detalles_orden}"
                enviar_telegram(alerta_minuto)
                
            precio_anterior = precio_actual
            oi_anterior = oi_actual
            vol_anterior = vol_actual
            
        except Exception as e:
            print(f"❌ Error en bucle: {e}")
            time.sleep(5)

# =====================================================================
# CONFIGURACIÓN WSGI EXIGIDA POR RENDER
# =====================================================================
radar_iniciado = False

def app(environ, start_response):
    global radar_iniciado
    if not radar_iniciado:
        hilo_seguro = threading.Thread(target=ejecutar_bucle_radar)
        hilo_seguro.daemon = True
        hilo_seguro.start()
        radar_iniciado = True
    start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])
    mensaje = "📡 Radar Watson Pro: Sistema Operando Persistente 24/7."
    return [mensaje.encode('utf-8')]

if not radar_iniciado:
    hilo_seguro = threading.Thread(target=ejecutar_bucle_radar)
    hilo_seguro.daemon = True
    hilo_seguro.start()
    radar_iniciado = True
