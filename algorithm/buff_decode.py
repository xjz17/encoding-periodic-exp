from mylib.byteToys import byteInToys
from mylib.byteToys import byteOutToys
import math

bits_needed = [0, 5, 8, 11, 15, 18, 21, 25, 28, 31, 35]


def buff_decode(file_path: str) -> list[int]:
    stream = byteInToys(file_path)
    result = []
    result_len = stream.decode(32)
    precision = stream.decode(32)
    if result_len == 0:
        return result
    frac_bit = math.ceil(math.log2(10**precision))
    if precision >= 0 and precision < len(bits_needed):
        frac_bit = bits_needed[precision]
    min_value = stream.decode(32)
    int_bit = stream.decode(32)
    bytes_group: list[byteOutToys] = []
    for _ in range(result_len):
        bytes_group.append(byteOutToys())
    for _ in range(int((int_bit + frac_bit + 7) / 8)):
        for i in range(result_len):
            bytes_group[i].encode(stream.decode(8), 8)
    for i in range(result_len):
        stream_single = bytes_group[i].dump()
        int_part = stream_single.decode(int_bit)
        frac_part = stream_single.decode(frac_bit)
        frac_part_int = math.ceil(frac_part * (10**precision) / (2**frac_bit))
        value = int_part * (10**precision) + frac_part_int + min_value * (10**precision)
        value = value % (1 << 32)
        if value >= 1 << 31:
            value -= 1 << 32
        result.append(value)
    return result
