from telethon import TelegramClient, events import asyncio import json import os

api_id = 22340540 api_hash = '264130c425cb6a107c99fa8c4155a078' admin_id = 7824772776

client = TelegramClient('session', api_id, api_hash)

پاک‌سازی فایل کاربران قبلی

with open("known_users.json", "w") as f: f.write("{}")

known_users = {} usernames_to_send = []

def save_users(): with open("known_users.json", "w") as f: json.dump(known_users, f, indent=2)

اسکن پیام‌ها به صورت مرحله‌ای با offset_id

async def scan_all_groups(): global usernames_to_send async for dialog in client.iter_dialogs(): if dialog.is_group: entity = dialog.entity try: print(f"شروع اسکن گروه: {entity.title}") offset_id = 0 total_new_users = 0

while True:
                messages = await client.get_messages(entity, limit=100, offset_id=offset_id, reverse=True)
                if not messages:
                    break

                for msg in messages:
                    sender = await msg.get_sender()
                    if not sender or sender.bot:
                        continue

                    user_id = str(sender.id)
                    username = sender.username
                    full_name = ((sender.first_name or '') + ' ' + (sender.last_name or '')).strip()

                    if not username or user_id in known_users:
                        continue

                    known_users[user_id] = {
                        "username": username,
                        "name": full_name
                    }
                    usernames_to_send.append(f"@{username} ({full_name or '---'})")
                    total_new_users += 1

                offset_id = messages[-1].id
                await asyncio.sleep(0.5)  # جلوگیری از flood

            print(f"تعداد کاربران با یوزرنیم در {entity.title}: {total_new_users}")

        except Exception as e:
            print(f"خطا در گروه {entity.title}: {e}")

save_users()

ارسال لیست ۵۰تایی‌ها

async def send_usernames_list(): batches = [usernames_to_send[i:i+50] for i in range(0, len(usernames_to_send), 50)] total_batches = len(batches)

await client.send_message(admin_id, f"در مجموع {total_batches} لیست ۵۰تایی آماده شده.")

for i, batch in enumerate(batches):
    msg = f"لیست {i + 1}:\n\n" + "\n".join(batch)
    await client.send_message(admin_id, msg)
    await asyncio.sleep(10)

return True

پایش زنده کاربران جدید

@client.on(events.NewMessage) async def live_watch(event): sender = await event.get_sender() if not sender or sender.bot: return

user_id = str(sender.id)
if user_id not in known_users:
    username = sender.username
    full_name = ((sender.first_name or '') + ' ' + (sender.last_name or '')).strip()
    if username:
        known_users[user_id] = {
            "username": username,
            "name": full_name
        }
        save_users()

اجرای اصلی

async def main(): await client.send_message(admin_id, "شروع اسکن همه پیام‌های گروه‌ها از پایین‌ترین پیام...")

await scan_all_groups()

count = len(usernames_to_send)
await client.send_message(admin_id, f"تعداد یوزرنیم‌های منحصربه‌فرد پیدا شده: {count}")

if count == 0:
    await client.send_message(admin_id, "هیچ یوزرنیمی پیدا نشد.")
    return

await client.send_message(admin_id, "ارسال لیست‌ها آغاز شد...")
await send_usernames_list()
await client.send_message(admin_id, "ارسال تموم شد. پایش زنده فعاله.")

await client.run_until_disconnected()

client.start() client.loop.run_until_complete(main())
