# Assignment 3: Try every Caesar key and rank likely English results.

# English letters ordered approximately from most to least common.
english_frequency_order = "etaoinshrdlucmfwypvbgkjqxz"
ciphertext = input("Enter ciphertext: ")

best_key = 0
best_plaintext = ""
best_score = -1

# A Caesar cipher has only 26 possible shifts, so try them all.
for key in range(26):
    candidate = ""

    # Undo this key while preserving letter case and non-letter characters.
    for character in ciphertext:
        if "A" <= character <= "Z":
            candidate += chr((ord(character) - ord("A") - key) % 26 + ord("A"))
        elif "a" <= character <= "z":
            candidate += chr((ord(character) - ord("a") - key) % 26 + ord("a"))
        else:
            candidate += character

    # Count English letters in this candidate; punctuation is not evidence.
    counts = {}
    for character in candidate.lower():
        if "a" <= character <= "z":
            counts[character] = counts.get(character, 0) + 1

    # Common letters earn more points, making likely English score higher.
    score = 0
    for position, letter in enumerate(english_frequency_order):
        score += counts.get(letter, 0) * (26 - position)

    print("Key:", key, "| Text:", candidate, "| Score:", score)

    # Save the highest-scoring candidate seen so far.
    if score > best_score:
        best_score = score
        best_key = key
        best_plaintext = candidate

print("\nMost promising result:")
print("Key:", best_key)
print("Plaintext:", best_plaintext)

# Frequency scoring is a heuristic; it may be unreliable for very short text.
