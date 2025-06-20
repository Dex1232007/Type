import httpx
import re
from typing import Dict, List, Optional, Union

async def get_yt_info(youtube_url: str) -> Dict[str, Union[bool, str]]:
    try:
        api_url = f"https://zawmyo123.serv00.net/youtube/yt_v2.php?action=generate&url={youtube_url}"
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, timeout=30)
            response.raise_for_status()
            data = response.json()

        if not data.get('success'):
            return {'ok': False, 'error': 'Invalid API response'}

        video_id_match = re.search(r'(?:v=|\/)([\w-]{11})', youtube_url)
        video_id = video_id_match.group(1) if video_id_match else ''

        return {
            'ok': True,
            'title': data.get('title', 'Unknown Title'),
            'author': data.get('author', 'Unknown Author'),
            'duration': data.get('duration', 'Unknown'),
            'thumbnail': f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        }
    except Exception as e:
        return {'ok': False, 'error': str(e)}

async def get_audio_info(youtube_url: str) -> Dict[str, Union[bool, str]]:
    try:
        api_url = f"https://mp3.manzoor76b.workers.dev/?url={youtube_url}"
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, timeout=30)
            response.raise_for_status()
            data = response.json()

        if not data.get('status'):
            return {'ok': False, 'error': 'Invalid download API response'}

        return {'ok': True, 'download_url': data.get('output', '')}
    except Exception as e:
        return {'ok': False, 'error': str(e)}

async def search_youtube(query: str) -> List[Dict[str, str]]:
    try:
        api_url = f"https://zawmyo123.serv00.net/api/ytsearch.php?query={query}"
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, timeout=30)
            response.raise_for_status()
            results = response.json()
        return results if isinstance(results, list) else []
    except Exception:
        return []

def validate_youtube_url(url: str) -> bool:
    return bool(re.match(r'^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]{11}', url))

def extract_youtube_url_only(text: str) -> Optional[str]:
    match = re.search(r'(https?:\/\/[^\s]+)', text)
    if match:
        url = match.group(1).strip()
        if validate_youtube_url(url):
            return url
    return None
