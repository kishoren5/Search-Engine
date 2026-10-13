from collections.abc import Sequence


def delta_encode(sorted_integers: Sequence[int]) -> list[int]:
    """Delta-encode a strictly monotonically increasing list of non-negative integers.

    Example: [10, 15, 23, 24] -> [10, 5, 8, 1]
    """
    if not sorted_integers:
        return []

    deltas: list[int] = [sorted_integers[0]]
    prev = sorted_integers[0]
    for current in sorted_integers[1:]:
        if current < prev:
            raise ValueError(f"Input sequence must be strictly sorted: {current} < {prev}")
        deltas.append(current - prev)
        prev = current

    return deltas


def delta_decode(deltas: Sequence[int]) -> list[int]:
    """Decode a list of deltas back to original sorted integers.

    Example: [10, 5, 8, 1] -> [10, 15, 23, 24]
    """
    if not deltas:
        return []

    original: list[int] = [deltas[0]]
    current = deltas[0]
    for delta in deltas[1:]:
        if delta < 0:
            raise ValueError(f"Delta cannot be negative: {delta}")
        current += delta
        original.append(current)

    return original


def vbyte_encode_number(n: int) -> bytearray:
    """Encode a single non-negative integer using 7-bit variable-byte encoding."""
    if n < 0:
        raise ValueError(f"Cannot encode negative integer: {n}")

    out = bytearray()
    while True:
        byte = n & 0x7F
        n >>= 7
        if n > 0:
            out.append(byte)
        else:
            # Set high bit (continuation flag / termination bit)
            out.append(byte | 0x80)
            break
    return out


def vbyte_encode(numbers: Sequence[int]) -> bytes:
    """Encode a sequence of non-negative integers into a contiguous VByte byte string."""
    buf = bytearray()
    for n in numbers:
        buf.extend(vbyte_encode_number(n))
    return bytes(buf)


def vbyte_decode(data: bytes | memoryview) -> list[int]:
    """Decode a VByte byte string into a list of integers."""
    numbers: list[int] = []
    current_num = 0
    shift = 0

    for byte in data:
        if byte & 0x80:
            # Last byte for this number
            current_num |= (byte & 0x7F) << shift
            numbers.append(current_num)
            current_num = 0
            shift = 0
        else:
            current_num |= (byte & 0x7F) << shift
            shift += 7

    return numbers


def compress_postings(doc_ids: Sequence[int], term_frequencies: Sequence[int]) -> bytes:
    """Compress paired doc_ids and term_frequencies using delta + VByte.

    Format:
    - 4-byte header: count of postings (uint32)
    - VByte encoded doc_id deltas
    - VByte encoded term frequencies
    """
    if len(doc_ids) != len(term_frequencies):
        raise ValueError("doc_ids and term_frequencies lengths must match")

    count = len(doc_ids)
    if count == 0:
        return (0).to_bytes(4, byteorder="little")

    deltas = delta_encode(doc_ids)
    doc_bytes = vbyte_encode(deltas)
    tf_bytes = vbyte_encode(term_frequencies)

    header = count.to_bytes(4, byteorder="little")
    doc_len = len(doc_bytes).to_bytes(4, byteorder="little")

    return header + doc_len + doc_bytes + tf_bytes


def decompress_postings(data: bytes | memoryview) -> tuple[list[int], list[int]]:
    """Decompress paired doc_ids and term_frequencies from compressed binary representation."""
    if len(data) < 4:
        return [], []

    count = int.from_bytes(data[0:4], byteorder="little")
    if count == 0:
        return [], []

    doc_bytes_len = int.from_bytes(data[4:8], byteorder="little")
    doc_bytes = data[8 : 8 + doc_bytes_len]
    tf_bytes = data[8 + doc_bytes_len :]

    deltas = vbyte_decode(doc_bytes)
    doc_ids = delta_decode(deltas)
    tfs = vbyte_decode(tf_bytes)

    return doc_ids, tfs
