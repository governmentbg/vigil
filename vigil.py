#!/usr/bin/env python
'''
vigil, v0.1, (c) Alex Stanev <a.stanev@is-bg.net>
License: MIT
Base OS stats monitoring
Pull nginx-rtmp-module stats

Python dependencies: psutil, xmltodict
sudo apt install python3-psutil python3-xmltodict
'''

import json
import xmltodict
import time
import socket
import psutil
from psutil._common import bytes2human
import ssl
from urllib.request import urlopen


class Vigil(object):
    res = {}

    def __init__(self):
        self.res['hostname'] = socket.gethostname()
        self.res['timestamp'] = round(time.time())

    def getCPU(self):
        self.res['load'] = [round(e, 2) for e in psutil.getloadavg()]
        self.res['cpu_percent'] = [round(e / psutil.cpu_count() * 100, 2) for e in self.res['load']]

    def getMem(self):
        self.res['mem_percent_used'] = psutil.virtual_memory().percent

    def getDiskUsage(self):
        self.res['disk_usage'] = {}
        for p in psutil.disk_partitions():
            if p.fstype in ['ext4', 'xfs', 'btrfs']:
                self.res['disk_usage'][p.mountpoint] = psutil.disk_usage(p.mountpoint).percent

    def getPerf(self, sec=5):
        self.res['perf'] = {}

        net_before = psutil.net_io_counters()
        io_before = psutil.disk_io_counters()
        
        time.sleep(sec)
        
        net_after = psutil.net_io_counters()
        io_after = psutil.disk_io_counters()
        
        self.res['perf']['net_sent'] = bytes2human((net_after.bytes_sent - net_before.bytes_sent) / sec) + '/s'
        self.res['perf']['net_recv'] = bytes2human((net_after.bytes_recv - net_before.bytes_recv) / sec) + '/s'
        self.res['perf']['io_read']  = bytes2human((io_after.read_bytes  - io_before.read_bytes)  / sec) + '/s'
        self.res['perf']['io_write'] = bytes2human((io_after.write_bytes - io_before.write_bytes) / sec) + '/s'

    def getRTMPstats(self, url='https://localhost/stats', to=5):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            resp = urlopen(url, context=ctx, timeout=to)
            stats_xml = resp.read()
            resp.close()
            
            self.res['rtmp_stats'] = xmltodict.parse(stats_xml)
        except:
            None

    def run(self):
        self.getCPU()
        self.getMem()
        self.getDiskUsage()
        self.getPerf()

        if self.res['hostname'].find('ingest') != -1:
            self.getRTMPstats()

        print(json.dumps(self.res))
        

if __name__ == "__main__":
    v = Vigil()
    v.run()
