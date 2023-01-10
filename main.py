from telethon import TelegramClient, events, sync
from telethon.tl.functions.account import UpdateProfileRequest, GetAuthorizationsRequest
from telethon import functions, types
from telethon.tl.types import UserStatusOnline
import itertools

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 000000
api_hash = 'hash'

client = TelegramClient('telethon.session', api_id, api_hash).start()
client.connect()
print(client.is_user_authorized())

bot = ''


def change_photo(file_path):
    client(functions.photos.UploadProfilePhotoRequest(file=client.upload_file(file_path)))


def change_about(text):
    client(UpdateProfileRequest(about=text))


def change_firstname(first_name):
    client(UpdateProfileRequest(first_name=first_name))


def change_lastname(last_name):
    client(UpdateProfileRequest(last_name=last_name))


def check_spam_block():
    if not client.is_user_authorized():
        return 'account is baned'
    return 'account isn`t banned'


def date_created():
    result = client(GetAuthorizationsRequest())
    auths_list = result.__getattribute__('authorizations')

    date = auths_list[0].date_created

    for auths in auths_list:
        if date > auths.date_created:
            date = auths.date_created

    return date


def check_online():
    result = client(GetAuthorizationsRequest())
    auths_list = result.__getattribute__('authorizations')
    #d = dict(itertools.zip_longest(*[iter(auths_list)] * 2, fillvalue=""))
    #print(d)
    text = ''.join(str(e) for e in auths_list)
    print(text)


def check_balance(message):

    balance_dict = {'BTC': '0', 'TON': '0'}
    try:
        client.send_message('https://t.me/wallet', '/wallet')

        i = 0
        for message in client.iter_messages('https://t.me/wallet'):
            text = message.text.split()

            for t in text:
                if t == 'BTC' or t == 'TON':
                    print(t + ' ' + text[4])
                    balance_dict[t] = text[4]
            if i == 1:
                break

            i += 1
    except:
        pass

    return balance_dict



#print(client)
#client.download_profile_photo('me')


print(date_created())
check_online()
print(check_balance('/start'))

date_created()

