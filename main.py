#!/home/pi/speedtest/env/bin/python
import speedtest
from influxdb import InfluxDBClient

servers = [21378]
threads = None

s = speedtest.Speedtest()
s.get_servers(servers)
s.download(threads=threads)
s.upload(threads=threads, pre_allocate=False)

download = s.results.download / 1e6
upload = s.results.upload / 1e6
ping = s.results.ping
# s.results.share()
# results_dict = s.results.dict()

speed_data = [
    {
        "measurement" : "internet_speed",
        "tags" : {
            "host": "my"
        },
        "fields" : {
            "download" : download,
            "upload"   : upload,
            "ping"     : ping
        }
    }
]

client = InfluxDBClient('localhost', 8086, 'speedmonitor', 'pimylifeup', 'internetspeed')
client.write_points(speed_data)

if __name__ == "__main__":
    import sys
    try:
        share = sys.argv[1]
        out = s.results.share()
        print(out)
    except IndexError:
        pass
