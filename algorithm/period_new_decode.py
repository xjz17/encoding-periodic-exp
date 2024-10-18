import numpy as np
from mylib.byteToys import byteInToys
from mylib.round import comp_round_inverse
from algorithm.period_decode import descending_bit_packing_decode
from algorithm.period_decode import separate_storage_decode
from algorithm.ts_2diff_decode import decode_block

max_size: int = 2**32 - 1
max_value: int = 2**32 - 1
group_size = 8

part_size = 1024


def separate_storage_decode_part(
    stream: byteInToys,
    use_separate: bool = True,
) -> list[int]:
    data = []
    data_length = stream.decode(max_size.bit_length())
    for i in range(0, data_length, part_size):
        if use_separate:
            data += separate_storage_decode(
                stream,
                encode_length=False,
                data_length=int(min(i + part_size, data_length)) - i,
            )
        else:
            data += decode_block(stream, deltaed=True)
    for i in range(len(data)):
        if data[i] >= 1 << 31:
            data[i] -= 1 << 32
    return data


def period_decode(
    file_path: str,
    use_separate: bool = True,
) -> list[int]:
    stream = byteInToys(file_path)
    p = stream.decode(max_size.bit_length())
    if p == 0:
        data = separate_storage_decode_part(stream, use_separate=use_separate)
        return np.cumsum(data).tolist()
    beta_sgn = stream.decode(1)
    beta = stream.decode(max_value.bit_length().bit_length())
    if beta_sgn == 1:
        beta *= -1
    dataf = comp_round_inverse(descending_bit_packing_decode(stream), beta)
    res = np.cumsum(
        separate_storage_decode_part(stream, use_separate=use_separate)
    ).tolist()
    return (
        np.tile(
            np.round(np.fft.irfft(dataf, n=p)).astype(np.int64),
            reps=((len(res) + p - 1) // p,),
        )[: len(res)]
        - res
    ).tolist()


# print(period_decode("result.bin"))
