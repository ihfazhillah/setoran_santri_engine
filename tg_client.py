#pylint: disable=c0330, w0613

"""Telegram client untuk interaksi dengan setoran_santri_engine"""



import logging
from datetime import datetime
from telegram import KeyboardButton, ReplyKeyboardMarkup
from tg_config import tg_token, admin_ids
from setoran_models import check_startend_format
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from setoran_models import *
from db_config import db
from query_setoran import (get_sudah_free, get_belum_setor, get_belum_murojaah,
get_sudah_murojaah_harus_ulang, get_sudah_tambah_harus_ulang, get_belum_tambah
)
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

# STATES
START, START_PROCESS, LIHAT, TAMBAH, TAMBAH_NAMA_SANTRI, PERSETUJUAN_SAVE_SANTRI, CARI_NAMA_SANTRI, PROCESS_END, PROCESS_JENIS, PROCESS_LULUS, PROCESS_PERSETUJUAN_SETORAN, PROCESS_START, PROCESS_LIHAT, BELUM = range(14)

# CONSTANS
ADMIN_IDS = admin_ids
TG_TOKEN = tg_token
CONTEXT = dict()

# CUSTOM KEYBOARDS
reply_start = [[KeyboardButton("👀 Lihat"), KeyboardButton("➕ Tambah")]]
reply_tambah = [[KeyboardButton("Santri"), KeyboardButton("Setoran")]]
reply_persetujuan = [[KeyboardButton("✔ Simpan"), KeyboardButton("✖ Jangan")]]
reply_jenis = [[KeyboardButton("➕ Tambah Baru"), KeyboardButton("♻ Murojaah")]]
reply_lulus = [[KeyboardButton("👍 Lulus"), KeyboardButton("👎 Ulang Lagi")]]
reply_lihat = [[KeyboardButton("📃 Daftar Santri"), KeyboardButton("📚 Daftar Surat")],
               [KeyboardButton("👏 Free"), KeyboardButton("⛔ Belum")]]
reply_belum = [[KeyboardButton("Setoran")],
               [KeyboardButton("♻ Murojaah"), KeyboardButton("➕ Tambah Baru")],
               [KeyboardButton("Murojaah sudah, harus ulang")],
               [KeyboardButton("Tambah sudah, harus ulang")]]

def start(bot, update):
    if update.message.chat_id in ADMIN_IDS:
        update.message.reply_text("Ini adalah start text, tidak ada lebih",
            reply_markup=ReplyKeyboardMarkup(reply_start, 
                                             one_time_keyboard=True,
                                             resize_keyboard=True))

        return START_PROCESS
    else:
        update.message.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")

def process_start(bot, update):
    if update.message.chat_id in ADMIN_IDS:
        message = update.message.text
        if message == "➕ Tambah":
            update.message.reply_text("Santri/Setoran",
                reply_markup=ReplyKeyboardMarkup(reply_tambah,
                    one_time_keyboard=True,
                    resize_keyboard=True))
            
            return TAMBAH

        elif message == "👀 Lihat":
            update.message.reply_text("mau lihat apa?",
                reply_markup=ReplyKeyboardMarkup(reply_lihat,
                    one_time_keyboard=True,
                    resize_keyboard=True))
            
            return LIHAT
        else:
            update.message.reply_text("Saya tidak faham pesan anda")
            return ConversationHandler.END
    else:
        update.message.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")


def process_tambah(bot, update):
    if update.message.chat_id in ADMIN_IDS:
        message = update.message.text

        if message == 'Santri':
            update.message.reply_text("Masukkan nama santri baru. Usahakan Uniq")
            return TAMBAH_NAMA_SANTRI

        elif message == 'Setoran':
            update.message.reply_text("Silahkan masukkan nama santri yang setoran")
            return CARI_NAMA_SANTRI
        else:
            update.message.reply_text("Saya tidak faham pesan anda")
            return START
    else:
        update.message.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")


def process_tambah_nama_santri(bot, update):
    message = update.message.text
    chat_id = update.message.chat_id 

    if chat_id in ADMIN_IDS:
        # check sudah ada belum namanya
        with db_session:
            nama = get(s for s in Santri if s.nama == message)
            if nama:
                update.message.reply_text("Silahkan masukkan nama yang lainnya. {} sudah ada".format(message))
                return TAMBAH_NAMA_SANTRI

        CONTEXT[chat_id] = {'santri': {'nama': message}}
        update.message.reply_text("Data yang kamu masukkan:\nNama Santri: %s"%(CONTEXT[chat_id]['santri']['nama']),
            reply_markup=ReplyKeyboardMarkup(reply_persetujuan,
                resize_keyboard=True,
                one_time_keyboard=True))
        return PERSETUJUAN_SAVE_SANTRI
    else:
        update.message.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")


def process_persetujuan_save_santri(bot, update):
    message = update.message.text
    chat_id = update.message.chat_id

    if chat_id in ADMIN_IDS:
        if message == "✔ Simpan":
            data_nama = CONTEXT[chat_id]['santri']['nama']
            # menyimpan nama
            with db_session:
                Santri(nama=data_nama)
                commit()

            update.message.reply_text("Santri dengan nama *%s* berhasil"
                                      " disimpan kedatabase" %(data_nama),
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    resize_keyboard=True,
                    one_time_keyboard=True))
            return START 
        elif message == "✖ Jangan":
            data_nama = CONTEXT[chat_id]['santri']['nama']

            update.message.reply_text("Data %s akan kami hapus" %(data_nama),
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    resize_keyboard=True,
                    one_time_keyboard=True))
            return START 
        else:
            update.message.reply_text("Saya tidak faham pesan anda",
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    resize_keyboard=True,
                    one_time_keyboard=True))
            return START
        data_nama = CONTEXT[chat_id]['santri']['nama']
        del data_nama
    else:
        update.message.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")

def process_cari_nama_santri(bot, update):
    message = update.message.text 
    chat_id = update.message.chat_id

    if chat_id in ADMIN_IDS:
        # cari nama , santri adalah object dari pencarian
        with db_session:
            nama = get(s for s in Santri if s.nama == message)

            if not nama:
                update.message.reply_text("Maaf, {} yang kamu cari tidak ditemukan "
                    "Silahkan masukkan pencarian lain".format(message))
                return CARI_NAMA_SANTRI
 
        CONTEXT[chat_id] = {'setoran': {'santri': message}}

        update.message.reply_text("Berikutnya, masukkan start, nosurat/ayat\n"
                                  "(Permulaan setoran)\n"
                                  "Contoh = alfatihah ayat 1 ==>  1/1")

        return PROCESS_START

    else:
        update.message.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")


def process_start_setor(bot, update):
    message = update.message.text
    chat_id = update.message.chat_id

    if chat_id in ADMIN_IDS:
        if check_startend_format(message):
            CONTEXT[chat_id]['setoran']['start'] = message

            update.message.reply_text("Kemudian, masukkan end, nosurat/ayat\n"
                                      "(akhir dari setoran)\n"
                                      "Contoh = alfatihah ayat 7 ==> 1/7")

            return PROCESS_END
        else:
            update.message.reply_text("Maaf, format yang anda masukkan salah. "
                "silahkan ulangi masukan start (permulaan setoran)")
            return PROCESS_START
    else:
        update.messasge.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")

def process_end_setor(bot, update):
    message = update.message.text
    chat_id = update.message.chat_id 

    if chat_id in ADMIN_IDS:
        if check_startend_format(message):
            CONTEXT[chat_id]['setoran']['end'] = message 

            update.message.reply_text("Pilih jenis setoran, murojaah atau tambah", reply_markup=ReplyKeyboardMarkup(reply_jenis,
                one_time_keyboard=True,
                resize_keyboard=True))

            return PROCESS_JENIS

        else:

            update.message.reply_text("Maaf, format yang anda masukkan salah."
                " silahkan ulang masukan end (akhir setoran)")

            return PROCESS_END

    else:
        update.massage.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")


def process_jenis_setor(bot, update):
    message = update.message.text 
    chat_id = update.message.chat_id

    if chat_id in ADMIN_IDS:
        
        if message == "➕ Tambah Baru":
            CONTEXT[chat_id]['setoran']['jenis'] = 'tambah'

            update.message.reply_text("Tambah dia lulus atau tidak? ",
                reply_markup=ReplyKeyboardMarkup(reply_lulus,
                    one_time_keyboard=True,
                    resize_keyboard=True))

            return PROCESS_LULUS
        elif message == "♻ Murojaah":
            CONTEXT[chat_id]['setoran']['jenis'] = 'murojaah'

            update.message.reply_text("Murojaah dia lulus atau tidak? ",
                reply_markup=ReplyKeyboardMarkup(reply_lulus,
                    one_time_keyboard=True,
                    resize_keyboard=True))

            return PROCESS_LULUS

        else:
            update.message.reply_text("Maaf, masukan salah")

            return PROCESS_JENIS 

    else:
        update.massage.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")

def process_lulus_setor(bot, update):
    message = update.message.text 
    chat_id = update.message.chat_id 

    pilihan = {'👍 Lulus': True,
                '👎 Ulang Lagi': False}

    
    if chat_id in ADMIN_IDS:
        if message in pilihan:
            CONTEXT[chat_id]['setoran']['lulus'] = pilihan[message]

            text = """Data yang anda masukkan:
            Nama santri : {nama}
            Setoran : {setoran}
            Jenis : {jenis}
            Lulus : {lulus}

            Yakin mau save ?
            """.strip()

            context = CONTEXT[chat_id]['setoran']
            context['timestamp'] = datetime.now()

            update.message.reply_text(text.format(nama=context['santri'],
                                                  setoran=context['start'] + "-" + context['end'],
                                                  jenis=context['jenis'],
                                                  lulus=context['lulus']),
            reply_markup=ReplyKeyboardMarkup(reply_persetujuan,
                one_time_keyboard=True,
                resize_keyboard=True))

            return PROCESS_PERSETUJUAN_SETORAN
            
        else:
            update.message.reply_text("Maaf, masukan salah")

            return PROCESS_LULUS

    else:
        update.massage.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")

@db_session
def process_persetujuan_setor(bot, update):
    message = update.message.text 
    chat_id = update.message.chat_id
    data_setoran = CONTEXT[chat_id]['setoran']


    if chat_id in ADMIN_IDS:
        if message == "✔ Simpan":
            # process simpan
            # with db_session:
            nama = get(s for s in Santri if s.nama == data_setoran['santri'])
            data_setoran['santri'] = nama
            Setoran(**data_setoran)
            commit()

            update.message.reply_text("Data yang anda masukkan telah kami simpan",
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    one_time_keyboard=True,
                    resize_keyboard=True))

            del data_setoran

            return START 

        elif message == "✖ Jangan":

            update.message.reply_text("Data yang anda masukkan akan kami delete",
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    one_time_keyboard=True,
                    resize_keyboard=True))

            del data_setoran

            return START
        else:

            update.message.reply_text("Maaf, masukan salah",
                reply_markup=ReplyKeyboardMarkup(reply_persetujuan,
                    one_time_keyboard=True,
                    resize_keyboard=True))

            return PROCESS_PERSETUJUAN_SETORAN
    else:
        update.massage.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")


def lihat(bot, update):
    message = update.message

    if message.chat_id in ADMIN_IDS:
        update.message.reply_text("Mau lihat apa ???",
            reply_markup=ReplyKeyboardMarkup(reply_lihat,
                one_time_keyboard=True,
                resize_keyboard=True))
        return PROCESS_LIHAT
    else:
        update.massage.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")

@db_session
def process_lihat(bot, update):
    message = update.message.text 
    chat_id = update.message.chat_id

    if chat_id in ADMIN_IDS:
        if message == "📃 Daftar Santri":
            santri = select(s for s in Santri)
            body = "DAFTAR SANTRI\n"
            body += "Jumlah Santri terdaftar %s" %(count(santri))
            body += "\n\n"
            santri_text = "{nama}({jml_setoran})"
            santri_ = [santri_text.format(nama=s.nama, jml_setoran=count(s.setorans)) for s in santri]
            body += "\n".join(santri_)
            update.message.reply_text(body,
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    one_time_keyboard=True,
                    resize_keyboard=True))
            return START

        elif message == "📚 Daftar Surat":
            update.message.reply_text("Not implemented",
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    one_time_keyboard=True,
                    resize_keyboard=True))
            return START
        elif message == "👏 Free":
            santri = get_sudah_free()
            body = "DAFTAR SANTRI TANPA TANGGUNGAN\n"
            body += "sudah setoran dan lulus\n"
            body += "baik murojaah maupun tambah\n"
            santri_ = ["{nama}({jml_setoran})".format(nama=s.nama, jml_setoran=count(s.setorans)) for s in santri] or ['Tidak ditemukan']
            body += "\n".join(santri_)

            update.message.reply_text(body,
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    one_time_keyboard=True,
                    resize_keyboard=True))
            return START 

        elif message == "⛔ Belum":
            update.message.reply_text("Belum apa ??",
                reply_markup=ReplyKeyboardMarkup(reply_belum,
                    one_time_keyboard=True,
                    resize_keyboard=True))
            return BELUM
        else:
            update.message.reply_text("Maaf, kami tidak tahu apa yang kamu mau...!!")
            return START
    else:
        update.message.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")

@db_session
def process_belum(bot, update):

    message = update.message.text 
    chat_id = update.message.chat_id

    if chat_id in ADMIN_IDS:
        if message == "Setoran":
            santri = get_belum_setor()
            body = "Daftar Santri belum setor (%s)" %count(santri)
            body += "\n\n"
            santri_ = [s.nama for s in santri]
            body += "\n".join(santri_)
            body += "\n"

            update.message.reply_text(body, 
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    one_time_keyboard=True,
                    resize_keyboard=True))

            return START
        elif message == "♻ Murojaah":
            santri = get_belum_murojaah()
            body = "Daftar santri belum murojaah (%s)" %count(santri)
            body += "\n\n"
            santri_ = [s.nama for s in santri]
            body += "\n".join(santri_)
            body += "\n"

            update.message.reply_text(body,
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    one_time_keyboard=True,
                    resize_keyboard=True))
            return START
        elif message == "➕ Tambah Baru":
            santri = get_belum_tambah()
            body = "Daftar santri belum tambah (%s)" %count(santri)
            body += "\n\n"
            body += "\n".join(s.nama for s in santri)
            body += "\n"

            update.message.reply_text(body,
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    one_time_keyboard=True,
                    resize_keyboard=True))

            return START

        elif message == "Murojaah sudah, harus ulang":
            santri = get_sudah_murojaah_harus_ulang()
            body = "Daftar santri sudah murojaah belum lancar (%s)" %count(santri)
            body += "\n\n"
            body += "\n".join(s.name for s in santri)
            body += "\n"

            update.message.reply_text(body,
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    one_time_keyboard=True,
                    resize_keyboard=True))

            return START
        elif message == "Tambah sudah, harus ulang":
            santri = get_sudah_tambah_harus_ulang()
            body = "Daftar santri sudah tambah belum lancar (%s)" %count(santri)
            body += "\n\n"
            body += "\n".join(s.nama for s in santri)
            body += "\n"

            update.message.reply_text(body,
                reply_markup=ReplyKeyboardMarkup(reply_start,
                    one_time_keyboard=True,
                    resize_keyboard=True))

            return START
        else:
            update.message.reply_text("Maaf, kami tidak tahu apa yang kamu mau...!!")
            return START
    else:
        update.message.reply_text("⛔⛔⛔ Maaf, anda tidak terdaftar ⛔⛔⛔")


def cancel(bot, update):
    update.message.reply_text("Operasi dihentikan",
        reply_markup=ReplyKeyboardMarkup(reply_start,
            one_time_keyboard=True,
            resize_keyboard=True))
    return START       

def error(bot, update, error):
    print(error) 

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TG_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={START_PROCESS:[MessageHandler([Filters.text], process_start)], 
                TAMBAH: [MessageHandler([Filters.text], process_tambah)],
                TAMBAH_NAMA_SANTRI: [MessageHandler([Filters.text], process_tambah_nama_santri)],
                PERSETUJUAN_SAVE_SANTRI: [MessageHandler([Filters.text],
                    process_persetujuan_save_santri)],
                CARI_NAMA_SANTRI: [MessageHandler([Filters.text], process_cari_nama_santri)],
                PROCESS_START: [MessageHandler([Filters.text], process_start_setor)],
                PROCESS_END: [MessageHandler([Filters.text], process_end_setor)],
                PROCESS_JENIS: [MessageHandler([Filters.text], process_jenis_setor)],
                PROCESS_LULUS: [MessageHandler([Filters.text], process_lulus_setor)],
                PROCESS_PERSETUJUAN_SETORAN: [MessageHandler([Filters.text], process_persetujuan_setor)],
                START: [MessageHandler([Filters.text], process_start)],
                LIHAT: [MessageHandler([Filters.text], process_lihat)],
                BELUM: [MessageHandler([Filters.text], process_belum)],


        },
        fallbacks=[CommandHandler('cancel', cancel)]

        
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)
    

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
