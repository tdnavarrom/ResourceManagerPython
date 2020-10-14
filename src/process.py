import psutil

def get_disk_usage(disk_partition):
    disk_usage = psutil.disk_usage(disk_partition)
    return disk_usage

def get_disk_paritions():
    return psutil.disk_partitions()

def get_current_processes():
    procs = {p.pid: p.info for p in psutil.process_iter(['name', 'memory_percent', 'cpu_num'])}
    return procs

def kill_process(pid):
    p = psutil.Process(pid)
    p.terminate()

