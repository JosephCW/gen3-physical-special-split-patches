#!/usr/bin/env python3
"""Connect to mGBA's GDB stub, stop at TestAiDone() and print gTestAiScore
(one line per scenario, four summed move scores each).

  python3 ai_read.py <TestAiDone address hex> <gTestAiScore address hex>
"""
import socket, sys, time

SCENARIOS, MOVES = 6, 4   # matches sAiTestScenarios in test_ai.inc
bp, addr = int(sys.argv[1], 16), int(sys.argv[2], 16)

for _ in range(60):                       # wait for mGBA to open its GDB port
    try:
        s = socket.create_connection(('127.0.0.1', 2345))
        break
    except OSError:
        time.sleep(0.5)
s.settimeout(120)
buf = b''

def recv_packet():
    """Read one $...#xx packet and acknowledge it."""
    global buf
    while True:
        i = buf.find(b'$')
        if i >= 0:
            j = buf.find(b'#', i)
            if j >= 0 and len(buf) >= j + 3:
                pkt, buf = buf[i + 1:j], buf[j + 3:]
                s.sendall(b'+')
                return pkt.decode()
        data = s.recv(65536)
        if not data:
            raise EOFError
        buf += data

def cmd(c):
    p = c.encode()
    s.sendall(b'$' + p + b'#' + b'%02x' % (sum(p) & 255))
    return recv_packet()

cmd('?')
cmd('Z0,%x,2' % bp)                       # breakpoint on TestAiDone (Thumb code)
cmd('c')                                  # run until it is hit
data = bytes.fromhex(cmd('m%x,%x' % (addr, SCENARIOS * MOVES * 4)))
for sc in range(SCENARIOS):
    row = data[sc * MOVES * 4:(sc + 1) * MOVES * 4]
    print(*[int.from_bytes(row[i:i + 4], 'little', signed=True) for i in range(0, MOVES * 4, 4)])
