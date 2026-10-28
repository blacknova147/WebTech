# Assignment 1: Caesar cipher
# Each English letter moves forward by the key; other characters stay unchanged.


def caesar_cipher(message, shift):
    """Return message with English letters shifted by the given amount."""
    encrypted_message = ""
    shift = shift % 26  # Reduce large keys to one alphabet's worth of movement.

    for character in message:
        # Remember the start of the character's alphabet to preserve its case.
        if "A" <= character <= "Z":
            alphabet_start = ord("A")
        elif "a" <= character <= "z":
            alphabet_start = ord("a")
        else:
            encrypted_message += character  # Keep spaces, digits, and punctuation.
            continue

        # Convert the letter to 0-25, shift with wraparound, then convert it back.
        letter_number = ord(character) - alphabet_start
        shifted_number = (letter_number + shift) % 26
        encrypted_message += chr(shifted_number + alphabet_start)

    return encrypted_message


# Read the message and numeric shift from the user.
plaintext = input("Enter plaintext: ")
key = int(input("Enter key: "))

# A negative shift reverses the positive shift for decryption.
ciphertext = caesar_cipher(plaintext, key)
decrypted_text = caesar_cipher(ciphertext, -key)

print("Plaintext:      ", plaintext)
print("Ciphertext:     ", ciphertext)
print("Decrypted text: ", decrypted_text)
