from pathlib import Path
import base64
import requests

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


SERVER_URL = "http://127.0.0.1:8000"
DEVICE_ID = "sandhya1234"

BASE_DIR = Path(__file__).resolve().parent.parent

PRIVATE_KEY_FILE = BASE_DIR / "keys" / "private.pem"


def load_private_key():

    with open(PRIVATE_KEY_FILE, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def request_challenge():

    response = requests.post(
        f"{SERVER_URL}/auth/request",
        json={
            "device_id": DEVICE_ID
        }
    )

    response.raise_for_status()

    return response.json()["challenge"]


def sign_challenge(challenge):

    private_key = load_private_key()

    signature = private_key.sign(
        challenge.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    return base64.b64encode(signature).decode()


def verify_authentication(signature_b64):

    response = requests.post(
        f"{SERVER_URL}/auth/verify",
        json={
            "device_id": DEVICE_ID,
            "signature": signature_b64
        }
    )

    return response


def main():

    print("\n[1] Requesting challenge...")

    challenge = request_challenge()

    print("[✓] Challenge received")
    print("Challenge:", challenge)

    print("\n[2] Signing challenge...")

    signature = sign_challenge(challenge)

    # TEST: Corrupt signature
    #signature = signature[:-5] + "ABCDE"

    print("[✓] Signature generated")

    print("\n[3] Verifying authentication...")

    response = verify_authentication(signature)

    result = response.json()

    print("\n========================")
    print("Authentication Result")
    print("========================")
   
    print(f"Device ID : {DEVICE_ID}")

    if result.get("authenticated"):

        print("Challenge : Verified")
        print("Signature : Valid")
        print("\n✅ RESULT : AUTHENTICATED")


    else:

        print("Challenge : Verification Failed")
        print("Signature : Invalid")

        print("\n❌ RESULT : NOT AUTHENTICATED")

        if "error" in result:
            print("Reason:", result["error"])

print("================================")


if __name__ == "__main__":
    main()