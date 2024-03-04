
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


url = 'http://localhost:20000/9000'

# url = 'http://localhost:8080/download'
# url = 'http://107.174.67.157:22225/9000'
# url = 'http://107.174.67.157:20001/9000'
url = 'http://localhost:8000/ws/chat/'



async def send_file_chunk(ws, msg):

    await ws.send_json(msg)


def convert_size(size_bytes):
    GB = size_bytes / (1024 ** 3)
    MB = (size_bytes % (1024 ** 3)) / (1024 ** 2)
    KB = (size_bytes % (1024 ** 2)) / 1024
    return f"{int(GB)}GB {int(MB)}MB {int(KB)}KB"

async def send_file(filename, ws, UUID):
    print('send_file---start')

    CHUNK_SIZE = 1024*1024  # 每块的大小

    with open(filename, 'rb') as file:
        current_size = 0
        size = get_file_size(filename)
      
        while True:
            chunk = file.read(CHUNK_SIZE)

            if not chunk:
                break

            current_size += 1024
            data = {}

            chunk = base64.b64encode(chunk)
            # 字符串化，使用utf-8的方式解析二进制
            chunk = str(chunk, 'utf-8')

            # chunk = str(chunk)
            if current_size >= size:
                data = {'Chunk': chunk, 'Is_the_last': True}
            else:
                data = {'Chunk': chunk, 'Is_the_last': False}

            msg = {'Type': 'file', 'UUID': UUID, 'Data': data}
            await send_file_chunk(ws, msg)
            await asyncio.sleep(0.005)
            sys.stdout.write(
                f"\r{'%.2f / %.2f MB'%(current_size/1024/1024,size/1024/1024)}")
            sys.stdout.flush()

    print('---send_file---')
    print(filename + '文件发送完成')


async def send_all_anime_title(ws):
    msg = {'Type': 'title', 'titles': animeinfolist().get_anime_titles()}
    print('send_all_anime_title_over')
    await ws.send_json(msg)


def parse_range_header(range_header, file_size):

    start_range, end_range = range_header.split('=')[1].split('-')
    start_range = int(start_range)
    end_range = int(end_range) if end_range else min(start_range + 1024*1024,file_size - 1)
    content_length = end_range - start_range + 1

    return start_range, end_range, content_length

async def receive_from_server(ws, msg):
    try:
        print('msg  ===  '+ str(msg))
        if (msg['Type'] == 'folder'):
            try:
                    
                folder_path = os.path.join(file_root_path, msg['Path'])
                print('进入路径：' + folder_path)
                folder_info_list = get_path_file_info(folder_path)

                content = {'Type': 'folder', 'Infos': folder_info_list, 'Status':'1'}
                await ws.send_json(content)
                print('发送路径内容完成：'+folder_path)
                # print(folder_info_list)
            except:
                content = {'Type': 'folder', 'Infos': folder_info_list, 'Status':'0'}
                await ws.send_json(content)
        elif (msg['Type'] == 'episode_titles'):
            print('get_anime_episode_titles')
            anime_title = msg['Title']
            UUID = msg['UUID']
            episodes = animeinfolist.get_anime_episode_titles(anime_title)
            msg = {'Type': 'episode_titles','UUID': UUID, 'episode_title_list': episodes}
            print('episode_titles')
            # print(msg)
            await ws.send_json(msg)
        elif (msg['Type'] == 'file'):

            UUID = msg['UUID']
            if(msg['FileType'] == 'file'):
                abs_file_name = os.path.join(file_root_path, msg['Path'])
                await send_file(abs_file_name, ws, UUID)

            elif(msg['FileType'] == 'cover'):
                # 传来msg['Path']是anime的title，通过title获取cover的路径，然后用send_file传输回去
                abs_file_name = os.path.join(anime_root_path, msg['Title'])
                abs_file_name = os.path.join(abs_file_name, 'cover.jpg') 
                abs_file_path = get_cover_path_by_anime_title(msg['Title'])  

                await send_file(abs_file_path, ws, UUID)
                # await send_file(abs_file_name, ws, UUID)

            elif(msg['FileType'] == 'video'):
                # print('video')
                data = msg['Data']
                UUID = data['UUID']
                range = data['Range']
                title = data['Title']
                episode = data['Episode']
                print(f'准备发送range资源{range}')

                path = get_episode_by_title_episode_title(title,episode)
                file_size = os.path.getsize(path)
                if range:
                    start, end, content_length = parse_range_header(range, file_size)

                with open(path, 'rb') as file:
                    file.seek(start)
                    chunk = file.read(content_length)
 
                chunk = base64.b64encode(chunk)
                # 字符串化，使用utf-8的方式解析二进制
                chunk = str(chunk, 'utf-8')
                # print(convert_size(file_size))
                data = {'file_size': file_size,'start': start, 'end': end, 'content_length': content_length,'chunk': chunk}
                msg = {'Type': 'file', 'UUID': UUID, 'Data': data}
  
                # print(file_size)
                print(f'发送range资源{range}完毕')
                await send_file_chunk(ws, msg)

        elif (msg['Type'] == 'animeinfo'):
            await send_all_anime_title(ws)

        # print(msg)
    except asyncio.CancelledError:
        pass


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
                            msg = await ws.receive_json()
                            asyncio.create_task(receive_from_server(ws, msg))
                            # await receive_from_server(ws,msg)
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
