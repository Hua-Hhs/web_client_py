
import asyncio
from aiohttp import ClientSession, WSMsgType
import os
from filetool import get_file_size, get_path_file_info
import sys
import time
import io
import json
import base64
# from animeinfos import animeinfolist
from animeinfos import anime_root_path, animeinfolist, get_cover_path_by_anime_title, get_episode_by_title_episode_title


script_path = os.path.dirname(os.path.abspath(__file__))
file_root_path = 'F:\\'


url = 'http://localhost:8000/ws/chat/'

async def client():
    print(file_root_path)
    while True:
        try:
            async with ClientSession() as session:
                async with session.ws_connect(url) as ws:
                    print('建立连接')
                    while True:
                        try:
                            if ws.closed:
                                break
                            await ws.send_json({
                                "Type":"header",
                                "type": "register"
                            
                            })
                            msg = await ws.receive_json()
                            # msg = await ws.receive()
                            print(msg)
                            await asyncio.sleep(2)
                        except asyncio.CancelledError:
                            break
        except Exception as e:
            print(f"连接出错: {e}")

        sleep_time = 2
        print('等待 ', sleep_time, ' 秒后尝试重新连接...')
        await asyncio.sleep(2)


async def main():
    client_task = asyncio.create_task(client())
    await asyncio.gather(client_task)

asyncio.run(main())


