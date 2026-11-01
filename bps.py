#!/usr/bin/env python3
"""Minimal BPS patch creator / applier (no dependencies).

  python3 bps.py create  original.gba modified.gba out.bps
  python3 bps.py apply   original.gba patch.bps   out.gba

BPS is the standard ROM-hacking patch format (used by Flips, Rom Patcher JS,
mGBA, ...). A BPS file describes how to build the modified ROM ("target") out of
the original ROM ("source") with four kinds of instructions:

  SourceRead   copy bytes from the source at the *same* position we're writing to
  TargetRead   bytes stored literally in the patch (new data)
  SourceCopy   copy bytes from somewhere else in the source (for data that moved)
  TargetCopy   copy bytes from earlier in the target (for repeated data)

It also stores CRC32 checksums of the source, the target and the patch itself.
That's how a patcher knows you gave it the wrong ROM (e.g. v1.1 instead of v1.0).

Recompiling the game shifts lots of code and data around, so most of the target
is "the same bytes as the source, a little further along". SourceCopy covers that
cheaply, which keeps the patch to a few hundred KB.
"""
import sys, zlib

# Instruction types (stored in the low 2 bits of each instruction number)
SOURCE_READ, TARGET_READ, SOURCE_COPY, TARGET_COPY = range(4)
MIN_MATCH = 16  # shortest run worth looking up in the index (and the index key length)
STEP = 8        # index every 8th source position (keeps memory use reasonable for a 16 MB ROM)


def enc_num(n):
    """Encode a non-negative integer as a BPS variable-length number.

    7 bits per byte, least significant first; the high bit marks the last byte.
    BPS also subtracts 1 after each continuation byte so every value has exactly
    one encoding.
    """
    out = bytearray()
    while True:
        x = n & 0x7f
        n >>= 7
        if n == 0:
            out.append(0x80 | x)
            return out
        out.append(x)
        n -= 1


def dec_num(data, pos):
    """Decode a BPS variable-length number at data[pos]. Returns (value, new_pos)."""
    n, shift = 0, 1
    while True:
        x = data[pos]; pos += 1
        n += (x & 0x7f) * shift
        if x & 0x80:
            return n, pos
        shift <<= 7
        n += shift


def enc_signed(n):
    """Encode a signed offset: magnitude shifted left one, with the sign in bit 0."""
    return enc_num((abs(n) << 1) | (1 if n < 0 else 0))


def create(src, tgt, metadata=b''):
    """Build a BPS patch that turns `src` into `tgt`."""
    # Index of the source: 16-byte chunk -> first position it appears at (every STEP bytes).
    # Used to find where a piece of the target came from in the source.
    index = {}
    for p in range(0, len(src) - MIN_MATCH, STEP):
        index.setdefault(src[p:p + MIN_MATCH], p)

    # Header: magic, source size, target size, metadata
    out = bytearray(b'BPS1')
    out += enc_num(len(src)) + enc_num(len(tgt)) + enc_num(len(metadata)) + metadata
    src_rel = 0          # SourceCopy offsets are relative to where the last one finished
    literal_start = None  # start of a run of bytes we couldn't match (written as TargetRead)
    t = 0                # current position in the target
    n = len(tgt)

    def flush_literal(end):
        """Write any pending unmatched bytes as one TargetRead instruction."""
        nonlocal literal_start
        if literal_start is not None:
            ln = end - literal_start
            out.extend(enc_num(((ln - 1) << 2) | TARGET_READ))
            out.extend(tgt[literal_start:end])
            literal_start = None

    def match_len(sp, tp):
        """How many bytes match between src[sp:] and tgt[tp:]."""
        ln = 0
        while tp + ln < n and sp + ln < len(src) and src[sp + ln] == tgt[tp + ln]:
            ln += 1
        return ln

    last_delta = 0  # source-minus-target offset of the last SourceCopy (data tends to shift in blocks)
    while t < n:
        # Try three ways to find the bytes at target position t in the source,
        # cheapest first, and keep the longest match.
        best_kind, best_len, best_sp = None, 0, 0
        # 1. Unchanged at the same position (SourceRead)
        if t < len(src):
            ln = match_len(t, t)
            if ln >= 4:
                best_kind, best_len = SOURCE_READ, ln
        # 2. Shifted by the same amount as the previous copy
        if best_len < MIN_MATCH:
            sp = t + last_delta
            if 0 <= sp < len(src):
                ln = match_len(sp, t)
                if ln > best_len and ln >= 8:
                    best_kind, best_len, best_sp = SOURCE_COPY, ln, sp
        # 3. Look it up in the index. The index only has every STEP-th source
        #    position, so try target offsets t..t+7 to line up with one of them.
        if best_len < MIN_MATCH:
            for k in range(STEP):
                key = tgt[t + k:t + k + MIN_MATCH]
                sp = index.get(key)
                if sp is not None and sp - k >= 0:
                    ln = match_len(sp - k, t)
                    if ln > best_len and ln >= MIN_MATCH:
                        best_kind, best_len, best_sp = SOURCE_COPY, ln, sp - k
        if best_kind is None:
            # No match: this byte is new data; add it to the pending literal run
            if literal_start is None:
                literal_start = t
            t += 1
            continue
        flush_literal(t)
        # Each instruction number is (length - 1) << 2 | type
        if best_kind == SOURCE_READ:
            out.extend(enc_num(((best_len - 1) << 2) | SOURCE_READ))
        else:
            out.extend(enc_num(((best_len - 1) << 2) | SOURCE_COPY))
            out.extend(enc_signed(best_sp - src_rel))
            src_rel = best_sp + best_len
            last_delta = best_sp - t
        t += best_len
    flush_literal(n)

    # Footer: CRC32 of source, target, and of the patch so far
    out += zlib.crc32(src).to_bytes(4, 'little')
    out += zlib.crc32(tgt).to_bytes(4, 'little')
    out += zlib.crc32(out).to_bytes(4, 'little')
    return bytes(out)


def apply(src, patch):
    """Apply a BPS patch to `src` and return the patched ROM, checking all checksums."""
    if patch[:4] != b'BPS1':
        raise ValueError('not a BPS patch')
    # The last 12 bytes are: source CRC, target CRC, patch CRC
    if zlib.crc32(patch[:-4]) != int.from_bytes(patch[-4:], 'little'):
        raise ValueError('patch file is corrupt')
    if zlib.crc32(src) != int.from_bytes(patch[-12:-8], 'little'):
        raise ValueError('wrong source ROM (CRC32 mismatch) - check game version/revision')
    pos = 4
    src_size, pos = dec_num(patch, pos)
    tgt_size, pos = dec_num(patch, pos)
    meta_size, pos = dec_num(patch, pos)
    pos += meta_size  # metadata is free text; skip it
    tgt = bytearray(tgt_size)
    out = src_rel = tgt_rel = 0  # write position, and the two relative read cursors
    end = len(patch) - 12
    while pos < end:
        data, pos = dec_num(patch, pos)
        cmd, ln = data & 3, (data >> 2) + 1
        if cmd == SOURCE_READ:
            tgt[out:out + ln] = src[out:out + ln]
        elif cmd == TARGET_READ:
            tgt[out:out + ln] = patch[pos:pos + ln]; pos += ln
        else:
            # SourceCopy / TargetCopy: move the read cursor by a signed offset, then copy
            d, pos = dec_num(patch, pos)
            d = -(d >> 1) if d & 1 else d >> 1
            if cmd == SOURCE_COPY:
                src_rel += d
                tgt[out:out + ln] = src[src_rel:src_rel + ln]; src_rel += ln
            else:
                # TargetCopy may overlap what it's writing, so copy byte by byte
                tgt_rel += d
                for i in range(ln):
                    tgt[out + i] = tgt[tgt_rel]; tgt_rel += 1
        out += ln
    if zlib.crc32(tgt) != int.from_bytes(patch[-8:-4], 'little'):
        raise ValueError('output CRC32 mismatch')
    return bytes(tgt)


if __name__ == '__main__':
    if len(sys.argv) != 5 or sys.argv[1] not in ('create', 'apply'):
        sys.exit(__doc__)
    a = open(sys.argv[2], 'rb').read()
    b = open(sys.argv[3], 'rb').read()
    result = create(a, b) if sys.argv[1] == 'create' else apply(a, b)
    open(sys.argv[4], 'wb').write(result)
    print('wrote %s (%d bytes)' % (sys.argv[4], len(result)))
