# esi-r2d7

Async Python client for ESI R2D7 RS-232 blind and shade controllers (now Hunter Douglas; also used with Draper shades). Built on [serialx](https://pypi.org/project/serialx/), so it works with local serial ports and with any URL that serialx can open, such as `socket://` or the Home Assistant Connect AUX-2 ESPHome serial proxy.

This library holds the protocol code for the Home Assistant ESI R2D7 integration. It has no Home Assistant dependency.

## Install

```bash
pip install esi-r2d7
```

## Use

```python
import asyncio
from esi_r2d7 import R2D7Connection

async def main() -> None:
    r2d7 = R2D7Connection("/dev/ttyUSB0", system=1)
    await r2d7.connect()
    await r2d7.open_blind(4)    # sends *1o04;
    await r2d7.close_blind(5)   # sends *1c05;
    await r2d7.stop_system()    # sends *1s; - stops EVERY moving blind on system 1
    await r2d7.disconnect()

asyncio.run(main())
```

The serial settings are fixed at **9600 baud, 8 data bits, no parity, 1 stop bit**.

## Important: Stop is system-wide

The R2D7 has no per-blind stop. The [v4.1 protocol](https://www.seymourscreenexcellence.com/documents/r2d7_v4.1_protocol.pdf), footnote 15, says STOP is universal, and a channel suffix such as `*1s05;` is ignored. Real hardware confirms this. So the library offers only `stop_system()`, and `command(1, "s", 4)` raises `ValueError`.

## Behaviour

- `command(system, operation, channel)` builds one frame. System is 1–7, channel is 1–60, operation is `"o"`, `"c"` or `"s"`. Any other input raises `ValueError`; a malformed frame never reaches the wire.
- One connection, one lock: commands from many callers never interleave bytes.
- Stops sent within `STOP_COALESCE_SECONDS` (0.3 s) collapse into one frame, unless an Open or Close was sent in between, or the link dropped.
- If a write fails, Stop is sent again once after a reconnect. Open and Close are not resent, because a repeated Open or Close can act as a stop on some motor controls.
- A reader task watches the link. `add_listener()` callbacks run when the link comes up or is lost.
- Controller replies `U` (not understood), `O` (buffer overflow) and X-off are logged and counted (`rejected_commands`, `buffer_overflows`). They are not acted on yet.
- `take_recently_moved(window)` returns the channels sent Open or Close in the last `window` seconds, so a caller can mark them as stopped after a Stop.
- `CONNECT_ERRORS` lists every exception a caller should catch for connection problems.

## Limitations

- No command pacing yet. The controller has a 256-byte buffer and discards everything on overflow, so avoid sending more than about 20 commands at once.
- The controller reports no position.

## Tests

```bash
pip install -e ".[test]"
pytest
```

The tests use a fake R2D7 on a loopback socket and real serialx. No hardware is needed.

## Releasing

Publishing uses PyPI trusted publishing, so no PyPI token is stored in GitHub.

1. One time: on pypi.org, add a pending trusted publisher for project `esi-r2d7`, owner `davidfi01`, repository `esi-r2d7`, workflow `publish.yml`, environment `pypi`.
2. Set `version` in `pyproject.toml`, commit and push.
3. Publish a GitHub release named `vX.Y.Z`. The `Publish to PyPI` workflow builds and uploads it.

## License

Apache License 2.0. See `LICENSE`.
