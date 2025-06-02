import asyncio
import socket
import sys

async def async_input(prompt=""):
    print(prompt, end="", flush=True)
    return await asyncio.get_event_loop().run_in_executor(None, lambda: sys.stdin.readline().strip())

async def input_name():
    print("> Input your name.")
    name = await async_input(">>> ")
    print(f"Hello, {name}.")
    return name

async def input_message(message_queue):
    while True:
        try:
            print("> Please enter your message.")
            message = await async_input(">>> ")
            await message_queue.put(message)  # キューにメッセージを追加
        except Exception as e:
            print(f"Error reading input: {e}")

async def send_message(sock, server_address, user_name, message_queue):
    while True:
        message = await message_queue.get()  # キューからメッセージを取得 
        if not message.strip():
            print("quit.")
            break
        client_message = f"{user_name}: {message}"
        sock.sendto(client_message.encode("utf-8"), server_address)

async def receive_message(sock):
    while True:
        try:
            # サーバーからのブロードキャストメッセージを受信
            data, _ = await asyncio.get_event_loop().run_in_executor(None, sock.recvfrom, 4096)
            print(f"\nBroadcast message!: {data.decode()}")
        except Exception as e:
            print(f"\nBroadcast message!:  {e}")
            break

async def main():
    ip = "127.0.0.1"
    port = 8000
    server_address = (ip, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message_queue = asyncio.Queue()  # メッセージ用の非同期キューを作成
    user_name = await input_name()

    await asyncio.gather(
        input_message(message_queue), 
        send_message(sock, server_address, user_name, message_queue),
        receive_message(sock),
    )
    sock.close()
    print("Connection closed")

# イベントループの開始
asyncio.run(main())
