import numpy as np
import pandas as pd
from mylib.byteToys import byteOutToys

PREVIOUS_VALUES = 128
PREVIOUS_VALUES_LOG2 = int(np.log2(PREVIOUS_VALUES))
THRESHOLD = 6 + PREVIOUS_VALUES_LOG2
SET_LSB = 2 ** (THRESHOLD + 1) - 1

LEADING_REPRESENTATION = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    2,
    2,
    2,
    2,
    3,
    3,
    4,
    4,
    5,
    5,
    6,
    6,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
    7,
]

LEADING_ROUND = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    8,
    8,
    8,
    8,
    12,
    12,
    12,
    12,
    16,
    16,
    18,
    18,
    20,
    20,
    22,
    22,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
    24,
]

stored_values: list[int] = []
indices: list[int] = []
index = 0
stored_leading_zeros = 0


def leadingzero(x: int) -> int:
    if x < 0:
        return 0
    elif x == 0:
        return 32
    return 32 - x.bit_length()


def trailingzero(x: int) -> int:
    if x == 0:
        return 32
    return (x - (x & (x - 1))).bit_length() - 1


def compress_value(stream: byteOutToys, value: int):
    global index, stored_leading_zeros
    previous_index = 0
    xor = 0
    trailing_zeros = 0
    key = value & SET_LSB
    cur_index = indices[key]
    if cur_index != -1 and (index - cur_index) < PREVIOUS_VALUES:
        tmp_xor = value ^ stored_values[cur_index % PREVIOUS_VALUES]
        trailing_zeros = trailingzero(tmp_xor)
        if trailing_zeros > THRESHOLD:
            previous_index = cur_index % PREVIOUS_VALUES
            xor = tmp_xor
        else:
            previous_index = index % PREVIOUS_VALUES
            xor = stored_values[previous_index] ^ value
    else:
        previous_index = index % PREVIOUS_VALUES
        xor = stored_values[previous_index] ^ value
    if xor == 0:
        # case 00
        stream.encode(0, 2)
        stream.encode(previous_index, PREVIOUS_VALUES_LOG2)
        stored_leading_zeros = 32 + 1
    else:
        leading_zeros = LEADING_ROUND[leadingzero(xor)]
        if trailing_zeros > THRESHOLD:
            # case 01
            stream.encode(1, 2)
            stream.encode(previous_index, PREVIOUS_VALUES_LOG2)
            stream.encode(LEADING_REPRESENTATION[leading_zeros], 3)
            significant_bits = 32 - leading_zeros - trailing_zeros
            stream.encode(significant_bits, 6)
            stream.encode(xor >> trailing_zeros, significant_bits)
            stored_leading_zeros = 32 + 1
        elif leading_zeros == stored_leading_zeros:
            stream.encode(2, 2)
            significant_bits = 32 - leading_zeros
            stream.encode(xor, significant_bits)
        else:
            stream.encode(3, 2)
            stored_leading_zeros = leading_zeros
            stream.encode(LEADING_REPRESENTATION[leading_zeros], 3)
            significant_bits = 32 - leading_zeros
            stream.encode(xor, significant_bits)
    index += 1
    indices[key] = index
    stored_values[index % PREVIOUS_VALUES] = value


def chimp_encode(data: list[int], file_path: str) -> int:
    global index, indices, stored_values
    stream = byteOutToys()
    indices = [-1] * (2 ** (THRESHOLD + 1))
    stored_values = [0] * PREVIOUS_VALUES
    stream.encode(len(data), 32)
    stream.encode(data[0], 32)
    index = 0
    indices[data[0] & SET_LSB] = index
    stored_values[0] = data[0]
    for i in range(1, len(data)):
        compress_value(stream, data[i])
    stream.flush()
    result = len(stream.byte_stream)
    stream.write(file_path)
    return result


# def gorilla_com(data: list[int]) -> float:
#     return gorilla(data) / (len(data) * 32)


# df = pd.read_csv("test.csv")
# print(gorilla_encode(df["value"].tolist(), "result.bin"))
