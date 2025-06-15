import socket
import asyncio

clients = set()

async def handle_client(sock):
    while True:
        data, client_address = await asyncio.get_event_loop().run_in_executor(None, sock.recvfrom, 4096)
        message = data.decode()
        print(f"Received message from {client_address}: {message}")

        clients.add(client_address)
        
        for client in clients:
            if client != client_address:
                print(f"Broadcasting to {client}")
                sock.sendto(data, client)

async def main():
    ip = "127.0.0.1"
    port = 8000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    try:
        await handle_client(sock)
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        sock.close()

asyncio.run(main())
