import re


def bisect_request(url):
    start_end_format = re.compile(r"(([a-z]+)\[(\d*)(:\d*){0,1}:(\d*)\])")
    print("\n" + str(start_end_format.findall(url)[0]) + "\n")
    var_time, var, start, step, end = start_end_format.findall(url)[0]

    mid = (int(start) + int(end)) // 2

    # step will either be ':n' or '' if there is no step
    url1 = url.replace(var_time, f"{var}[{start}{step}:{mid}]")
    url2 = url.replace(var_time, f"{var}[{mid+1}{step}:{end}]")

    return [url1, url2]
