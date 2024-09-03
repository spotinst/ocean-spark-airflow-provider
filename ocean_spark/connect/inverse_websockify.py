#!/usr/bin/env python3

""" Originally from
Copyright (C) 2021 Jim Paris <jim@jim.sh>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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

import os
import asyncio
import logging
import websockets

from typing import Any, List


class Proxy:
    def __init__(
        self,
        url: str,
        token: str,
        port: int = 15002,
        addr: str = "0.0.0.0",
        ping_interval: float = -1.0,
    ):
        logging.info("Initializing proxy")
        if port == -1 and not addr.startswith("/"):
            logging.info(
                "Port is -1 and address is not a unix socket, creating a unix socket"
            )
            pid = str(os.getpid())
            rnd = os.urandom(4).hex()
            self.addr = f"/tmp/ocean-spark-{pid}-{rnd}.sock"
        else:
            self.addr = addr

        self.ping_interval = ping_interval
        self.port = port
        self.token = token
        self.url = url
        self.done = False
        self.loop = asyncio.new_event_loop()

    def inverse_websockify(self) -> None:
        self.loop.run_until_complete(self.start())
        self.loop.run_forever()

    async def copy(self, reader: Any, writer: Any) -> None:
        while not self.done:
            data = await reader()
            if data == b"":
                break
            future = writer(data)
            if future:
                await future

    async def ping(self, ws: Any) -> None:
        while not self.done:
            await asyncio.sleep(self.ping_interval)
            await ws.ping()

    async def handle_client(self, r: Any, w: Any) -> None:
        peer = w.get_extra_info("peername")
        try:
            async with websockets.connect(
                self.url,
                subprotocols=None,
                extra_headers={"Authorization": f"Bearer {self.token}"},
            ) as ws:
                logging.debug(
                    f"{peer} connected to {self.url} on {self.addr}:{self.port}"
                )

                def r_reader() -> Any:
                    return r.read(65536)

                tcp_to_ws = self.loop.create_task(self.copy(r_reader, ws.send))
                ws_to_tcp = self.loop.create_task(self.copy(ws.recv, w.write))

                task_list = [tcp_to_ws, ws_to_tcp]
                if self.ping_interval > 0:
                    ping_task = self.loop.create_task(self.ping(ws))
                    task_list.append(ping_task)

                done, pending = await asyncio.wait(
                    task_list, return_when=asyncio.FIRST_COMPLETED
                )
                for x in done:
                    try:
                        await x
                    except:
                        pass
                for x in pending:
                    x.cancel()
        except Exception as e:
            logging.error(f"{peer} exception:", e)
        w.close()
        logging.debug(f"{peer} closed")

    async def start(self) -> None:
        if self.addr.startswith("/"):
            await asyncio.start_unix_server(self.handle_client, self.addr)
        else:
            await asyncio.start_server(self.handle_client, self.addr, self.port)
