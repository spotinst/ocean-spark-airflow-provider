#!/usr/bin/env python3

desc = """\
Inverse websockify is a TCP to WebSocket proxy/bridge.  It accepts a
plain TCP connection and connects to a WebSocket server, effectively
adding WS support to a client that does not natively support it.  It
is essentially the opposite of "websockify".

Note that this only handles simple byte streams of data, with no
support for conveying WebSockets message framing back to the client.

For example, Eclipse Mosquitto supports WebSockets on the server side,
but not on the client side (for bridging).  To connect one instance

  {prog} --port 15002

and configure the client with e.g.

  address 127.0.0.1:15002
"""

import sys

import asyncio
import websockets

from typing import Any, List


class Proxy:
    def __init__(self, url: str, token: str, port: int = 15002, addr: str = "0.0.0.0"):
        self.port = port
        self.addr = addr
        self.token = token
        self.url = url

    async def copy(self, reader: Any, writer: Any) -> None:
        while True:
            data = await reader()
            if data == b"":
                break
            future = writer(data)
            if future:
                await future

    async def handle_client(self, r: Any, w: Any) -> None:
        peer = w.get_extra_info("peername")
        print(f"{peer} connected")
        loop = asyncio.get_event_loop()
        try:
            async with websockets.connect(
                self.url,
                subprotocols=None,
                extra_headers={"Authorization": f"Bearer {self.token}"},
            ) as ws:
                print(f"{peer} connected to {self.url}")

                def r_reader() -> Any:
                    return r.read(65536)

                tcp_to_ws = loop.create_task(self.copy(r_reader, ws.send))
                ws_to_tcp = loop.create_task(self.copy(ws.recv, w.write))
                done, pending = await asyncio.wait(
                    [tcp_to_ws, ws_to_tcp], return_when=asyncio.FIRST_COMPLETED
                )
                for x in done:
                    try:
                        await x
                    except:
                        pass
                for x in pending:
                    x.cancel()
        except Exception as e:
            print(f"{peer} exception:", e)
        w.close()
        print(f"{peer} closed")

    async def start(self) -> None:
        await asyncio.start_server(self.handle_client, self.addr, self.port)
        print(f"Listening on {self.addr} port {self.port}")


def main(argv: List[str]) -> None:
    import argparse
    import textwrap

    parser = argparse.ArgumentParser(
        prog=argv[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.indent(desc.format(prog=argv[0]), prefix="    "),
    )

    parser.add_argument(
        "--port", "-p", metavar="PORT", default=15002, help="TCP listen port"
    )
    parser.add_argument(
        "--listen", "-l", metavar="ADDR", default="0.0.0.0", help="TCP listen address"
    )
    parser.add_argument(
        "--token", metavar="TOKEN", default=None, help="WebSocket token"
    )
    parser.add_argument(
        "url", metavar="URL", help="WebSocket URL (ws://.. or wss://..)"
    )

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    proxy = Proxy(args.url, args.token, args.port, args.listen)
    loop.run_until_complete(proxy.start())
    loop.run_forever()


if __name__ == "__main__":
    main(sys.argv)
