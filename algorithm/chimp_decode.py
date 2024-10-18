import numpy as np
from mylib.byteToys import byteInToys

PREVIOUS_VALUES = 128
PREVIOUS_VALUES_LOG2 = int(np.log2(PREVIOUS_VALUES))
THRESHOLD = 6 + PREVIOUS_VALUES_LOG2
SET_LSB = 2 ** (THRESHOLD + 1) - 1

LEADING_REPRESENTATION = [0, 8, 12, 16, 18, 20, 22, 24]

stored_values: list[int] = []
index = 0
stored_leading_zeros = 0


def decompress_value(stream: byteInToys) -> int:
    global index, stored_values, stored_leading_zeros
    result = 0
    previous_index = 0
    cur_type = stream.decode(2)
    if cur_type == 0:
        previous_index = stream.decode(PREVIOUS_VALUES_LOG2)
        result = stored_values[previous_index]
        stored_leading_zeros = 32 + 1
    elif cur_type == 1:
        previous_index = stream.decode(PREVIOUS_VALUES_LOG2)
        leading_zeros = LEADING_REPRESENTATION[stream.decode(3)]
        significant_bits = stream.decode(6)
        trailing_zeros = 32 - leading_zeros - significant_bits
        result = stored_values[previous_index] ^ (
            stream.decode(significant_bits) << trailing_zeros
        )
        stored_leading_zeros = 32 + 1
    elif cur_type == 2:
        previous_index = index % PREVIOUS_VALUES
        leading_zeros = stored_leading_zeros
        significant_bits = 32 - leading_zeros
        result = stored_values[previous_index] ^ stream.decode(significant_bits)
    else:
        previous_index = index % PREVIOUS_VALUES
        leading_zeros = LEADING_REPRESENTATION[stream.decode(3)]
        stored_leading_zeros = leading_zeros
        significant_bits = 32 - leading_zeros
        result = stored_values[previous_index] ^ stream.decode(significant_bits)
    index += 1
    stored_values[index % PREVIOUS_VALUES] = result
    return result


def chimp_decode(file_path: str) -> list[int]:
    global index, stored_values
    stream = byteInToys(file_path)
    stored_values = [0] * PREVIOUS_VALUES
    length = stream.decode(32)
    first_value = stream.decode(32)
    result = [first_value]
    index = 0
    stored_values[0] = first_value
    for i in range(1, length):
        result.append(decompress_value(stream))

    for i in range(length):
        if result[i] >= 1 << 31:
            result[i] -= 1 << 32
    return result


# print(gorilla_decode("result.bin"))
