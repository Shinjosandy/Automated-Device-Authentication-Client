# TPM-Ready Challenge-Response Authentication Framework

## Part 2: Automated Device Authentication Client

---

## Overview

Part 2 extends the challenge-response authentication framework developed in Part 1 by automating the entire device authentication process.

The objective of this phase was to eliminate manual operations such as key generation, device registration through Postman, challenge handling, signature generation using OpenSSL commands, and manual verification.

The resulting system provides an automated client capable of interacting directly with the authentication server and performing end-to-end device authentication.

---

## Objectives

* Automate RSA key provisioning
* Automate device registration
* Automate challenge retrieval
* Automate digital signature generation
* Automate authentication verification
* Remove dependency on manual Postman requests
* Prepare the framework for TPM integration

---

## Features

### Automated Key Provisioning

* Generates RSA key pair automatically
* Creates:

  * `private.pem`
  * `public.pem`
* Detects existing keys and avoids regeneration

### Automated Device Registration

* Reads the generated public key
* Registers the device automatically with the server
* Eliminates manual public key copy-paste operations

### Automated Challenge Retrieval

* Requests challenge directly from the server
* Receives nonce automatically
* Removes dependency on challenge text files

### Automated Signature Generation

* Loads private key automatically
* Signs challenge programmatically
* Converts signature to Base64 internally

### Automated Authentication Verification

* Sends generated signature to the server
* Receives authentication result automatically

### Authentication Reporting

* Displays clear authentication status
* Supports both successful and failed authentication scenarios

---

## Project Structure

```text
TPM-Challenge-Automaion/

├── app.py
├── config.py
├── models.py

├── routes/
│   ├── register.py
│   └── auth.py

├── crypto/
│   ├── challenge.py
│   └── verify.py

├── device/
│   ├── provision.py
│   ├── register_device.py
│   └── authenticate.py

├── keys/
│   ├── private.pem
│   └── public.pem

└── instance/
    └── tpm_auth.db
```

---

## Authentication Workflow

```text
Device Startup
      │
      ▼
Check Keys
      │
      ▼
Generate Keys (if needed)
      │
      ▼
Register Device
      │
      ▼
Request Challenge
      │
      ▼
Receive Nonce
      │
      ▼
Sign Challenge
      │
      ▼
Send Signature
      │
      ▼
Verify Signature
      │
      ▼
Authentication Result
```

---

## How to Run the Project

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd TPM-Challenge-Automaion
```

---

### Step 2: Create Virtual Environment

```powershell
py -m venv venv
```

---

### Step 3: Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks execution:

```powershell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\venv\Scripts\Activate.ps1)
```

---

### Step 4: Install Dependencies

```powershell
venv\Scripts\python.exe -m pip install flask
venv\Scripts\python.exe -m pip install flask-sqlalchemy
venv\Scripts\python.exe -m pip install cryptography
venv\Scripts\python.exe -m pip install requests
```

Alternatively:

```powershell
venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

### Step 5: Start Authentication Server

Open Terminal 1:

```powershell
venv\Scripts\python.exe -m flask run --host=0.0.0.0 --port=8000
```

Expected Output:

```text
* Running on http://127.0.0.1:8000
```

Keep this terminal running.

---

### Step 6: Generate Device Keys

Open Terminal 2:

```powershell
venv\Scripts\python.exe device\provision.py
```

Expected Output:

```text
[*] Generating RSA key pair...
[✓] Keys generated successfully
```

Generated Files:

```text
keys/private.pem
keys/public.pem
```

---

### Step 7: Register Device

```powershell
venv\Scripts\python.exe device\register_device.py
```

Expected Output:

```text
Status Code: 201
Response: {'message': 'Device registered successfully'}
```

---

### Step 8: Authenticate Device

```powershell
venv\Scripts\python.exe device\authenticate.py
```

Expected Output:

```text
================================
      AUTHENTICATION REPORT
================================

Device ID : sandhya1234
Challenge : Verified
Signature : Valid

RESULT : AUTHENTICATED

================================
```

---

## Complete Execution Flow

```text
Start Server
      ↓
Generate Keys
      ↓
Register Device
      ↓
Authenticate Device
      ↓
AUTHENTICATED
```

---

## Test Authentication Failure

To verify signature validation:

Open:

```text
device/authenticate.py
```

Temporarily modify:

```python
signature = sign_challenge(challenge)
signature = signature[:-5] + "ABCDE"
```

Run:

```powershell
venv\Scripts\python.exe device\authenticate.py
```

Expected Output:

```text
RESULT : NOT AUTHENTICATED
```

This confirms that the server correctly rejects invalid signatures.

---

## Components

### provision.py

Responsible for:

* RSA key generation
* Key storage
* Device provisioning

Output:

```text
keys/private.pem
keys/public.pem
```

Run:

```powershell
venv\Scripts\python.exe device\provision.py
```

---

### register_device.py

Responsible for:

* Reading public key
* Registering device with server

Configured Device:

```text
sandhya1234
```

Run:

```powershell
venv\Scripts\python.exe device\register_device.py
```

Example Response:

```json
{
    "message": "Device registered successfully"
}
```

---

### authenticate.py

Responsible for:

* Requesting challenge
* Signing challenge
* Sending signature
* Receiving authentication result

Run:

```powershell
venv\Scripts\python.exe device\authenticate.py
```

---

## Server APIs Used

### Register Device

```http
POST /register
```

---

### Request Challenge

```http
POST /auth/request
```

Request:

```json
{
    "device_id": "sandhya1234"
}
```

Response:

```json
{
    "device_id": "sandhya1234",
    "challenge": "..."
}
```

---

### Verify Authentication

```http
POST /auth/verify
```

Request:

```json
{
    "device_id": "sandhya1234",
    "signature": "<Base64 Signature>"
}
```

Response:

```json
{
    "authenticated": true
}
```

---

## Example Authentication Report

### Successful Authentication

```text
================================
      AUTHENTICATION REPORT
================================

Device ID : sandhya1234
Challenge : Verified
Signature : Valid

RESULT : AUTHENTICATED

================================
```

---

### Failed Authentication

```text
================================
      AUTHENTICATION REPORT
================================

Device ID : sandhya1234
Challenge : Verification Failed
Signature : Invalid

RESULT : NOT AUTHENTICATED

================================
```

---

## Security Features

* Public Key Cryptography
* Challenge-Response Authentication
* Replay Attack Protection
* Server-Side Signature Verification
* Private Key Isolation
* Automated Verification Workflow

---

## Improvements Over Part 1

### Part 1 (Manual)

```text
Generate Keys
     ↓
Copy Public Key
     ↓
Open Postman
     ↓
Register Device
     ↓
Request Challenge
     ↓
Save Challenge
     ↓
Sign Challenge
     ↓
Convert Signature
     ↓
Verify Authentication
```

### Part 2 (Automated)

```text
Run Client
     ↓
Generate Keys
     ↓
Register Device
     ↓
Request Challenge
     ↓
Sign Challenge
     ↓
Verify Authentication
```

---

## Current Status

### Completed

✅ Automatic RSA Key Provisioning

✅ Automatic Device Registration

✅ Automatic Challenge Retrieval

✅ Automatic Signature Generation

✅ Automatic Authentication Verification

✅ Authentication Reporting

---

## Future Work

### Part 3 – TPM Integration

Planned Enhancements:

* TPM-Protected Private Keys
* TPM-Based Signing Operations
* Hardware-Backed Authentication
* Device Trust Establishment

### Part 4 – TPM Remote Attestation

Planned Enhancements:

* Endorsement Key (EK)
* Attestation Identity Key (AIK)
* TPM Quote Verification
* PCR Validation
* Platform Integrity Verification

---

## Conclusion

Part 2 successfully transformed the manual challenge-response authentication framework into a fully automated device authentication client. The system now performs key provisioning, registration, challenge retrieval, signature generation, and authentication verification without manual intervention.

The architecture is now ready for the next phase involving TPM-backed key storage and signing operations while maintaining compatibility with virtual machine deployment environments.
