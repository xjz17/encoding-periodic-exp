import numpy as np
from mylib.byteToys import byteInToys
from algorithm.sprintz_decode import sprintz_decode_wrap

END_CODE = (1 << 31) - 1
result = []
tag_global = []
tag_global_index = 0
result_global = []
result_global_index = 0


def hire(l: int, r: int, d_value: int):
    global tag_global, tag_global_index, result_global, result_global_index
    tag_cur = tag_global[tag_global_index]
    tag_global_index += 1
    if tag_cur == 0:
        for i in range(l, r + 1):
            result[i] = d_value
            return
    d_cur = result_global[result_global_index]
    result_global_index += 1
    if l == r:
        result[l] = (d_value + d_cur) & ((1 << 32) - 1)
        return
    mid = (l + r) // 2
    hire(l, mid, (d_value + d_cur) & ((1 << 32) - 1))
    hire(mid + 1, r, (d_value + d_cur) & ((1 << 32) - 1))
    return


def hire_decode(file_path: str) -> list[int]:
    global result, tag_global, tag_global_index, result_global, result_global_index
    result = []
    tag_global = []
    tag_global_index = 0
    result_global = []
    result_global_index = 0
    stream = byteInToys(file_path)
    result_len = stream.decode(32)
    if result_len == 0:
        return []
    result = [0] * result_len
    tag_global = sprintz_decode_wrap(stream)
    tag_global_index = 0
    result_global = sprintz_decode_wrap(stream)
    result_global_index = 0
    hire(0, result_len - 1, 0)
    for i in range(len(result)):
        if result[i] >= 1 << 31:
            result[i] -= 1 << 32
    return result
