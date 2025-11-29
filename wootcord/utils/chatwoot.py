import typing as t
import discord
import aiohttp
from wootcord.models import MessageCreatePayload
from wootcord.config import chatwoot_base_url, chatwoot_account_id, chatwoot_api_key

def convert_dc_message(
    message: discord.Message, 
    message_type: t.Literal["incoming", "outgoing"] = "outgoing",
    is_private: bool = False,
    add_signature: bool = True,
) -> MessageCreatePayload:
    content_parts = []

    if message.clean_content:
        content_parts.append(message.clean_content)

    if message.attachments:
        content_parts.append("\n**Attachments:**")
        for attachment in message.attachments:
            content_parts.append(f"[{attachment.filename}]({attachment.url})")

    if message.stickers:
        content_parts.append("\n**Stickers:**")
        for sticker in message.stickers:
            content_parts.append(f"[Sticker]({sticker.url})")

    if message.embeds:
        for embed in message.embeds:
            embed_text = []
            if embed.title:
                embed_text.append(f"**{embed.title}**")
            if embed.description:
                embed_text.append(embed.description)
            
            for field in embed.fields:
                embed_text.append(f"**{field.name}**: {field.value}")

            if embed_text:
                content_parts.append("\n> " + "\n> ".join(embed_text))
    
    if add_signature:
        role_name = getattr(message.author, "top_role", None)
        role_name = role_name.name if role_name else None

        if role_name and role_name != "@everyone":
            role_str = f" | {role_name}"
        else:
            role_str = ""

        content_parts.append(f"\n**— {message.author.display_name}{role_str}**")

    final_content = "\n".join(content_parts)

    if not final_content:
        final_content = "*(Empty Message or Unsupported Content)*"

    return MessageCreatePayload(
        content=final_content,
        message_type=message_type,
        private=is_private,
        content_type="text",
        content_attributes={},
    )

async def send_to_chatwoot(
    conversation_id: int,
    payload: MessageCreatePayload
) -> t.Optional[t.Dict[str, t.Any]]:
    response = await _send_to_chatwoot(
        account_id=chatwoot_account_id,
        conversation_id=conversation_id,
        payload=payload,
        api_access_token=chatwoot_api_key,
        base_url=chatwoot_base_url,
    )
    return response

async def _send_to_chatwoot(
    account_id: int,
    conversation_id: int,
    payload: MessageCreatePayload,
    api_access_token: str,
    base_url: str,
    session: t.Optional[aiohttp.ClientSession] = None
) -> t.Optional[t.Dict[str, t.Any]]:
    endpoint = f"{base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"

    headers = {
        "api_access_token": api_access_token,
        "Content-Type": "application/json"
    }

    json_payload = payload.model_dump()

    async def _perform_request(client):
        try:
            async with client.post(endpoint, json=json_payload, headers=headers) as response:
                if response.status >= 400:
                    raise Exception(f"{response.status} {response.json()}")
                return await response.json()
        except Exception:
            raise

    if session:
        return await _perform_request(session)
    else:
        async with aiohttp.ClientSession() as new_session:
            return await _perform_request(new_session)