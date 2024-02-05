
import asyncio
from aiohttp import ClientSession, WSMsgType
import os
from filetool import get_file_size, get_path_file_info
import sys
import time
script_path = os.path.dirname(os.path.abspath(__file__))
file_root_path = 'D:\\mywebfiles'


url = 'http://localhost:8080/9000'

# url = 'http://localhost:8080/download'
url = 'http://107.174.67.157:20000/9000'

async def send_file_chunk(ws, chunk):
    await ws.send_bytes(chunk)
    

async def send_file(filename, ws):
    CHUNK_SIZE = 1024  # 每块的大小

    with open(filename, 'rb') as file:
        a = 0
        size = get_file_size(filename)
        while True:            
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break
            await send_file_chunk(ws, chunk)
            a+=1024
            # print(a/1024/1024,'/',size/1024/1024)
            sys.stdout.write(f"\r{'%.2f / %.2f MB'%(a/1024/1024,size/1024/1024)}")
            sys.stdout.flush()
            # time.sleep(0.001)
    print('---send_file---')
    print(filename + '文件发送完成')

async def send_file_ws(file_name,ws):
    abs_file_name = os.path.join(file_root_path,file_name)
    headers = {
        'File': file_name,
        }   
    await ws.send_json(headers)
    await send_file(abs_file_name,ws)
    await ws.send_str("OK")

async def receive_from_server(ws,msg):
    try:
        
        print(msg['Type'])
        if(msg['Type'] == 'folder'):
            folder_path = os.path.join(file_root_path,msg['Path'])
            print('进入路径：'+ folder_path)
            folder_info_list = get_path_file_info(folder_path)
            await ws.send_json(folder_info_list)
            print('发送路径内容完成：'+folder_path)
            print(folder_info_list)
        elif(msg['Type'] == 'file'):
            
            abs_file_name = os.path.join(file_root_path,msg['Path'])
            headers = {
                'File': msg['Path'],
                }   
            await ws.send_json(headers)
            await send_file(abs_file_name,ws)
            await ws.send_str("OK")

        print(msg)
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
                            asyncio.create_task(receive_from_server(ws,msg))                        
                            # await receive_from_server(ws,msg)         
                        except asyncio.CancelledError:
                            break
        except Exception as e:
            print(f"连接出错: {e}")
        
        sleep_time = 2
        print('等待 ',sleep_time,' 秒后尝试重新连接...')
        await asyncio.sleep(2)

async def main():
    client_task = asyncio.create_task(client())
    await asyncio.gather(client_task)

asyncio.run(main())
