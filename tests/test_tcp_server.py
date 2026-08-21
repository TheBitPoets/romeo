import asyncio

from romeo.backends.mock import MockBackend
from romeo.network.server import TcpRobotServer
from romeo.safety import SafetyBackend


async def read_line(reader: asyncio.StreamReader) -> str:
    return (await reader.readline()).decode("utf-8").strip()


async def server_scenario() -> None:
    inner = MockBackend()
    safety = SafetyBackend(inner, background_watchdog=False)
    server = TcpRobotServer(safety, port=0)
    host, port = await server.start()

    reader, writer = await asyncio.open_connection(host, port)
    assert await read_line(reader) == "OK ROMEO/1 READY"

    writer.write(b"FORWARD 0.4\n")
    await writer.drain()
    assert await read_line(reader) == "OK FORWARD"
    assert (inner.left_speed, inner.right_speed) == (0.4, 0.4)

    busy_reader, busy_writer = await asyncio.open_connection(host, port)
    assert (await read_line(busy_reader)).startswith("ERR BUSY")
    busy_writer.close()
    await busy_writer.wait_closed()

    writer.write(b"LOOK 30 120\nSTOP\n")
    await writer.drain()
    assert await read_line(reader) == "OK LOOK"
    assert await read_line(reader) == "OK STOP"
    assert (inner.pan_angle, inner.tilt_angle) == (30.0, 120.0)
    assert (inner.left_speed, inner.right_speed) == (0.0, 0.0)

    writer.write(b"DANCE\n")
    await writer.drain()
    assert (await read_line(reader)).startswith("ERR unknown command")

    writer.write(b"FORWARD\n")
    await writer.drain()
    assert await read_line(reader) == "OK FORWARD"
    writer.close()
    await writer.wait_closed()
    for _ in range(20):
        if safety.active_controller is None:
            break
        await asyncio.sleep(0)
    assert safety.active_controller is None
    assert (inner.left_speed, inner.right_speed) == (0.0, 0.0)

    await server.close()
    safety.close()


def test_tcp_server_protocol_ownership_and_disconnect_stop() -> None:
    asyncio.run(server_scenario())
