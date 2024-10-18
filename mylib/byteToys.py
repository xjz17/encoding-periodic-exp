class byteOutToys:
    def __init__(self):
        self.byte_length: int = 8
        self.byte_stream = bytearray()
        self.byte_stream_index = 0
        self.current_bytes: int = 0
        self.bit_index: int = 0

    def smallFlush(self):
        while self.bit_index >= self.byte_length:
            self.byte_stream.append(
                self.current_bytes >> (self.bit_index - self.byte_length)
            )
            self.current_bytes &= (1 << (self.bit_index - self.byte_length)) - 1
            self.bit_index -= self.byte_length

    def encode(self, x: int, k: int):
        x = int(x)
        k = int(k)
        x &= (1 << k) - 1
        self.current_bytes <<= k
        self.current_bytes |= x
        self.bit_index += k
        self.smallFlush()

    def flush(self):
        self.smallFlush()
        if self.bit_index > 0:
            self.byte_stream.append(
                self.current_bytes << (self.byte_length - self.bit_index)
            )
            self.current_bytes = 0
            self.bit_index = 0

    def write(self, file_path):
        self.flush()
        with open(file_path, "wb") as f:
            f.write(self.byte_stream)

    def write_one(self, another: "byteOutToys"):
        self.flush()
        if self.byte_stream_index < len(self.byte_stream):
            another.encode(self.byte_stream[self.byte_stream_index], self.byte_length)
            self.byte_stream_index += 1

    def dump(self) -> "byteInToys":
        result = byteInToys("")
        self.flush()
        result.byte_stream = self.byte_stream
        return result


class byteInToys:
    def __init__(self, file_path: str):
        self.byte_length = 8
        self.current_bytes = 0
        self.bit_index = 0
        if file_path != "":
            with open(file_path, "rb") as f:
                self.byte_stream = bytearray(f.read())
        else:
            self.byte_stream = []
        self.byte_stream_index = 0

    def decode(self, k: int) -> int:
        k = int(k)
        while self.bit_index < k:
            self.current_bytes <<= self.byte_length
            self.current_bytes |= self.byte_stream[self.byte_stream_index]
            self.byte_stream_index += 1
            self.bit_index += self.byte_length
        result = self.current_bytes >> (self.bit_index - k)
        self.current_bytes &= (1 << (self.bit_index - k)) - 1
        self.bit_index -= k
        return result
