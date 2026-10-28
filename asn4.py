# Assignment 4: Brute-force two columnar transposition keys.
from itertools import permutations


def decrypt_transposition(ciphertext, key):
    """Undo one columnar transposition for text with complete rows."""
    column_count = len(key)
    row_count = len(ciphertext) // column_count

    # Columns were read in increasing key-number order during encryption.
    column_order = sorted(range(column_count), key=lambda index: key[index])
    columns = [""] * column_count
    position = 0

    # Split the ciphertext back into columns using the original read order.
    for column in column_order:
        columns[column] = ciphertext[position:position + row_count]
        position += row_count

    # Read across the reconstructed grid to recover the pre-encrypted text.
    plaintext = ""
    for row in range(row_count):
        for column in range(column_count):
            plaintext += columns[column][row]

    return plaintext


# A small dictionary gives candidate plaintexts points for recognizable words.
common_words = [
    "THE", "THIS", "THAT", "IS", "OF", "TO", "IN", "AND", "FOR",
    "WITH", "ON", "AS", "ENGINEERING", "MINUTES", "FIVE", "MESSAGE",
    "TEXT", "DATA", "SECURITY",
]


def english_score(text):
    """Give more points when known English words occur in the text."""
    total = 0
    for word in common_words:
        if word in text:
            total += len(word)
    return total


# Spaces are removed because this demonstration expects a compact grid.
ciphertext = input("Enter ciphertext: ").replace(" ", "").upper()
key_length = int(input("Enter key length: "))

# This version uses a rectangle with complete rows and distinct key positions.
if key_length <= 0 or len(ciphertext) % key_length != 0:
    raise SystemExit("Key length must be positive and divide ciphertext length.")

# Each permutation represents one possible ordering of the column labels.
possible_keys = list(permutations(range(key_length)))
best_score = -1
best_plaintext = ""
best_first_key = ()
best_second_key = ()
combinations_tried = 0

print("\nCryptanalysis started...\n")

# Try every pair because the example applies two transpositions in succession.
for first_key in possible_keys:
    intermediate_text = decrypt_transposition(ciphertext, first_key)

    for second_key in possible_keys:
        candidate = decrypt_transposition(intermediate_text, second_key)
        score = english_score(candidate)
        combinations_tried += 1

        # Keep the candidate with the strongest dictionary-word score.
        if score > best_score:
            best_score = score
            best_plaintext = candidate
            best_first_key = first_key
            best_second_key = second_key

print("Total combinations tried:", combinations_tried)
print("\nBest possible plaintext:")
print(best_plaintext)
print("\nKey 1:", best_first_key)
print("Key 2:", best_second_key)
print("English score:", best_score)

# This is a teaching heuristic, not a guarantee that the best score is correct.
