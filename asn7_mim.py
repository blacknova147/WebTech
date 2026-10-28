# Assignment 7 companion: simulate a Diffie-Hellman man-in-the-middle attack.
# This offline toy example demonstrates why public keys need authentication.
prime = 23
generator = 5

# Alice, Bob, and the attacker Eve select private values for this demo.
alice_private = 6
bob_private = 15
eve_private = 7

# Calculate the public values that each participant would normally share.
alice_public = pow(generator, alice_private, prime)
bob_public = pow(generator, bob_private, prime)
eve_public = pow(generator, eve_private, prime)
print("Alice's public key:", alice_public)
print("Bob's public key:", bob_public)
print("Eve's public key:", eve_public)

# In this simulation Eve replaces both exchanged public values with her own.
print("\nEve sends", eve_public, "to Alice and Bob")

# Alice and Bob unknowingly establish separate keys with Eve.
alice_key = pow(eve_public, alice_private, prime)
bob_key = pow(eve_public, bob_private, prime)

# Eve derives each matching key using her private value and the real public key.
eve_alice_key = pow(alice_public, eve_private, prime)
eve_bob_key = pow(bob_public, eve_private, prime)

print("\nAlice's key:", alice_key)
print("Eve's key with Alice:", eve_alice_key)
print("\nBob's key:", bob_key)
print("Eve's key with Bob:", eve_bob_key)

# Matching pairs show that Eve can sit between both parties in this model.
# Real protocols prevent this by authenticating the exchanged public keys.
