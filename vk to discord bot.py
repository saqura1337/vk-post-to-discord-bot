import vk_api
import discord
import asyncio

# Входим в ВК по токену
session_vk = vk_api.VkApi(token='token_VK')
vk = session_vk.get_api()

# Айди группы ВК
group_id = 'id'

# Входим в Discord
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
discord_token = 'ds_token'

# Айди канала в Discord
channel_id = 'ch_ID'

# Код бота
@client.event
async def on_ready():
    channel = client.get_channel(channel_id)
    if channel:
        print(f"Подключен к {channel.name} ({channel.id})")
    else:
        print(f"Ошибка: канал не найден или бот не имеет доступа к этому каналу")

    print(f"Залогинен как: {client.user.name} ({client.user.id})")
    print("-----------------------")

    last_post_id = None

    while True:
        try:
            # Получаем новые посты через VK API
            wall = vk.wall.get(owner_id='-' + group_id, count=1, offset=1)['items'][0]
            text = wall['text']
            attachments = wall.get('attachments', [])
            post_id = wall['id']

            if post_id != last_post_id and not wall.get('is_pinned', False):
                message = f"НОВЫЙ ПОСТ В ГРУППЕ ВК: \n\n{text}\n"

                for attachment in attachments:
                    if attachment['type'] == 'photo':
                        message += f"{attachment['photo']['sizes'][-1]['url']}\n"
                    elif attachment['type'] == 'link':
                        message += f"{attachment['link']['url']}\n"

                # теперь отсылаем месседж в дисик
                channel = client.get_channel(int(channel_id))
                if channel is not None:
                    await channel.send(message)
                else:
                    print("Ошибка: канал не найден или бот не имеет доступа к этому каналу")
                last_post_id = post_id

            await asyncio.sleep(180)

        except Exception as e:
            print(f"Error: {e}")

client.run(discord_token)
