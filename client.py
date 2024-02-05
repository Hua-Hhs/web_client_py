
import asyncio
from aiohttp import ClientSession, WSMsgType
import os
from filetool import get_file_size, get_path_file_info
import sys
import time
import io
import json
import base64
from animeinfos import animeinfolist
from animeinfos import anime_root_path


script_path = os.path.dirname(os.path.abspath(__file__))
file_root_path = 'F:\\'


url = 'http://localhost:20000/9000'

# url = 'http://localhost:8080/download'
url = 'http://107.174.67.157:20001/9000'
# url = 'http://107.174.67.157:20001/9000'


async def send_file_chunk(ws, msg):

    await ws.send_json(msg)


async def send_file(filename, ws, UUID):

    CHUNK_SIZE = 1024  # 每块的大小

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
    msg = {'Type': 'title', 'titles': animeinfolist().get_all_anime_title()}
    print('over')
    await ws.send_json(msg)


async def send_all_anime_cover():
    pass

def parse_range_header(range_header, file_size):
    # print(range_header)
    _, range_values = range_header.split('=')
    start_str, end_str = range_values.split('-')

    # 处理空字符串的情况，使用默认值
    start = int(start_str) if start_str else 0
    end = int(end_str) if end_str else min( start + 1024*256 - 1, file_size)

    return start, end

async def receive_from_server(ws, msg):
    try:
        print(msg['Type'])
        if (msg['Type'] == 'folder'):
            try:
                    
                folder_path = os.path.join(file_root_path, msg['Path'])
                print('进入路径：' + folder_path)
                folder_info_list = get_path_file_info(folder_path)

                content = {'Type': 'folder', 'Infos': folder_info_list, 'Status':'1'}
                await ws.send_json(content)
                print('发送路径内容完成：'+folder_path)
                print(folder_info_list)
            except:
                content = {'Type': 'folder', 'Infos': folder_info_list, 'Status':'0'}
                await ws.send_json(content)
        elif (msg['Type'] == 'file'):

            UUID = msg['UUID']
            if(msg['FileType'] == 'file'):
                abs_file_name = os.path.join(file_root_path, msg['Path'])
                await send_file(abs_file_name, ws, UUID)

            elif(msg['FileType'] == 'cover'):
                abs_file_name = os.path.join(anime_root_path, msg['Path'])
                abs_file_name = os.path.join(abs_file_name, 'cover.jpg')                
                await send_file(abs_file_name, ws, UUID)

            elif(msg['FileType'] == 'video'):
                # print('video')
                data = msg['Data']
                UUID = data['UUID']
                range = data['Range']
                title = data['Title']
                chapter = data['Chapter']
                # print(msg['Data'])
                # path = 'E:\\web\\anime\\111.mp4'  # Set the correct path to your video file
                path = 'E:\\web\\myweb\\files\\bule bird\\2222.mp4' 
                path = anime_root_path + title + '\\' + chapter 
                print(path)
                file_size = os.path.getsize(path)
                
                if range:
                    start, end = parse_range_header(range, file_size)
                    request_size = end - start + 1

                with open(path, 'rb') as file:
                    print('open')
                    file.seek(start)
                    chunk = file.read(request_size)
                        # await response.write(data)
                        # request_size -= chunk_size
                # print(request_size)
                chunk = base64.b64encode(chunk)
                # 字符串化，使用utf-8的方式解析二进制
                chunk = str(chunk, 'utf-8')
                data = {'file_size': file_size,'start': start, 'end': end, 'request_size': request_size,'chunk': chunk}
                # data = {'file_size': file_size,'start': start, 'end': end, 'request_size': request_size}
                msg = {'Type': 'file', 'UUID': UUID, 'Data': data}
                # print(msg)
                # print(1)
                print(file_size)
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
