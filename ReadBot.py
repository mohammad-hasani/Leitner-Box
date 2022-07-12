import asyncio
from telethon import TelegramClient, events
from telethon.sync import TelegramClient

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 1523555
api_hash = '7ed4c8eaf95ba28f10644e901d201710'


# async def main():
#   client = TelegramClient('my_session', api_id, api_hash)
#   await client.start()
#
#   print((await client.get_me()).stringify())
#
#   from database import read_words_yield
#   for i in read_words_yield():
#       print(i)
#       await client.send_message('TranslateGerman_bot', i)
#   # await client.send_file('username', '/home/myself/Pictures/holidays.jpg')
#
#   # await client.download_profile_photo('me')
#   # messages = await client.get_messages('username')
#   # await messages[0].download_media()
#
#   # for message in client.iter_messages('TranslateGerman_bot'):
#   #         print(message.sender_id, ':', message.text)
#
#   # @client.on(events.NewMessage())
#   # async def handler(event):
#   #    # await event.respond('Hey!')
#   #    await event.respond(event.text)
#
#
# asyncio.run(main())


from telethon.sync import TelegramClient


with TelegramClient('my_session', api_id, api_hash) as client:
    for message in client.iter_messages('TranslateGerman_bot'):
        print(message.sender_id, ':', message.text)


