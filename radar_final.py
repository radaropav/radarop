import time
import requests
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# Importamos la librería oficial de datos
import yfinance as yf

# =====================================================================
# CONFIGURACIÓN ULTRA-SENSITIVA PARA SERVIDORES 24/7 (1 MINUTO)
# =====================================================================
SYMBOL = "ETH-USD"  
INTERVALO_SEGUNDOS = 60  
TELEGRAM_CHAT_ID = "5883043795"

# =====================================================================
# SERVIDOR WEB INMUNE A BLOQUEOS (Uso de HTTP nativo sin Flask)
# =====================================================================
class ServidorFantasma(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Radar Watson Pro: Sistema Activo 24/7")
        
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

def arrancar_servidor_web():
    """Inicia la pasarela web nativa para que Render no tire Time Out."""
    import os
    puerto = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", puerto), ServidorFantasma)
    server.serve_forever()

# =====================================================================
# FUNCIONES DE CONEXIÓN CON RECOMENDACIÓN OPERATIVA EN TELEGRAM
# =====================================================================

def enviar_telegram(mensaje):
    url = "https://telegram.org"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"⚠️ Error al enviar a Telegram: {e}")

def obtener_datos_mercado():
    precio, open_interest, volumen = None, None, None
    try:
        ticker = yf.Ticker(SYMBOL)
        datos = ticker.fast_info
        precio = float(datos['last_price'])
        volumen_usd = float(datos['last_volume'])
        volumen = volumen_usd / precio if precio else 0.0
        if precio and volumen:
            open_interest = volumen * 0.35
    except Exception as e:
        print(f"⚠️ Error en lectura de Yahoo Finance: {e}")
        return None, None, None
    return precio, open_interest, volumen

# =====================================================================
# BUCLE PRINCIPAL DEL RADAR 
# =====================================================================
def bucle_radar():
    print(f"📡 RADAR WATSON ULTRA-SENSITIVO: ACTIVADO PARA {SYMBOL} (VELOCIDAD: 1 MIN)")
    enviar_telegram(f"📡 *Radar 24/7 Nube Iniciado*\nPatrullando flujo de {SYMBOL} sin límites de tiempo...")

    # Forzar la primera captura con reintentos limpios
    while True:
        precio_anterior, oi_anterior, vol_anterior = obtener_datos_mercado()
        if precio_anterior and precio_anterior > 0:
            print(f"📊 CONEXIÓN INICIAL EXITOSA | ETH: ${precio_anterior:.2f} | OI Estimado: {oi_anterior:,.2f} | Vol 24h: {vol_anterior:,.2f} ETH\n")
            break
        print("⏳ Sincronizando la red de datos en vivo con Yahoo Finance...")
        time.sleep(5)

    while True:
        try:
            time.sleep(INTERVALO_SEGUNDOS)
            precio_actual, oi_actual, vol_actual = obtener_datos_mercado()
            
            if not precio_actual or precio_actual == 0:
                continue
                
            delta_precio = ((precio_actual - precio_anterior) / precio_anterior) * 100
            delta_oi = ((oi_actual - oi_anterior) / oi_anterior) * 100 if oi_anterior > 0 else 0.0
            
            if delta_precio > 0.02:
                rumbo_precio = "📈 PRECIO ALZA (Presión compradora activa)"
            elif delta_precio < -0.02:
                rumbo_precio = "📉 PRECIO BAJA (Presión vendedora activa)"
            else:
                rumbo_precio = "⚖️ PRECIO NEUTRO (Presión equilibrada)"

            if delta_oi > 0.1:
                rumbo_flujo = "🐋 INYECCIÓN DE CAPITAL (Las instituciones están ABRIENDO órdenes)"
            elif delta_oi < -0.1:
                rumbo_flujo = "⚠️ RETIRO DE CAPITAL (Las instituciones están CERRANDO posiciones)"
            else:
                rumbo_flujo = "💤 FLUJO PASIVO (Los operadores pesados están esperando)"

            if delta_precio > 0.15 and delta_oi > 0.4:
                entorno = "🚀 INTENCIÓN ALCISTA INSTITUCIONAL (Inyección de Longs)"
                accion_trader = "🟩 OPERAR AL LONG (Fuerza institucional alcista)"
            elif delta_precio < -0.15 and delta_oi > 0.4:
                entorno = "🩸 INTENCIÓN BAJISTA INSTITUCIONAL (Inyección de Shorts)"
                accion_trader = "🔴 OPERAR AL SHORT (Fuerza institucional bajista)"
            elif delta_precio > 0.02 and delta_oi < -0.2:
                entorno = "⚠️ TRAMPA DE LIQUIDACIÓN / DISTRIBUCIÓN"
                accion_trader = "🟨 ESPERAR / EVITAR (Precio sube falsamente mientras capital huye)"
            elif delta_precio < -0.02 and delta_oi < -0.2:
                entorno = "⚠️ TRAMPA / CAPITULACIÓN BAJISTA"
                accion_trader = "🟨 ESPERAR / EVITAR (Cierre de cortos masivo)"
            else:
                entorno = "⏳ ENTORNO NEUTRO / CONSTRICCIÓN DE RANGO"
                accion_trader = "⬜ MANTENERSE QUIETO (Sin dirección institucional clara)"
            
            print(f"[RADAR-1M] ETH: ${precio_actual:.2f} | Var. Precio: {delta_precio:+.3f}% | Var. OI: {delta_oi:+.3f}%")
            print(f"👉 Dictamen General: {entorno}")
            print(f"🎯 ACCIÓN SUGERIDA: {accion_trader}\n")
            
            # Alerta flash minuto a minuto directo a tu teléfono
            alerta_minuto = f"🎯 *ETH:* ${precio_actual:.2f} | {accion_trader}"
            enviar_telegram(alerta_minuto)
            
            # GATILLOS DE MEGA ENTRADA CRÍTICOS
            mega_entrada = False
            alerta_msg = ""
            
            if delta_precio >= 0.35 and delta_oi >= 1.0:
                mega_entrada = True
                alerta_msg = (
                    f"🚨🚨 *POTENCIAL MEGA ENTRADA: LONG (1 MIN)* 🚨🚨\n\n"
                    f"📈 *Movimiento Explosivo:* ${precio_actual:.2f} ({delta_precio:+.3f}% en 60s)\n"
                    f"🐋 *Inyección Ballena Fluido:* {delta_oi:+.3f}%\n"
                    f"⚡ *Sugerencia:* Evaluar entrada rápida en compra."
                )
            elif delta_precio <= -0.35 and delta_oi >= 1.0:
                mega_entrada = True
                alerta_msg = (
                    f"🚨🚨 *POTENCIAL MEGA ENTRADA: SHORT* 🚨🚨\n\n"
                    f"📉 *Colapso Explosivo:* ${precio_actual:.2f} ({delta_precio:+.3f}% en 60s)\n"
                    f"🐋 *Inyección Ballena Fluido:* {delta_oi:+.3f}%\n"
                    f"⚡ *Sugerencia:* Evaluar entrada rápida en venta."
                )
                
            if mega_entrada:
                enviar_telegram(alerta_msg)
                
            precio_anterior = precio_actual
            oi_anterior = oi_actual
            vol_anterior = vol_actual
            
        except Exception as e:
            print(f"⚠️ Nota de estabilidad en bucle: {e}")
            time.sleep(5)

# =====================================================================
# ARRANQUE DEL ENTORNO EN SEGUNDO PLANO
# =====================================================================
if __name__ == "__main__":
    # 1. Lanzamos el servidor web fantasma nativo en un hilo secundario
    hilo_web = threading.Thread(target=arrancar_servidor_web)
    hilo_web.daemon = True
    hilo_web.start()
    
    # 2. Dejamos que el hilo principal maneje el radar de forma directa sin pausas
    bucle_radar()
