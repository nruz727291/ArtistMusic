import asyncio
from pyrogram import filters, types

from Elevenyts import app


@app.on_message(filters.group & filters.command("tagall"))
async def tag_all_members(_, message: types.Message):
    """
    Mention all real users in the group using /tagall
    """

    if message.chat.type not in ["supergroup", "group"]:
        return await message.reply_text(
            "❌ This command only works in groups."
        )

    # Optional message after /tagall
    extra_msg = " ".join(message.command[1:])

    if extra_msg:
        text = f"<blockquote><b>{extra_msg}</b></blockquote>\n\n"
    else:
        text = "<blockquote><b>📢 Tagging all members</b></blockquote>\n\n"

    mentions = []
    count = 0

    try:
        async for member in app.get_chat_members(message.chat.id):

            user = member.user

            # Skip bots + deleted users
            if user.is_bot or user.is_deleted:
                continue

            # Mention format
            mentions.append(
                f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
            )

            count += 1

            # Telegram message limit safe
            if len(mentions) == 5:
                await message.reply_text(
                    text + " | ".join(mentions),
                    disable_web_page_preview=True
                )

                mentions = []

                # Anti flood wait
                await asyncio.sleep(2)

        # Send remaining mentions
        if mentions:
            await message.reply_text(
                text + " | ".join(mentions),
                disable_web_page_preview=True
            )

    except Exception as e:
        await message.reply_text(
            f"❌ Error: <code>{e}</code>"
        )
