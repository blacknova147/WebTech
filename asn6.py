# Assignment 6: Simplified DES (S-DES), an educational 8-bit block cipher.
import time


# Fixed S-DES lookup tables specify bit positions and substitution values.
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INVERSE = [4, 1, 3, 5, 7, 2, 8, 6]
EXPANSION_PERMUTATION = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]

# Each S-box maps a 4-bit input to a 2-bit output.
S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2],
]
S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3],
]


def permute(bits, table):
    """Reorder bits using a table whose positions start at 1."""
    return "".join(bits[position - 1] for position in table)


def circular_left_shift(bits, amount):
    """Rotate a bit string left, moving its first bits to the end."""
    return bits[amount:] + bits[:amount]


def generate_keys(key):
    """Create the two 8-bit round keys from a 10-bit input key."""
    permuted_key = permute(key, P10)
    left_half = circular_left_shift(permuted_key[:5], 1)
    right_half = circular_left_shift(permuted_key[5:], 1)
    first_key = permute(left_half + right_half, P8)

    # S-DES shifts each half two additional places before making round key 2.
    left_half = circular_left_shift(left_half, 2)
    right_half = circular_left_shift(right_half, 2)
    second_key = permute(left_half + right_half, P8)
    return first_key, second_key


def substitute(bits, box):
    """Look up a 4-bit value; outside bits select row, inside bits select column."""
    row = int(bits[0] + bits[3], 2)
    column = int(bits[1] + bits[2], 2)
    return format(box[row][column], "02b")


def round_function(bits, round_key):
    """Apply one Feistel round: expand, mix, substitute, permute, and XOR."""
    left_half = bits[:4]
    right_half = bits[4:]

    # Expand the right half to eight bits, then XOR it with this round's key.
    expanded = permute(right_half, EXPANSION_PERMUTATION)
    mixed = "".join(
        str(int(expanded[index]) ^ int(round_key[index]))
        for index in range(8)
    )

    # The two S-boxes each turn four bits into two; P4 reorders the result.
    substituted = substitute(mixed[:4], S0) + substitute(mixed[4:], S1)
    permuted = permute(substituted, P4)

    # XOR the four-bit result with the left half and keep the right half.
    new_left = "".join(
        str(int(left_half[index]) ^ int(permuted[index]))
        for index in range(4)
    )
    return new_left + right_half


def encrypt_block(block, first_key, second_key):
    """Encrypt exactly one 8-bit block using round keys in forward order."""
    block = permute(block, IP)
    block = round_function(block, first_key)
    block = block[4:] + block[:4]  # Swap halves between the two rounds.
    block = round_function(block, second_key)
    return permute(block, IP_INVERSE)


def decrypt_block(block, first_key, second_key):
    """Decrypt one block by applying the same rounds with keys reversed."""
    block = permute(block, IP)
    block = round_function(block, second_key)
    block = block[4:] + block[:4]
    block = round_function(block, first_key)
    return permute(block, IP_INVERSE)


# S-DES expects one 10-bit binary key.
key = input("Enter 10-bit key: ")
if len(key) != 10 or any(bit not in "01" for bit in key):
    raise SystemExit("The key must contain exactly 10 binary digits.")

first_key, second_key = generate_keys(key)
print("\nRound key 1 =", first_key)
print("Round key 2 =", second_key)

# This text demonstration maps each character to one byte (0-255).
message = input("\nEnter message (ASCII/byte characters only): ")
if any(ord(character) > 255 for character in message):
    raise SystemExit("Use only characters whose code point is between 0 and 255.")

# Encode the text as a continuous string of 8-bit blocks.
binary_message = "".join(format(ord(character), "08b") for character in message)

# Encrypt every byte and measure only the encryption operation.
start_time = time.perf_counter()
ciphertext = ""
for position in range(0, len(binary_message), 8):
    ciphertext += encrypt_block(binary_message[position:position + 8],
                                first_key, second_key)
encryption_time = time.perf_counter() - start_time

# Decrypt each encrypted byte, using the round keys in reverse order.
start_time = time.perf_counter()
decrypted_binary = ""
for position in range(0, len(ciphertext), 8):
    decrypted_binary += decrypt_block(ciphertext[position:position + 8],
                                      first_key, second_key)
decryption_time = time.perf_counter() - start_time

# Convert each recovered 8-bit block back into its original character.
decrypted_message = ""
for position in range(0, len(decrypted_binary), 8):
    byte = decrypted_binary[position:position + 8]
    decrypted_message += chr(int(byte, 2))

print("\nEncrypted binary:")
print(ciphertext)
print("\nDecrypted message:")
print(decrypted_message)
print("\nTime required:")
print("Encryption:", encryption_time, "seconds")
print("Decryption:", decryption_time, "seconds")

# S-DES is intentionally small for learning; it is not secure for real data.
