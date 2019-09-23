from telethon.tl.functions import messages
from telethon.tl.types import InputPeerChat, ChatBannedRights
from telethon.sync import TelegramClient

from common import db, tg

DEFAULT_RIGHTS = ChatBannedRights(
            until_date=None,
            view_messages=False,
            send_messages=False,
            send_media=False,
            send_stickers=False,
            send_gifs=False,
            send_games=False,
            send_inline=True,
            send_polls=True,
            change_info=True,
            invite_users=True,
            pin_messages=True)


def populate(quantity: int) -> None:
    client = TelegramClient(api_id=tg.API_ID, api_hash=tg.API_HASH, session="tmp")
    client.connect()
    for i in range(quantity):
        chat_id = client(messages.CreateChatRequest([tg.DEAL_BOT_UID, "me"], tg.BOARD_NAME)).chats[0].id
        chat = db.Chat(invite=client(messages.ExportChatInviteRequest(InputPeerChat(chat_id))).link, occupied=False, id=chat_id * -1)
        chat.save()

        client(messages.EditChatDefaultBannedRightsRequest(InputPeerChat(chat_id), DEFAULT_RIGHTS))
        client(messages.EditChatAdminRequest(chat_id, tg.DEAL_BOT_UID, True))
        client(messages.DeleteChatUserRequest(chat_id, "me"))


if __name__ == "__main__":
    populate(1)
