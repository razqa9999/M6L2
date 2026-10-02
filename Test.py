import os
import time
import urllib.parse
import requests
import discord
from discord.ext import commands

# =====================================================================
# 1. PENGISIAN TOKEN DISCORD (Token Anda Sudah Aman Di Sini)
# =====================================================================
DISCORD_TOKEN = "YOUR TOKEN BOT"

# =====================================================================
# 2. KONFIGURASI BOT DISCORD
# =====================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Kriteria 1: Program dapat dijalankan!")
    print(f"✅ Bot berhasil login sebagai: {bot.user.name}")
    print("👉 Silakan ketik '!gambar [deskripsi]' di server Discord Anda.")

# =====================================================================
# 3. PERINTAH UNTUK MEMBUAT GAMBAR (GRATIS TANPA API KEY AI)
# =====================================================================
@bot.command()
async def gambar(ctx, *, prompt_user):
    await ctx.send(f"🔄 Menyiapkan data... Memproses prompt: *\"{prompt_user}\"*")

    # Alternatif gratis tanpa API key: Pollinations
    prompt_aman = urllib.parse.quote(prompt_user)
    URL_ENDPOINT = f"https://image.pollinations.ai/prompt/{prompt_aman}?width=1024&height=1024&nologo=true"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = None

    print("\n🚀 Mengirimkan request ke server AI lewat internet...")
    for attempt in range(3):
        try:
            response = requests.get(URL_ENDPOINT, headers=headers, timeout=60)
            print(f"✅ Kriteria 2: Python berhasil mengirim request. Percobaan {attempt + 1}/3")
            if response.status_code == 200:
                break
            if response.status_code in (500, 502, 503, 504):
                print(f"⚠️ Server AI sedang timeout. Mengulang... ({attempt + 1}/3)")
                time.sleep(2 ** attempt)
                continue
            break
        except Exception as e:
            if attempt < 2:
                print(f"⚠️ Koneksi gagal, retrying... ({attempt + 1}/3): {e}")
                time.sleep(2 ** attempt)
                continue
            await ctx.send(f"❌ Kriteria 2 Gagal: Koneksi ke server AI terputus: {e}")
            return

    if response is None:
        return

    if response.status_code == 200:
        print("✅ Kriteria 3: AI berhasil menerima request (200 OK).")
        print("✅ Kriteria 4: AI berhasil menghasilkan gambar.")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(BASE_DIR, exist_ok=True)
        nama_file = os.path.abspath(os.path.join(BASE_DIR, "temp_discord_image.png"))
        konten_gambar = response.content

        try:
            with open(nama_file, "wb") as file:
                file.write(konten_gambar)

            print("✅ Kriteria 5: Gambar berhasil disimpan lokal.")

            await ctx.send(file=discord.File(nama_file))
            await ctx.send("🎉 Gambar dari AI berhasil dibuat dan ditampilkan di Discord Anda!")
        finally:
            if os.path.exists(nama_file):
                os.remove(nama_file)
    else:
        print(f"❌ AI menolak request. Status: {response.status_code}")
        await ctx.send(
            "❌ Server AI sedang bermasalah atau prompt terlalu berat. "
            "Coba lagi dalam beberapa detik dengan prompt yang lebih singkat."
        )

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
