from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# load private key
with open("private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# read challenge
with open("challenge.txt", "rb") as f:
    data = f.read()

# sign
signature = private_key.sign(
    data,
    padding.PKCS1v15(),
    hashes.SHA256()
)

# save signature
with open("signature.bin", "wb") as f:
    f.write(signature)

print("Signature generated successfully")