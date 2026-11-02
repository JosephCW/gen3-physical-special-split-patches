#!/usr/bin/env python3
"""Connect to mGBA's GDB stub, stop at each TestDumpPoint() call and dump
IO regs + palette + VRAM + OAM to <outdir>/dump_<id>.bin.

  python3 gdb_dump.py <TestDumpPoint address hex> <outdir> <count> [<sGpuRegBuffer address hex>]

How it fits together:
  * The test build (harness.diff) calls TestDumpPoint(id) once each screen is
    ready to check.
  * mGBA started with `-g` waits for a debugger on TCP port 2345, speaking the
    GDB Remote Serial Protocol.
  * This script is a tiny GDB client. It sets a breakpoint on TestDumpPoint, lets
    the game run, and at each stop copies the display memory out.
    render_gba.py then turns each dump into a PNG.
  * Some display registers (the background scroll offsets) are write-only on
    real hardware and read back as junk. If the address of the game's
    sGpuRegBuffer (its copy of every display register it writes) is given, the
    registers are read from there instead. Without it (Ruby/Sapphire has no such
    buffer) the scroll offsets are recorded as 0, which is right for static menus.
"""
import socket, sys, time, os

bp, outdir, count = int(sys.argv[1], 16), sys.argv[2], int(sys.argv[3])
regs_addr = int(sys.argv[4], 16) if len(sys.argv) > 4 else 0x04000000
os.makedirs(outdir, exist_ok=True)

# mGBA takes a moment to start listening, so retry the connection for up to 30 s
for _ in range(60):
    try:
        s = socket.create_connection(('127.0.0.1', 2345))
        break
    except OSError:
        time.sleep(0.5)
s.settimeout(300)  # emulation is slow under the debugger; allow time to reach each screen
buf = b''          # bytes received but not yet parsed


def recv_packet():
    """Read one GDB reply packet: `$<payload>#<2-digit checksum>`. Returns the payload."""
    global buf
    while True:
        i = buf.find(b'$')
        if i >= 0:
            j = buf.find(b'#', i)
            if j >= 0 and len(buf) >= j + 3:
                pkt = buf[i + 1:j]
                buf = buf[j + 3:]
                s.sendall(b'+')  # acknowledge
                return pkt.decode()
        d = s.recv(65536)
        if not d:
            raise EOFError
        buf += d


def cmd(c, reply=True):
    """Send one GDB command packet (payload + checksum = sum of bytes mod 256) and wait for the reply."""
    p = c.encode()
    s.sendall(b'$' + p + b'#' + b'%02x' % (sum(p) & 255))
    return recv_packet() if reply else None


def mem(addr, n):
    """Read n bytes of GBA memory with `m<addr>,<len>` (reply is hex), 256 bytes per request."""
    out = b''
    while n:
        k = min(n, 0x100)  # mGBA's stub rejects much larger reads
        out += bytes.fromhex(cmd('m%x,%x' % (addr, k)))
        addr += k
        n -= k
    return out


cmd('?')                   # ask why the target is stopped (also completes the handshake)
cmd('Z0,%x,2' % bp)        # breakpoint at TestDumpPoint; kind 2 = 16-bit Thumb instruction
for _ in range(count):
    cmd('c')               # continue; returns when the breakpoint is hit
    regs = cmd('g')        # all registers as hex, r0 first (8 hex digits, little-endian, each)
    dump_id = int.from_bytes(bytes.fromhex(regs[:8]), 'little')  # r0 = the id argument
    print('dump point', dump_id, flush=True)
    io = mem(regs_addr, 0x60)
    if regs_addr == 0x04000000:
        io = io[:0x10] + bytes(0x10) + io[0x20:]  # BGxHOFS/VOFS can't be read back; assume 0
    with open('%s/dump_%d.bin' % (outdir, dump_id), 'wb') as f:
        # Same layout render_gba.py expects: IO regs, palette RAM, VRAM, OAM
        f.write(io + mem(0x05000000, 0x400) + mem(0x06000000, 0x18000) + mem(0x07000000, 0x400))
cmd('D', reply=False)      # detach; the script then closes mGBA
