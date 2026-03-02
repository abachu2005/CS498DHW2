# CS498D Assignment 2 — Cloud Computing Basics

## Prerequisites

- A GCP project with billing enabled
- `gcloud` CLI installed and authenticated

---

## Part I & II: Node.js Server with Firestore

### 1. Enable Firestore in Datastore Mode

1. Go to **GCP Console → Firestore → Create Database**
2. Select **Datastore mode** (NOT Native mode)
3. Region: **us-central1**

### 2. Create Compute Engine Instances

#### Instance A (us-central1)

```bash
gcloud compute instances create instance-a \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --tags=http-server-8080 \
  --scopes=cloud-platform
```

#### Instance B (europe-west1)

```bash
gcloud compute instances create instance-b \
  --zone=europe-west1-b \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --tags=http-server-8080 \
  --scopes=cloud-platform
```

### 3. Open Firewall for Port 8080

```bash
gcloud compute firewall-rules create allow-8080 \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:8080 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=http-server-8080
```

### 4. Grant Datastore Access

```bash
SA_EMAIL=$(gcloud iam service-accounts list --filter="displayName:Compute Engine" --format="value(email)")
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/datastore.user"
```

### 5. Deploy the Server on Each Instance

Upload the server code:

```bash
gcloud compute scp --recurse server/ instance-a:~/server --zone=us-central1-a
gcloud compute scp --recurse server/ instance-b:~/server --zone=europe-west1-b
```

SSH into each instance and install Node 18 + dependencies:

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
cd ~/server && npm install
nohup node index.js > server.log 2>&1 &
```

### 6. Verify Endpoints

```bash
curl http://<EXTERNAL_IP>:8080/greeting
curl -X POST http://<EXTERNAL_IP>:8080/register -H "Content-Type: application/json" -d '{"username":"TestUser"}'
curl http://<EXTERNAL_IP>:8080/list
curl -X POST http://<EXTERNAL_IP>:8080/clear
```

---

## Part IV: Performance and Consistency Analysis

### Setup

```bash
cd client
pip install -r requirements.txt
```

### A. Latency Measurement

```bash
python latency_test.py http://<IP_A>:8080 http://<IP_B>:8080
```

### B. Eventual Consistency Test

```bash
python eventual_consistency_test.py http://<IP_A>:8080 http://<IP_B>:8080
```

---

## Submission Files

| File | Description |
|------|-------------|
| `Team_HW2.txt` | Your netID |
| `IPs.txt` | Space-separated external IPs of both instances |
| `Code_HW2.txt` | Description of Part IV script implementation |
| `Analysis.txt` | Latency results, consistency results, and discussion |
