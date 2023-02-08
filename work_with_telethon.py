from telethon.sync import TelegramClient
from telethon import functions, events, types
import random
import datetime
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.tl.types import InputPeerEmpty, InputPeerUser
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.custom import Dialog


session = 'telethon_tester_2.session'
app_id = 'app_id'
app_hash = 'app_hash'
# pin random message
def pin_random_message():
    messages_ids = []
    with TelegramClient(session, app_id, app_hash) as client:
        for message in client.iter_messages('yakiiimets'):
            messages_ids.append(message.id)
        result = client(functions.messages.UpdatePinnedMessageRequest(
            peer='yakiiimets',
            unpin=False,
            pm_oneside=True,
            id=int(messages_ids[random.randrange(1, len(messages_ids), 1)])
        ))
        print(result.stringify())


# send to favorite
def send_me_random_message():
    messages_ids = []
    with TelegramClient(session, app_id, app_hash) as client:
        for message in client.iter_messages('escapisme_inc'):
            messages_ids.append(message.id)
            #message.forward_to('me')
            print(messages_ids)

        client.forward_messages(entity='me', messages=int(messages_ids[random.randrange(1, len(messages_ids), 1)]), from_peer='escapisme_inc')
        # write to favorite
        client.send_message(entity='me', message='some text')


# change username
def change_username(first_name, last_name):
    numbs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    prefix = '_'
    with TelegramClient(session, app_id, app_hash) as client:
        username = first_name + prefix + last_name
        while True:
            try:
                client(UpdateUsernameRequest(username))
                break
            except:
                numb = numbs[random.randrange(0, 9, 1)]
                username = first_name + prefix + last_name + prefix + numb

    return username


# print(change_username('escapisme', 'inc'))
# 2fa authentication
def two_fa(phone):
    with TelegramClient(session, app_id, app_hash) as client:
        y = client.send_code_request(phone)
        client.sign_in(phone=phone, password=input('password : '), code=input('code :'), phone_code_hash=y.phone_code_hash)


# add to contact
def add_to_contact():
    with TelegramClient(session, app_id, app_hash) as client:
        result = client(functions.messages.GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=100,
            hash=0,
            exclude_pinned=False,
        ))

        users = result.users
        for user in users:
            print(user.first_name)
            print(user.id)
            print(user.phone)

            first_name = user.first_name
            last_name = user.last_name
            if first_name is None:
                first_name = ''
            if last_name is None:
                last_name = ''

            try:
                client(functions.contacts.AddContactRequest(id=user.username,
                                                            first_name=first_name,
                                                            last_name=last_name,
                                                            phone='',
                                                            add_phone_privacy_exception=True))
            except:
                print('not a person')


# add_to_contact()

# create folder
def create_folder():
    with TelegramClient(session, app_id, app_hash) as client:
        result = client(functions.messages.GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=100,
            hash=0,
            exclude_pinned=False,
        ))

        users = result.users
        input_parameters = []
        for user in users:
            print(user.first_name)
            print(user.id)
            print(user.phone)
            print(user.access_hash)

            input_parameters.append(InputPeerUser(user_id=user.id, access_hash=user.access_hash))

        result = client(functions.messages.UpdateDialogFilterRequest(
            id=2,
            filter=types.DialogFilter(
                id=2,
                title='new folder',
                include_peers=input_parameters,
                pinned_peers=[InputPeerUser(user_id=289677306, access_hash=-8351389710579524214)],
                exclude_peers=[],
                contacts=True,
                non_contacts=True,
                bots=True,
                groups=True,
                broadcasts=True,
                exclude_muted=True,
                exclude_read=True,
            )
        ))
        print(result)


# pin dialog
def pin_dialog():
    with TelegramClient(session, app_id, app_hash) as client:
        result = client(functions.messages.ReorderPinnedDialogsRequest(
            folder_id=0,
            order=['yakiiimets', 'escapisme_inc'],
            force=True
        ))
        print(result)


# phone call
def calling():
    with TelegramClient(session, app_id, app_hash) as client:
        result = client(functions.phone.RequestCallRequest(
            user_id='escapisme_inc',
            g_a_hash=b'arbitrary\x7f data \xfa here',
            protocol=types.PhoneCallProtocol(
                min_layer=42,
                max_layer=42,
                library_versions=['1.26', '1.25.4', '124'],
                udp_p2p=True,
                udp_reflector=True
            ),
            video=True
        ))
        print(result.stringify())


def user_info():
    with TelegramClient(session, app_id, app_hash) as client:
        result = client(functions.help.GetUserInfoRequest(
            user_id='434801255'
        ))
        print(result.stringify())


def work_with_date():
    print(int(datetime.datetime.now().hour))

work_with_date()
