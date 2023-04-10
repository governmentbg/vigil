# vigil



## What?

This is a simple python script to send base OS data to stats collector. It also pulls stats from nginx-rtmp-module's XML if the current machine is ingest node, based on the node hostname.

## Dependencies

```
sudo apt install python3-psutil python3-xmltodict
```

## Usage

Cron it like this:
```
./vigil.py | curl -k -H "Content-Type: application/json" -X POST --data-binary @- https://api
```

## Example result

### Only basic data

```
{"hostname": "osi", "timestamp": 1679821063, "load": [0.68, 0.69, 0.65], "cpu_percent": [8.5, 8.62, 8.12], "mem_percent_used": 66.0, "disk_usage": {"/": 98.3, "/home": 98.3, "/media/veracrypt1": 93.6, "/media/veracrypt2": 92.5, "/media/veracrypt3": 96.2}, "perf": {"net_sent": "42.4B/s", "net_recv": "13.2B/s", "io_read": "0.0B/s", "io_write": "3.4M/s"}}
```

### Ingest node with zero streams

```
{"hostname": "osi", "timestamp": 1679821129, "load": [1.38, 0.92, 0.73], "cpu_percent": [17.25, 11.5, 9.12], "mem_percent_used": 66.3, "disk_usage": {"/": 98.3, "/home": 98.3, "/media/veracrypt1": 93.6, "/media/veracrypt2": 92.5, "/media/veracrypt3": 96.2}, "perf": {"net_sent": "7.0K/s", "net_recv": "11.0K/s", "io_read": "0.0B/s", "io_write": "0.0B/s"}, "rtmp_stats": {"rtmp": {"nginx_version": "1.21.4", "nginx_rtmp_version": "1.1.4", "built": "Jul 12 2022 04:07:30", "pid": "1318194", "uptime": "405199", "naccepted": "9", "bw_in": "0", "bytes_in": "52738530", "bw_out": "0", "bytes_out": "3681", "server": {"application": [{"name": "test-setup", "live": {"nclients": "0"}}, {"name": "test-sik", "live": {"nclients": "0"}}, {"name": "real", "live": {"nclients": "0"}}]}}}}
```

### Ingest node with one stream

```
{"hostname": "osi", "timestamp": 1679821231, "load": [0.78, 0.82, 0.72], "cpu_percent": [9.75, 10.25, 9.0], "mem_percent_used": 66.3, "disk_usage": {"/": 98.3, "/home": 98.3, "/media/veracrypt1": 93.6, "/media/veracrypt2": 92.5, "/media/veracrypt3": 96.2}, "perf": {"net_sent": "345.8B/s", "net_recv": "309.6B/s", "io_read": "0.0B/s", "io_write": "56.0K/s"}, "rtmp_stats": {"rtmp": {"nginx_version": "1.21.4", "nginx_rtmp_version": "1.1.4", "built": "Jul 12 2022 04:07:30", "pid": "1318194", "uptime": "405302", "naccepted": "10", "bw_in": "1208816", "bytes_in": "55283160", "bw_out": "320", "bytes_out": "4090", "server": {"application": [{"name": "test-setup", "live": {"nclients": "0"}}, {"name": "test-sik", "live": {"nclients": "0"}}, {"name": "real", "live": {"stream": {"name": "010100003", "time": "16192", "bw_in": "1203504", "bytes_in": "2535387", "bw_out": "0", "bytes_out": "0", "bw_audio": "61240", "bw_video": "1142264", "client": {"id": "5049478", "address": "37.63.23.227", "time": "16440", "flashver": "FMLE/3.0 (compatible; SIK-Strea", "dropped": "0", "avsync": "7", "timestamp": "17960", "publishing": null, "active": null}, "meta": {"video": {"width": "1280", "height": "720", "frame_rate": "0", "codec": "H264", "profile": "Main", "compat": "192", "level": "4.2"}, "audio": {"codec": "AAC", "profile": "LC", "channels": "1", "sample_rate": "44100"}}, "nclients": "1", "publishing": null, "active": null}, "nclients": "1"}}]}}}}
```

## License
MIT
