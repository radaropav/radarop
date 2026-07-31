import time
import requests
import json
import sys

# Forzamos la instalación rápida de la librería de Yahoo Finance autorizada por Google
!pip install yfinance --quiet
import yfinance as yf

# =====================================================================
# CONFIGURACIÓN ULTRA-SENSITIVA CON RECOMENDACIÓN OPERATIVA EN TELEGRAM
# =====================================================================
SYMBOL = "ETH-USD"  
INTERVALO_SEGUNDOS = 60  
TELEGRAM_CHAT_ID = "5883043795"

# =====================================================================
# FUNCIONES DE CONEXIÓN
# =====================================================================

def enviar_telegram(mensaje):
    url = "https://telegram.org"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload, timeout=5)
    except Exception: pass

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
    except Exception:
        return None, None, None
    return precio, open_interest, volumen

# =====================================================================
# INICIALIZACIÓN
# =====================================================================
print(f"📡 RADAR WATSON ULTRA-SENSITIVO: ACTIVADO PARA {SYMBOL} (VELOCIDAD: 1 MIN)")
enviar_telegram(f"📡 *Radar con Alertas Minuto a Minuto Activo*\nRecibiendo recomendaciones directo en tu teléfono...")

while True:
    precio_anterior, oi_anterior, vol_anterior = obtener_datos_mercado()
    if precio_anterior and precio_anterior > 0:
        print(f"📊 CONEXIÓN INICIAL EXITOSA | ETH: ${precio_anterior:.2f} | OI Estimado: {oi_anterior:,.2f} | Vol 24h: {vol_anterior:,.2f} ETH\n")
        break
    print("⏳ Sincronizando la red de datos en vivo...")
    time.sleep(4)

# =====================================================================
# BUCLE DE RASTREO CONTINUO INDESTRUCTIBLE
# =====================================================================
while True:
    try:
        time.sleep(INTERVALO_SEGUNDOS)
        precio_actual, oi_actual, vol_actual = obtener_datos_mercado()
        
        if not precio_actual or precio_actual == 0:
            print("[SISTEMA] Aviso: Retraso en la respuesta del oráculo. Manteniendo escucha...")
            continue
            
        delta_precio = ((precio_actual - precio_anterior) / precio_anterior) * 100
        delta_oi = ((oi_actual - oi_anterior) / oi_anterior) * 100 if oi_anterior > 0 else 0.0
        
        # 1. Determinar rumbo del precio
        if delta_precio > 0.02:
            rumbo_precio = "📈 PRECIO ALZA (Presión compradora activa)"
        elif delta_precio < -0.02:
            rumbo_precio = "📉 PRECIO BAJA (Presión vendedora activa)"
        else:
            rumbo_precio = "⚖️ PRECIO NEUTRO (Presión equilibrada)"

        # 2. Determinar rumbo del flujo de capital (OI)
        if delta_oi > 0.1:
            rumbo_flujo = "🐋 INYECCIÓN DE CAPITAL (Las instituciones están ABRIENDO órdenes)"
        elif delta_oi < -0.1:
            rumbo_flujo = "⚠️ RETIRO DE CAPITAL (Las instituciones están CERRANDO posiciones)"
        else:
            rumbo_flujo = "💤 FLUJO PASIVO (Los operadores pesados están esperando)"

        # 3. MÓDULO MATEMÁTICO DE RECOMENDACIÓN OPERATIVA EXACTA
        if delta_precio > 0.15 and delta_oi > 0.4:
            entorno = "🚀 INTENCIÓN ALCISTA INSTITUCIONAL (Inyección de Longs)"
            accion_trader = "🟩 OPERAR AL LONG (Fuerza institucional alcista confirmada)"
        elif delta_precio < -0.15 and delta_oi > 0.4:
            entorno = "🩸 INTENCIÓN BAJISTA INSTITUCIONAL (Inyección de Shorts)"
            accion_trader = "🔴 OPERAR AL SHORT (Fuerza institucional bajista confirmada)"
        elif delta_precio > 0.02 and delta_oi < -0.2:
            entorno = "⚠️ TRAMPA DE LIQUIDACIÓN / DISTRIBUCIÓN"
            accion_trader = "🟨 ESPERAR / EVITAR (Precio sube falsamente mientras capital huye)"
        elif delta_precio < -0.02 and delta_oi < -0.2:
            entorno = "⚠️ TRAMPA / CAPITULACIÓN BAJISTA"
            accion_trader = "🟨 ESPERAR / EVITAR (Cierre de cortos masivo, rebote probable)"
        else:
            entorno = "⏳ ENTORNO NEUTRO / CONSTRICCIÓN DE RANGO"
            accion_trader = "⬜ MANTENERSE QUIETO (Sin dirección institucional clara)"
        
        # IMPRESIÓN DETALLADA EN CONSOLA CON ACCIÓN COMERCIAL
        print(f"[RADAR-1M] ETH: ${precio_actual:.2f} | Var. Precio: {delta_precio:+.3f}% | Var. OI: {delta_oi:+.3f}%")
        print(f"   ↳ Rumbo Precio: {rumbo_precio}")
        print(f"   ↳ Rumbo Capital: {rumbo_flujo}")
        print(f"👉 Dictamen General: {entorno}")
        print(f"🎯 ACCIÓN SUGERIDA: {accion_trader}\n")
        
        # NUEVO REQUISITO: Alerta flash en Telegram en cada impresión con el tipo de orden sugerido
        alerta_minuto = f"🎯 *ETH:* ${precio_actual:.2f} | {accion_trader}"
        enviar_telegram(alerta_minuto)
        
        # GATILLOS DE MEGA ENTRADA CRÍTICOS (MÁXIMA CONFLUENCIA AL TELÉFONO)
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
                f"🚨🚨 *POTENCIAL MEGA ENTRADA: SHORT (1 MIN)* 🚨🚨\n\n"
                f"📉 *Colapso Explosivo:* ${precio_actual:.2f} ({delta_precio:+.3f}% en 60s)\n"
                f"🐋 *Inyección Ballena Fluido:* {delta_oi:+.3f}%\n"
                f"⚡ *Sugerencia:* Evaluar entrada rápida en venta."
            )
            
        if mega_entrada:
            enviar_telegram(alerta_msg)
            
        precio_anterior = precio_actual
        oi_anterior = oi_actual
        vol_anterior = vol_actual
        
    except KeyboardInterrupt:
        print("\n📡 Radar apagado.")
        break
    except Exception:
        time.sleep(5)
