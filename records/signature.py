import hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

# Generate ECDSA keys (one-time or stored securely)
def generate_ecdsa_keys():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()

    # Serialize private key for storage
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key for storage
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return pem_private, pem_public

# Sign the file with ECDSA
def sign_file(private_key_pem, file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Generate the hash of the file
    file_hash = hashlib.sha256(file_data).digest()

    # Load private key
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)

    # Sign the file hash using ECDSA
    signature = private_key.sign(file_hash, ec.ECDSA(hashes.SHA256()))

    return signature

# Verify the signature
def verify_signature(public_key_pem, file_path, signature):
    with open(file_path, 'rb') as f:
        file_data = f.read()

    file_hash = hashlib.sha256(file_data).digest()

    # Load public key
    public_key = serialization.load_pem_public_key(public_key_pem)

    try:
        # Verify the signature
        public_key.verify(signature, file_hash, ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False
