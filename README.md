from telethon import TelegramClient, events
import json
import os

api_id = 26887744  # << جایگزین کن
api_hash = '9ba167ea51da5b7ad762bedc7e4545f6'  # << جایگزین کن
admin_id = 7824772776  # << آیدی عددی خودت

client = TelegramClient('session', api_id, api_hash)

# فایل ذخیره اطلاعات کاربران
STORAGE_FILE = "users.json"

# بارگذاری اطلاعات قبلی
if os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "r") as f:
        known_users = json.load(f)
else:
    known_users = {}

@client.on(events.NewMessage(chats=None))
async def catch_user(event):
    sender = await event.get_sender()
    if not sender or sender.bot:
        return

    user_id = str(sender.id)
    if user_id in known_users:
        return  # کاربر قبلاً ثبت شده

    # اطلاعات کاربر
    full_name = ((sender.first_name or '') + ' ' + (sender.last_name or '')).strip()
    username = sender.username or ''
    
    known_users[user_id] = {
        "name": full_name,
        "username": username
    }

    with open(STORAGE_FILE, "w") as f:
        json.dump(known_users, f, indent=2)

    msg = (
        "کاربر جدید شناسایی شد:\n\n"
        f"نام: {full_name or '---'}\n"
        f"یوزرنیم: @{username}" if username else "یوزرنیم: ندارد" + "\n"
        f"آیدی عددی: {user_id}"
    )

    await client.send_message(admin_id, msg)

async def main():
    await client.send_message(admin_id, "یوزربات روشنه و منتظره ببینه کی تو گروه پیام میده...")
    await client.run_until_disconnected()

client.start()
client.loop.run_until_complete(main())
