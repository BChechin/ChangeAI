import aiohttp
import asyncio
import urllib.parse

async def translate(text: str, from_lang: str = "ru", to_lang: str = "en") -> str:
    url = "https://translo.p.rapidapi.com/api/v3/translate"

    payload = urllib.parse.urlencode({
        "from": from_lang,
        "to": to_lang,
        "text": text
    })

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "53ebf2b39emsh0abcc68b74ed5c8p1b4c58jsnea22f8f3b8c8",
        "X-RapidAPI-Host": "translo.p.rapidapi.com"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as response:
            result: dict = await response.json()
            return result.get("translated_text", text)