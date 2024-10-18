import numpy as np
from mylib.byteToys import byteOutToys

block_size = 128


def encode_block(stream: byteOutToys, data: list[int]):
    delta = np.diff(data)
    stream.encode(data[0], 32)
    stream.encode(len(delta), 8)
    if len(delta) == 0:
        return
    bit_len = 0
    for i in range(len(delta)):
        if delta[i] > 0:
            delta[i] = delta[i] * 2 - 1
        else:
            delta[i] = -delta[i] * 2
        bit_len = max(bit_len, int(delta[i]).bit_length())
    # first_value + min_delta + len(delta) + bit_len + delta
    stream.encode(bit_len, 8)
    for d in delta:
        stream.encode(d, bit_len)
    return


def sprintz_encode_wrap(stream: byteOutToys, data: list[int]):
    bcnt = len(data) // block_size
    realBcnt = (len(data) + block_size - 1) // block_size
    stream.encode(realBcnt, 32)
    for i in range(bcnt):
        encode_block(stream, data[i * block_size : (i + 1) * block_size])
    if bcnt * block_size < len(data):
        encode_block(stream, data[bcnt * block_size :])


def sprintz_encode(data: list[int], file_path: str):
    stream = byteOutToys()
    sprintz_encode_wrap(stream, data)
    stream.flush()
    result = len(stream.byte_stream)
    stream.write(file_path)
    return result
