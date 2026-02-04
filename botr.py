import asyncio
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Pon tu token real aquí (no lo subas a GitHub ni lo compartas)
TOKEN = "8281053173:AAHXqZpmyYFULFZb1es6oEeLj-yTRAd9SDo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Este es un bot OSINT para verificar si un email está registrado en sitios web.\n\n"
        "Uso ético SOLO: verifica tu propio email o con consentimiento explícito.\n\n"
        "Comando:\n"
        "/check tuemail@ejemplo.com\n\n"
        "Ejemplo: /check test@gmail.com\n\n"
        "🔥 Uso educativo."
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /check email@ejemplo.com\nEj: /check test@gmail.com")
        return

    email = context.args[0]
    if "@" not in email:
        await update.message.reply_text("Email inválido. Debe tener @")
        return

    msg = await update.message.reply_text(f"Chequeando {email} con OSINT e-mail... ⏳\nPuede tardar 1-3 minutos por rate limits.")

    try:
        # Ejecuta Holehe con --only-used para mostrar solo los que existen + --no-color para parsear fácil
        cmd = ["holehe", email, "--only-used", "--no-color"]
        
        result = await asyncio.to_thread(
            subprocess.run,
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos máximo
        )

        if result.returncode != 0:
            await msg.edit_text(f"Error al ejecutar el bot:\n{result.stderr.strip()[:300]}")
            return

        output = result.stdout.strip()
        lines = output.splitlines()

        results = []
        for line in lines:
            line_clean = line.strip()
            if line_clean.startswith("[+]"):
                # Ejemplo: [+] Instagram → Exists
                site_part = line_clean.split("→")[0].replace("[+]", "").strip()
                results.append(f"✅ {site_part}")

        if not results:
            response = (
                f"No se encontraron sitios donde {email} esté registrado.\n"
                "Posibles causas:\n"
                "- Rate limit en muchos sitios\n"
                "- El email no está usado en los ~120 sitios que chequea OSINT e-mail\n"
                "- Prueba con otro email o espera unos minutos\n\n"
                "Output parcial para debug:\n" + output[:400] + "..."
            )
        else:
            response = f"📊 {email} está registrado en:\n\n" + "\n".join(results)

        await msg.edit_text(response)

    except subprocess.TimeoutExpired:
        await msg.edit_text("Tiempo excedido por rate limits. Prueba más tarde.")
    except Exception as e:
        await msg.edit_text(f"Error inesperado: {str(e)}\nVerifica que Holehe esté instalado: pip install --upgrade holehe")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
