# Stress Linux machines
How to stesss CPU and memory of Linux machines

## Stress CPU
```
yes > /dev/null # 100% use of one CPU
sudo apt install stess-ng
stress-ng -c 2 -i 1 --vm-bytes 128M -t 10s
stress-ng --cpu 4 --io 2 --vm 1 --vm-bytes 1G --timeout 60s --metrics-brief
stress-ng --cpu 4 --io 2 --vm 1 --vm-bytes 1G --timeout 30s --metrics-brief
stress-ng -c 0 -l 40 # 40% for all CPUs
```

## Check machine status
```
cat /proc/loadavg  | awk '{load_pct=$1*100.00} END {print load_pct}'
sudo apt install sysstat
sar -u 1
sar -u 2
sar -u 0
mpstat
mpstat -P ALL
htop
```

## Interesting links
- [Check CPU usage](https://phoenixnap.com/kb/check-cpu-usage-load-linux)
- [Stress-ng man](https://manpages.ubuntu.com/manpages/artful/man1/stress-ng.1.html)
- [Stress-ng examples](https://www.cyberciti.biz/faq/stress-test-linux-unix-server-with-stress-ng/)
- [Stress-ng thread](https://serverfault.com/questions/796225/stress-ng-simulate-specific-cpu-percentages)
