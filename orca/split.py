import re


def split_url(url, size):
    start_end_format = re.compile(r"(([a-z]+)\[(\d*)(:\d*){0,1}:(\d*)\])")
    var_time, var, start, stride, end = start_end_format.findall(url)[0]
    start = int(start)
    end = int(end)

    # Server error reports dataset size = dataset.nbytes/2
    b = size / 2
    # Request limit is 5e+8 bytes
    chunks = -(-b // 5e8)  # take ceiling
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
