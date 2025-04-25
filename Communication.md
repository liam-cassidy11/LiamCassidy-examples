

Steps of what we should focus on:
1. Communication
2. Device pairing
3. Secure communication

1. Communication
    AWS server- used as a relay for device communication
        Nothing important actually stored on the server
        Zero Trust on the Server:
        Since the decryption keys are never transmitted or stored on AWS, the server cannot decrypt or manipulate the data. AWS only relays the encrypted data between devices.


2. Device Pairing
    NTFY- allows devices to communicate with each other
        Lets a device know that another device is trying to communicate with it
        Need to set up an EC2 instance of AWS server 
        Install Docker to the server (needed for nfty)
        Install nfty as a docker container


3. Secure Communication
    Diffie hellman key exchange with elliptic curve setup
        Details below on how DH works/how we can use it
        We should first find a simple diffie hellman implementation
        In addition to diffie hellman we need a specified way of authentication using keys from DH

    Device Key Pair Setup:
        Generate Public-Private Keys: Each device generates its own asymmetric key pair (for example, using the X25519 algorithm). https://x25519.xargs.org/

    Exchange Public Keys: 
        Devices exchange their public keys via a secure, out-of-band method (QR code scanning, manual configuration, etc.). These public keys are stored on each device, ensuring they can later encrypt messages intended for a specific recipient.

    Data Encryption Before Transmission (using End-to-End Encryption (E2EE)) :
        Devices encrypt the partial keys (or any sensitive data) using their respective encryption keys before sending them to AWS. This means that even if the AWS server is compromised, attackers only access ciphertext.

    Secure Key Exchange:
        Using protocols like X25519 for Diffie-Hellman key exchange, devices can derive a shared secret to encrypt and decrypt messages. This process ensures that only the intended recipient, who has the correct private key, can access the decrypted data.

    Mutual TLS for Transport Security:
        Although E2EE already secures the content, using TLS (and even mutual TLS) adds an extra layer by ensuring the communication channel itself is secure, preventing man-in-the-middle attacks during transmission.

    Integrity and Authentication:
        With the use of authenticated encryption (such as AES-GCM), devices ensure that any tampering with the encrypted data is detected. This protects against unauthorized modifications while the data is in transit via AWS.
        Authentication must be post-quantum
        

DIFFIE HELLMAN
    X25519 is a key-agreement algorithm based on elliptic curve Diffie-Hellman (ECDH) using Curve25519. Here's a breakdown:
        Elliptic Curve Diffie-Hellman (ECDH):
            Allows two parties to securely compute a shared secret over an insecure channel.
            Each party has a private key and a corresponding public key. By combining their private key with the other party's public key, both derive the same shared secret.
        Curve25519:
            This is a specific elliptic curve that is designed for high performance and robust security.
            It offers fast computations and strong resistance against side-channel attacks.
        X25519 Specification:
            X25519 is essentially an implementation of the ECDH function on Curve25519. It focuses on the x-coordinate of the elliptic curve point, which simplifies the computation and enhances security. It is defined in RFC 7748.
        Security and Efficiency:
            The algorithm is favored in modern cryptographic protocols (such as TLS 1.3 and SSH) because of its efficiency and security properties. It minimizes the risk of exposing private key data even if parts of the system are compromised.
