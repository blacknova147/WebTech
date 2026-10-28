# Assignment 7: Demonstrate the Diffie-Hellman key exchange.
# These small public parameters are for learning, not for real security.
prime = 23
generator = 5

# Alice and Bob each choose a private number that they keep secret.
alice_private = int(input("Enter Alice's private key: "))
bob_private = int(input("Enter Bob's private key: "))

# Public values are powers of the generator, reduced modulo the prime.
alice_public = pow(generator, alice_private, prime)
bob_public = pow(generator, bob_private, prime)
print("Alice's public key:", alice_public)
print("Bob's public key:", bob_public)

# Each person combines their private value with the other person's public one.
alice_shared = pow(bob_public, alice_private, prime)
bob_shared = pow(alice_public, bob_private, prime)
print("Alice's shared key:", alice_shared)
print("Bob's shared key:", bob_shared)

# Both results match because (g^b)^a and (g^a)^b equal g^(a*b) modulo p.
if alice_shared == bob_shared:
    print("Key exchange successful!")
else:
    print("The shared keys do not match.")
