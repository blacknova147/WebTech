# Assignment 2: Count and graph English-letter frequencies.
import matplotlib.pyplot as plt


# Uppercase input makes letter counting and graph labels consistent.
text = input("Enter text: ").upper()

# Start with every English letter present, even if its count is zero.
frequency = {letter: 0 for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

# Count only A-Z so other alphabets, digits, and punctuation are ignored.
for character in text:
    if "A" <= character <= "Z":
        frequency[character] += 1

# Show letters from most frequent to least frequent.
print("\nLetter  Frequency")
for letter in sorted(frequency, key=frequency.get, reverse=True):
    print(letter, "     ", frequency[letter])

# Keep graph categories in alphabetic order for easy comparison.
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
counts = [frequency[letter] for letter in letters]

# Draw one bar for each letter and label the axes and chart.
plt.bar(letters, counts)
plt.xlabel("English letter")
plt.ylabel("Frequency")
plt.title("Letter Frequency Analysis")
plt.show()
