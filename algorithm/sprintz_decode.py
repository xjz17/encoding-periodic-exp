import numpy as np
from mylib.byteToys import byteInToys


def decode_block(stream: byteInToys) -> list[int]:
    first_value = stream.decode(32)
    delta_length = stream.decode(8)
    if delta_length == 0:
        return [first_value]
    bit_length = stream.decode(8)
    delta = []
    for _ in range(delta_length):
        tmp = stream.decode(bit_length)
        if tmp % 2 == 0:
            tmp = -tmp // 2
        else:
            tmp = (tmp + 1) // 2
        delta.append(tmp)
    return np.cumsum([first_value] + delta).tolist()


def sprintz_decode_wrap(stream: byteInToys) -> list[int]:
    result = []
    realBcnt = stream.decode(32)
    for tmp in range(realBcnt):
        result += decode_block(stream)
    for i in range(len(result)):
        if result[i] >= 1 << 31:
            result[i] -= 1 << 32
    return result


def sprintz_decode(file_path: str) -> list[int]:
    stream = byteInToys(file_path)
    return sprintz_decode_wrap(stream)


# print(ts_2diff_decode("result.bin"))
