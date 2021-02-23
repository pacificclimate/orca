import re
from math import ceil


def split_url(url, size, req_limit=5e8):
    if size / 2 > req_limit:
        start_end_format = re.compile(r"(([a-z]+)\[(\d*)(:\d*){0,1}:(\d*)\])")
        var_time, var, start, stride, end = start_end_format.findall(url)[0]
        start = int(start)
        end = int(end)

        # Server error reports dataset size = dataset.nbytes/2
        b = size / 2
        chunks = ceil(b / req_limit)
        total = end - start
        step = int(total // chunks)

        chunk_end = start + step
        urls = []

        while chunk_end < end:
            urls.append(url.replace(var_time, f"{var}[{start}{stride}:{chunk_end}]"))
            start = chunk_end + 1
            chunk_end += step

        if start <= end:
            urls.append(url.replace(var_time, f"{var}[{start}{stride}:{end}]"))

        return urls

    else:
        return [url]
