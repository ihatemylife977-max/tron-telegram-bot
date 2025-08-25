import os
import requests
import asyncio
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⛓ Tron Block Watcher started...")

def get_latest_block():
    url = "https://apilist.tronscanapi.com/api/block?sort=-number&limit=1"
    resp = requests.get(url).json()
    if "data" in resp and len(resp["data"]) > 0:
        blk = resp["data"][0]
        return blk["hash"], blk["number"]
    return None, None

async def monitor_blocks(app):
    last_block = None
    while True:
        blk_hash, blk_number = get_latest_block()
        if blk_hash and blk_number != last_block:
            last_block = blk_number
            text = f"🆕 Tron Block\n\n🔢 Block: {blk_number}\n🔗 Hash: {blk_hash}"
            await app.bot.send_message(chat_id=os.getenv("CHAT_ID"), text=text)
        await asyncio.sleep(3)

if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    async def main():
        await app.initialize()
        await app.start()
        asyncio.create_task(monitor_blocks(app))
        await app.updater.start_polling()
        await app.stop()

    asyncio.run(main())
