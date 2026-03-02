import sys
import time
import requests

NUM_REQUESTS = 10

def measure_register_latency(base_url, num_requests):
    latencies = []
    for i in range(num_requests):
        payload = {"username": f"latency_test_user_{i}_{int(time.time()*1000)}"}
        start = time.time()
        requests.post(f"{base_url}/register", json=payload)
        elapsed = time.time() - start
        latencies.append(elapsed)
    return latencies

def measure_list_latency(base_url, num_requests):
    latencies = []
    for i in range(num_requests):
        start = time.time()
        requests.get(f"{base_url}/list")
        elapsed = time.time() - start
        latencies.append(elapsed)
    return latencies

def clear_users(base_url):
    requests.post(f"{base_url}/clear")

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <INSTANCE_A_URL> <INSTANCE_B_URL>")
        print(f"Example: python {sys.argv[0]} http://34.1.2.3:8080 http://35.4.5.6:8080")
        sys.exit(1)

    instance_a = sys.argv[1].rstrip("/")
    instance_b = sys.argv[2].rstrip("/")

    results = {}

    for label, url in [("us-central1", instance_a), ("europe-west1", instance_b)]:
        clear_users(url)

        reg_latencies = measure_register_latency(url, NUM_REQUESTS)
        list_latencies = measure_list_latency(url, NUM_REQUESTS)

        avg_reg = sum(reg_latencies) / len(reg_latencies)
        avg_list = sum(list_latencies) / len(list_latencies)

        results[label] = {
            "register_avg": avg_reg,
            "list_avg": avg_list,
            "register_all": reg_latencies,
            "list_all": list_latencies,
        }

        clear_users(url)

    print("=" * 60)
    print("Latency Measurement Results")
    print("=" * 60)

    for label in ["us-central1", "europe-west1"]:
        r = results[label]
        print(f"\n--- {label} ---")
        print(f"/register average latency: {r['register_avg']*1000:.2f} ms")
        print(f"  Individual: {', '.join(f'{l*1000:.2f}' for l in r['register_all'])} ms")
        print(f"/list     average latency: {r['list_avg']*1000:.2f} ms")
        print(f"  Individual: {', '.join(f'{l*1000:.2f}' for l in r['list_all'])} ms")

    print()

if __name__ == "__main__":
    main()
