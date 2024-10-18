import os
import time
import numpy as np
import yaml
from algorithm.period_encode import get_period
from algorithm.period_encode import separate_storage
from algorithm.period_encode import get_beta
from algorithm.period_encode import encode_dataf_with_beta
from algorithm.period_encode import encode_with_beta_estimate
from algorithm.ts_2diff_encode import encode_block
from mylib.byteToys import byteOutToys

max_size: int = 2**32 - 1
max_value: int = 2**32 - 1
group_size = 8

min_period_count = 4
min_sample_length = 500
part_size = 1024


def period_completion(data: list[int], p: int) -> list[int]:
    n = len(data)
    if len(data) % p == 0:
        return data
    return data + data[-p : -(len(data) % p)]


def period_completion_average(data: list[int], p: int) -> list[int]:
    if len(data) % p == 0:
        return data
    data_extra = [0] * (p - len(data) % p)
    count = 0
    for i in range(0, len(data), p):
        if i + p - 1 < len(data):
            count += 1
            for j in range(p - len(data) % p):
                data_extra[len(data_extra) - 1 - j] += data[i + p - 1 - j]
    for i in range(len(data_extra)):
        data_extra[i] = data_extra[i] // count
    return data + data_extra


def separate_storage_part(
    stream: byteOutToys, data: list[int], use_separate: bool = True
):
    stream.encode(len(data), max_size.bit_length())
    for i in range(0, len(data), part_size):
        if use_separate:
            separate_storage(
                stream,
                data[i : int(min(i + part_size, len(data)))],
                encode_length=False,
            )
        else:
            encode_block(
                stream, data[i : int(min(i + part_size, len(data)))], deltaed=True
            )
    return


def encode_with_beta_part(
    stream: byteOutToys,
    data: list[int],
    dataf,
    p: int,
    beta: int,
    use_separate: bool = True,
):
    res = encode_dataf_with_beta(stream, data, dataf, p, beta)
    separate_storage_part(stream, res, use_separate=use_separate)


def get_period_segment(data: list[int]) -> int:
    with open(
        os.path.join("mylib", "pure_draw_config.yaml"), "r", encoding="utf-8"
    ) as f:
        config = yaml.full_load(f)
    n = len(data)
    sample_length = int(max(n // min_period_count, min(min_sample_length, n)))
    sample = data[:sample_length]
    p = get_period(sample, config["p"], config["k"])
    return p


def get_period_sample(data: list[int]) -> int:
    with open(
        os.path.join("mylib", "pure_draw_config.yaml"), "r", encoding="utf-8"
    ) as f:
        config = yaml.full_load(f)
    n = len(data)
    sample_length = int(max(n // min_period_count, min(min_sample_length, n)))
    k = max(1, n // sample_length)
    sample = data[::k]
    p = get_period(sample, config["p"], config["k"]) * k
    return p


def get_beta_no_completion(data: list[int], dataf) -> int:
    n = len(data)
    result = encode_with_beta_estimate(data, dataf, n, 0)
    beta = 0
    for current_beta in range(-16, 16):
        if current_beta != 0:
            tmp = encode_with_beta_estimate(data, dataf, n, current_beta)
            if result == -1 or (tmp != -1 and tmp < result):
                result = tmp
                beta = current_beta
    return beta


def period_encode_param(
    data: list[int],
    file_path: str,
    use_segment: bool = False,
    use_average: bool = False,
    use_separate: bool = True,
    use_completion: bool = True,
) -> tuple[int, float]:
    time_current = 0
    start = time.time()
    stream = byteOutToys()
    n = len(data)
    if n != 0:
        if use_completion:
            if use_segment:
                p = get_period_segment(data)
            else:
                p = get_period_sample(data)
            stream.encode(p, max_size.bit_length())
            if p == 0:
                data = [data[0]] + np.diff(data).tolist()
                separate_storage_part(stream, data, use_separate=use_separate)
            else:
                data_full = (
                    period_completion(data, p)
                    if not use_average
                    else period_completion_average(data, p)
                )
                sum_full = [0] * p
                for i in range(len(data_full)):
                    sum_full[i % p] += data_full[i]
                k = len(data_full) // p
                for i in range(p):
                    sum_full[i] /= k
                dataf = np.fft.rfft(sum_full)
                end = time.time()
                time_current += end - start
                beta = get_beta(data, dataf, p)
                start = time.time()
                stream.encode(0 if beta >= 0 else 1, 1)
                stream.encode(np.abs(beta), max_value.bit_length().bit_length())
                encode_with_beta_part(
                    stream, data, dataf, p, beta, use_separate=use_separate
                )
        else:
            stream.encode(n, max_size.bit_length())
            dataf = np.fft.rfft(data)
            end = time.time()
            time_current += end - start
            beta = get_beta_no_completion(data, dataf)
            start = time.time()
            stream.encode(0 if beta >= 0 else 1, 1)
            stream.encode(np.abs(beta), max_value.bit_length().bit_length())
            encode_with_beta_part(
                stream, data, dataf, n, beta, use_separate=use_separate
            )
    stream.flush()
    result = len(stream.byte_stream)
    stream.write(file_path)
    end = time.time()
    time_current += end - start
    return result, time_current
