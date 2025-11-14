# config gunicorn to do profiling
import cProfile

profile = cProfile.Profile()

print("gunicorn profiling configuration loaded")


def pre_request(worker, req):
    print("enabling profiler for request")
    profile.enable()


def post_request(worker, req):
    print("disabling profiler for request")
    profile.disable()


def worker_exit(server, worker):
    print("writing profiling results to file")
    profile.dump_stats("/app/profile.prof")
