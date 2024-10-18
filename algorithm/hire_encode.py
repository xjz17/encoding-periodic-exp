import numpy as np
from mylib.byteToys import byteOutToys
from algorithm.sprintz_encode import sprintz_encode_wrap

data_global = np.asarray([], dtype=np.int32)
tag_global = []
result_global = []
min_value = []
max_value = []


def compute(id: int, l: int, r: int):
    global data_global, min_value, max_value
    if l == r:
        min_value[id] = data_global[l]
        max_value[id] = data_global[l]
        return
    mid = (l + r) // 2
    compute(id * 2, l, mid)
    compute(id * 2 + 1, mid + 1, r)
    min_value[id] = min(min_value[id * 2], min_value[id * 2 + 1])
    max_value[id] = max(max_value[id * 2], max_value[id * 2 + 1])
    return


def hire(id: int, l: int, r: int, d_value: int):
    global min_value, max_value, tag_global, result_global
    min_cur = min_value[id] - d_value
    max_cur = max_value[id] - d_value
    if min_value == 0 and max_value == 0:
        tag_global.append(0)
        return
    d_cur = (min_cur + max_cur) // 2
    tag_global.append(1)
    result_global.append(d_cur)
    if l == r:
        return
    mid = (l + r) // 2
    hire(id * 2, l, mid, d_value + d_cur)
    hire(id * 2 + 1, mid + 1, r, d_value + d_cur)
    return


def hire_encode(data: list[int], file_path: str) -> int:
    global data_global, min_value, max_value, tag_global, result_global
    data_global = np.asarray([], dtype=np.int32)
    tag_global = []
    result_global = []
    min_value = []
    max_value = []
    stream = byteOutToys()
    stream.encode(len(data), 32)
    if len(data) != 0:
        data_global = np.asarray(data)
        min_value = [0] * (4 * len(data))
        max_value = [0] * (4 * len(data))
        compute(1, 0, len(data) - 1)
        hire(1, 0, len(data) - 1, 0)
    sprintz_encode_wrap(stream, tag_global)
    sprintz_encode_wrap(stream, result_global)
    stream.flush()
    result = len(stream.byte_stream)
    stream.write(file_path)
    return result
