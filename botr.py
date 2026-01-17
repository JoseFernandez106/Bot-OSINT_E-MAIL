  GNU nano 8.7                                                             botr.py
#!/usr/bin/env python3
"""
🖼️ BOT REMOVEDOR DE FONDOS CON API
Usa remove.bg - Calidad profesional
Sin necesidad de OpenCV en Termux
"""

import os
import io
import logging
import requests
from PIL import Image
from datetime import datetime

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== CONFIGURACIÓN ====================
TOKEN = "7269948379:AAEZ8PmZ55CN_CqbqmWcAMUzXycxZvP9jug"

# 🔑 TU API KEY DE REMOVE.BG - CONSIGUELA EN: https://www.remove.bg/api
API_KEY = "zNCN4mb9xLWHPMK8vzAScnXC"  # <-- REEMPLAZA CON TU KEY
API_URL = "https://api.remove.bg/v1.0/removebg"

os.makedirs("procesadas", exist_ok=True)

class BotRemoveBgAPI:
    def __init__(self, token, api_key):
        self.token = token
        self.api_key = api_key
        self.contador = 0
        self.errores = 0

        # Verificar si la API key está configurada
        if api_key == "zNCN4mb9xLWHPMK8vzAScnXC":
            logger.warning("⚠️ API KEY NO CONFIGURADA - Usa: https://www.remove.bg/api")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        user = update.effective_user

        # Verificar API key
        if self.api_key == "zNCN4mb9xLWHPMK8vzAScnXC":
            mensaje = """
⚠️ *BOT NO CONFIGURADO COMPLETAMENTE*

El bot necesita una *API Key* para funcionar.

*📋 PASOS PARA CONFIGURAR:*
1. Ve a: https://www.remove.bg/api
2. Regístrate (gratis)
3. Copia tu API Key
4. Ábreme el archivo `bot_remove_api.py`
5. Busca: `API_KEY = "zNCN4mb9xLWHPMK8vzAScnXC"`
6. Reemplázalo con tu key real

*🎁 PLAN GRATIS:* 50 imágenes/mes
*💎 PLAN PAGO:* Desde $0.20 por imagen

*Ejemplo de key:* `vT7PcR4sE8qJ9wM2nB5gY8hK3`

¡Configúrame y estaré listo!
            """
        else:
            mensaje = f"""
🖼️ *BOT REMOVEDOR DE FONDOS PROFESIONAL*

¡Hola {user.first_name}! Usamos *remove.bg* (IA profesional).

*🎯 CARACTERÍSTICAS:*
• ✅ Calidad profesional (IA entrenada)
• ✅ Rápido (2-5 segundos)
• ✅ Soporta cualquier fondo
• ✅ Sin instalar librerías pesadas

*📸 ¿CÓMO FUNCIONA?*
1. Envíame *cualquier* imagen
