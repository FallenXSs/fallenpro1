import telebot
import random
import requests
from telebot import types
import keyboard
from datetime import datetime
import requests

bot = telebot.TeleBot("6086089724:AAELu6YRS_U0JuJMmWPyhtnBMWJ18iOnPRY") 

print("Fallen Is Onnline")
print("Bot @FallenSorguBot 🌱")
print("Bot Sahibi @Fivist 👨‍💻")

bot_password = "YakupVoid"

bot_owner_chat_id =5638708289

sudo_users = [5638708289]

yakup = "BURAYA APİ"
srgAdres = "BURAYA APİ"
vesika = "BURAYA APİ"

logged_in_users = {}
banned_users = {}

@bot.message_handler(commands=['help'])
def send_help_message(message):
    username = message.from_user.first_name
    response_message = f"Merhaba {username}! bunlar benim komutlarım:\n\n" \
               "/tcpro - tcpro Sorgu Atar\n\n" \
               "/adres - adres sorgu atar\n\n" \
               "/vesika - aol vesika sorgu atar\n\n" \
               "/join - Grup ve yeniliklerin bulunduğu kanala katılmak için\n\n" \
               "ver: 2.5 NOT: 📋 Bu bot daha geliştirme aşamasında!\n\n"
    bot.reply_to(message, response_message)

def save_banned_users():
    with open("yasakli_kisiler.txt", "w") as file:
        for user_id, reason in banned_users.items():
            file.write(f"{user_id} {reason}\n")

def load_banned_users():
    try:
        with open("yasakli_kisiler.txt", "r") as file:
            for line in file:
                user_id, reason = line.strip().split(" ", 1)
                banned_users[int(user_id)] = reason
    except FileNotFoundError:
        pass

load_banned_users()

@bot.message_handler(func=lambda message: message.new_chat_members)
def welcome_new_members(message):
    for member in message.new_chat_members:
        if member.id in banned_users:
            bot.kick_chat_member(message.chat.id, member.id)
            bot.send_message(message.chat.id, f"Fallen Yasaklı Üyesiniz {member.first_name} !\n\nYasaklanma Sebebi: {banned_users[member.id]}")
        else:
            bot.send_message(message.chat.id, f"Hoş geldin reyiz {member.first_name}!")
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id in banned_users:
        bot.reply_to(message, "Fallen Yasaklı Üyesiniz.\n\nYasaklanma Sebebi: " + banned_users[user_id])
    else:
        bot.reply_to(message, "🌱 Hoşgeldin reyiz, Fallen Project hizmetlerini kullanarak, kanal kısımında bulunan sözleşmeyi kabul etmiş sayılırsınız! @FallenPro\n\nBu bot tamamen ücretsizdir! botu satan kişilere itibar etmeyin komutlar için /help")

GROUP_ID = -1001916631331

def send_log_to_group(username, name, start_time):
    message = f"Bot başlatıldı:\nKullanıcı Adı: {username}\nAdı: {name}\nBaşlatma Saati: {start_time}"
    bot.send_message(GROUP_ID, message)

# Bot'u başlatan kişinin kullanıcı adını ve adını alıp send_log_to_group() fonksiyonunu çağıran event handler
@bot.message_handler(commands=['start']) 
def handle_start(message):
    username = message.from_user.username
    name = message.from_user.first_name
    start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
    send_log_to_group(username, name, start_time)

@bot.message_handler(commands=['wban'])
def ban_user(message):
    if message.from_user.id not in sudo_users:
        bot.reply_to(message, "Siktir Git Bot Sahibine Yaz.")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Yanlış komut Kullanımı Örnek: /wban <id> <sebep>")
        return

    user_id = int(args[1])
    reason = "Fallen kullanıcı sözleşmesi kurallarına aykırı!" if len(args) < 3 else " ".join(args[2:])

    banned_users[user_id] = reason
    save_banned_users()
    bot.reply_to(message, f"Kullanıcı {user_id} yasaklandı.\n\nYasaklanma Sebebi: {reason}")

@bot.message_handler(commands=['unwban'])
def unban_user(message):
    if message.from_user.id not in sudo_users:
        bot.reply_to(message, "Siktir Git Bot Sahibine Yaz.")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Yanlış Komut Kullanımı /unwban ID")
        return

    user_id = int(args[1])
    if user_id in banned_users:
        del banned_users[user_id]
        save_banned_users()
        bot.reply_to(message, f"Kullanıcının yasağı kaldırıldı: {user_id}")
    else:
        bot.reply_to(message, f"Bu kullanıcı zaten yasaklı değil: {user_id}")

@bot.message_handler(commands=["gen"])
def generate_password(message):
    if message.chat.id != bot_owner_chat_id:
        bot.send_message(message.chat.id, "Bu komutu kullanmak için bot sahibi olmanız gerekiyor.")
        return
        

    new_password = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(16))
    global bot_password
    bot_password = new_password
    bot.send_message(message.chat.id, f"Başarılı!✨ Anahtar Oluşturuldu: {new_password}")


@bot.message_handler(commands=["login"])
def login_command(message):
    if message.chat.id in logged_in_users:
        bot.send_message(message.chat.id, "zaten giriş yapmışsın komutlar için /help")
        return
        
 
    bot.send_message(message.chat.id, "Lütfen Size Verilen Anahtarı Girin:")
    bot.register_next_step_handler(message, check_password)


def check_password(message):
    user_id = message.chat.id
    if message.text == bot_password:
        logged_in_users[user_id] = True
        bot.send_message(user_id, "Giriş başarılı.💸")
    else:
        bot.send_message(user_id, "Key Hatalı Yada Silinmiş Yeni Key Almak için @BenYakup")


@bot.message_handler(commands=['tcpro'])
def handle_tcpro_command(message):

    command_params = message.text.split()
    if len(command_params) != 2:
        bot.reply_to(message, "Hatalı komut kullanımı\nörnek:\n\n/tcpro 11111111110")
        return
    
    tc_no = command_params[1]
    
    response = requests.get(yakup.format(tc_no))
    
    if response.status_code == 200:
        try:
            json_data = response.json()
            if json_data:
                tc = json_data[0].get("Tc", "")
                ad = json_data[0].get("Adı", "")
                soyad = json_data[0].get("Soyadı", "")
                dogum_tarihi = json_data[0].get("Doğum Tarihi", "")
                dogum_yeri = json_data[0].get("Doğum Yeri", "")
                anne_adi = json_data[0].get("Anne Adı", "")
                baba_adi = json_data[0].get("Baba Adı", "")
                sira_no = json_data[0].get("Sıra No", "")
                aile_sira_no = json_data[0].get("Aile Sıra No", "")
                cilt_no = json_data[0].get("Cilt No", "")
                olum_tarihi = json_data[0].get("Ölüm Tarihi", "Belirtilmemiş")

                reply_message = f"""╔═══════════════
╟ @FallenSorguBot
╚═══════════════
╔═══════════════
╟ TC: {tc}
╟ AD: {ad}
╟ SOYAD: {soyad}
╟ DOĞUM TARİHİ: {dogum_tarihi}
╟ DOĞUM YERİ: {dogum_yeri}
╟ ANNE ADI: {anne_adi}
╟ BABA ADI: {baba_adi}
╟ SIRA NO: {sira_no}
╟ AİLE SIRA NO: {aile_sira_no}
╟ CİLT NO: {cilt_no}
╟ ÖLÜM TARİHİ: {olum_tarihi}
╚═══════════════"""
                bot.reply_to(message, reply_message)
            else:
                bot.reply_to(message, "TC kimlik numarası bulunamadı.")
        except ValueError:
            bot.reply_to(message, "API IS ERROR! 404.")
    else:
        bot.reply_to(message, "Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
        
@bot.message_handler(commands=['adres'])
def handle_tcpro_command(message):

    command_params = message.text.split()
    if len(command_params) != 2:
        bot.reply_to(message, "Hatalı komut kullanımı\nörnek:\n\n/adres 11111111110")
        return
    
    tc_no = command_params[1]
    
    response = requests.get(srgAdres.format(tc_no))
    
    if response.status_code == 200:
        try:
            json_data = response.json()
            if json_data:
                tc = json_data[0].get("Tc", "")
                isim = json_data[0].get("İsim", "")
                soyadi = json_data[0].get("Soyadı", "")
                dogumtarihiyil = json_data[0].get("Doğum Tarihi", "")
                adres = json_data[0].get("Adres", "")

                reply_message = f"""╔═══════════════
╟ @FallenSorguBot
╚═══════════════
╔═══════════════
╟ TC: {tc}
╟ AD: {ad}
╟ Soyadı: {soyadi}
╟ DOĞUM Tarihi: {dogumtarihiyil}
╟ ADRES: {adres}
╚═══════════════"""
                bot.reply_to(message, reply_message)
            else:
                bot.reply_to(message, "TC kimlik numarası bulunamadı.")
        except ValueError:
            bot.reply_to(message, "API error 404 not found ERROR!.")
    else:
        bot.reply_to(message, "Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")

        
@bot.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.from_user.id
    if user_id in sudo_users:
        bot.reply_to(message, 'Merhaba Yöneticim!💫 İşte komutlarınız:\n\n/wban - Kullanıcıyı Bottan Yasaklarım\n/unwban - Yasağı Kaldırırım\n/gen - Yeni Key Oluştururum')
    else:
        
        bot.reply_to(message, 'Bu Komutu Kullanmaya İznin Yok.🤬') 
        
@bot.message_handler(commands=['join'])
def send_join_buttons(message):
    # İki tane buton oluşturun
    keyboard = types.InlineKeyboardMarkup()
    group_button = types.InlineKeyboardButton("Support⛑️", url="t.me/MajesteTr")
    channel_button = types.InlineKeyboardButton("News Channel🆕", url="t.me/FallenPro")
    fed_button = types.InlineKeyboardButton("Sohbet Grubum", url="t.me/FallenTr")
    keyboard.row(group_button, channel_button, fed_button)
    bot.send_message(message.chat.id, "Yeniliklerden haberdar olmak için katılın💌!", reply_markup=keyboard)
    
@bot.message_handler(commands=['developer', 'dev'])
def send_developer_buttons(message):
     # İki tane buton oluşturun
     keyboard = types.InlineKeyboardMarkup()
     dev_button = types.InlineKeyboardButton("Owner :)", url="t.me/Fivist")
     keyboard.row(dev_button)
     bot.send_message(message.chat.id, "Onunla tanışmaya ne dersin?", reply_markup=keyboard)

@bot.message_handler(commands=['stats'])
def get_stats(message):
    user_id = message.from_user.id

    if user_id in sudo_users:
        # Botunuzun bulunduğu grupları ve kanalları alın
        chat_list = bot.get_chat_member_groups(user_id)

        # Yanıtı oluşturun
        response = f"Merhaba yöneticim, işte bulunduğum gruplar ve kanallar:\n"

        for chat in chat_list:
            response += f"- {chat.title}\n"

        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "Üzgünüm, bu komutu kullanmaya yetkiniz yok.")

bot.polling()
