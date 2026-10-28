# Assignment 5: Solve congruences with the Chinese Remainder Theorem.
from math import gcd


number_of_congruences = int(input("Enter number of congruences: "))
if number_of_congruences <= 0:
    raise SystemExit("Enter at least one congruence.")

remainders = []
moduli = []

# Read each equation in the form x = remainder (mod modulus).
for index in range(number_of_congruences):
    print("\nCongruence", index + 1, ": x = a (mod c)")
    remainders.append(int(input("Enter a (remainder): ")))
    moduli.append(int(input("Enter c (modulus): ")))

# The basic CRT formula requires positive, pairwise-coprime moduli.
if any(modulus <= 1 for modulus in moduli):
    raise SystemExit("Every modulus must be greater than 1.")

for first in range(number_of_congruences):
    for second in range(first + 1, number_of_congruences):
        if gcd(moduli[first], moduli[second]) != 1:
            raise SystemExit("The moduli must be pairwise coprime.")

print("\nGiven congruences:")
for remainder, modulus in zip(remainders, moduli):
    print("x =", remainder, "(mod", modulus, ")")

# M is the product of all moduli and is the period of the combined solution.
total_modulus = 1
for modulus in moduli:
    total_modulus *= modulus
print("\nM =", total_modulus)

# For each equation, build its CRT contribution.
solution_sum = 0
print("\ni\ta_i\tM_i\tb_i\tContribution")
print("-" * 42)

for index, (remainder, modulus) in enumerate(zip(remainders, moduli)):
    partial_modulus = total_modulus // modulus
    inverse = pow(partial_modulus, -1, modulus)
    contribution = remainder * partial_modulus * inverse
    solution_sum += contribution
    print(index + 1, "\t", remainder, "\t", partial_modulus, "\t",
          inverse, "\t", contribution)

# Every contribution satisfies one equation; reducing gives the least solution.
solution = solution_sum % total_modulus
print("\nSum of contributions =", solution_sum)
print("Final answer: x =", solution)
