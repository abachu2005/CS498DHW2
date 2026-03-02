import sys
import time
import requests

NUM_ITERATIONS = 100

def clear_users(url):
    requests.post(f"{url}/clear")

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <INSTANCE_A_URL> <INSTANCE_B_URL>")
        print(f"Example: python {sys.argv[0]} http://34.1.2.3:8080 http://35.4.5.6:8080")
        sys.exit(1)

    instance_a = sys.argv[1].rstrip("/")
    instance_b = sys.argv[2].rstrip("/")

    clear_users(instance_a)

    not_found_count = 0

    for i in range(NUM_ITERATIONS):
        username = f"consistency_user_{i}_{int(time.time()*1000)}"

        requests.post(f"{instance_a}/register", json={"username": username})

        resp = requests.get(f"{instance_b}/list")
        users = resp.json().get("users", [])

        if username not in users:
            not_found_count += 1

        if (i + 1) % 10 == 0:
            print(f"  Progress: {i + 1}/{NUM_ITERATIONS} iterations completed")

    print()
    print("=" * 60)
    print("Eventual Consistency Test Results")
    print("=" * 60)
    print(f"Total iterations:           {NUM_ITERATIONS}")
    print(f"Times username NOT found:   {not_found_count}")
    print(f"Times username found:       {NUM_ITERATIONS - not_found_count}")
    print(f"Inconsistency rate:         {not_found_count / NUM_ITERATIONS * 100:.1f}%")
    print()

    clear_users(instance_a)

if __name__ == "__main__":
    main()
