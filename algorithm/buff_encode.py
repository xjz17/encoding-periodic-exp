import math
from mylib.byteToys import byteOutToys

bits_needed = [0, 5, 8, 11, 15, 18, 21, 25, 28, 31, 35]


def buff_encode(data: list[int], file_path: str, precision: int):
    stream = byteOutToys()
    stream.encode(len(data), 32)
    stream.encode(precision, 32)
    if len(data) == 0:
        stream.flush()
        result = len(stream.byte_stream)
        stream.write(file_path)
        return result
    frac_bit = math.ceil(math.log2(10**precision))
    if precision >= 0 and precision < len(bits_needed):
        frac_bit = bits_needed[precision]
    min_value: int = math.floor(data[0] / (10**precision))
    max_value: int = math.floor(data[0] / (10**precision))
    for value in data:
        min_value = min(min_value, math.floor(value / (10**precision)))
        max_value = max(max_value, math.floor(value / (10**precision)))
    int_bit = math.ceil(math.log2(max_value - min_value + 1))
    stream.encode(min_value, 32)
    stream.encode(int_bit, 32)
    bytes_group: list[byteOutToys] = []
    for value in data:
        bytes_group.append(byteOutToys())
        tmp = value // (10**precision)
        bytes_group[-1].encode(tmp - min_value, int_bit)
        frac_part_int = (value - min_value * (10**precision)) % (10**precision)
        frac_part = frac_part_int * (2**frac_bit) // (10**precision)
        bytes_group[-1].encode(frac_part, frac_bit)
    for _ in range(int((int_bit + frac_bit + 7) / 8)):
        for i in range(len(bytes_group)):
            bytes_group[i].write_one(stream)
    stream.flush()
    result = len(stream.byte_stream)
    stream.write(file_path)
    return result
