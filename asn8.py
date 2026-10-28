# Assignment 8: Practice prime numbers, GCD, modular inverses, and toy RSA.
import math
import time


def is_prime(number):
    """Return whether number has no divisors other than 1 and itself."""
    if number < 2:
        return False

    # A composite number must have a factor at most its square root.
    for divisor in range(2, math.isqrt(number) + 1):
        if number % divisor == 0:
            return False
    return True


def gcd(first, second):
    """Find the greatest common divisor using Euclid's remainder rule."""
    while second != 0:
        first, second = second, first % second
    return abs(first)


def are_coprime(first, second):
    """Two integers are coprime when their greatest common divisor is 1."""
    return gcd(first, second) == 1


def modular_inverse(number, modulus):
    """Find d such that number*d is 1 modulo modulus, if it exists."""
    if modulus <= 1 or not are_coprime(number, modulus):
        return None

    # Search is straightforward for this small teaching program.
    for candidate in range(1, modulus):
        if (number * candidate) % modulus == 1:
            return candidate
    return None


def run_rsa_demo():
    """Generate a small RSA key pair and encrypt/decrypt one integer."""
    first_prime = int(input("Enter first prime number (p): "))
    second_prime = int(input("Enter second prime number (q): "))

    # RSA's two primes must be prime and distinct.
    if (first_prime == second_prime
            or not is_prime(first_prime)
            or not is_prime(second_prime)):
        print("Enter two different prime numbers.")
        return

    # n is the modulus; phi counts values relatively prime to n for p, q prime.
    modulus_n = first_prime * second_prime
    phi_n = (first_prime - 1) * (second_prime - 1)
    print("n =", modulus_n)
    print("Phi(n) =", phi_n)

    # Choose the first exponent that is coprime with phi(n).
    public_exponent = 2
    while public_exponent < phi_n:
        if are_coprime(public_exponent, phi_n):
            break
        public_exponent += 1

    # The private exponent reverses the public exponent modulo phi(n).
    private_exponent = modular_inverse(public_exponent, phi_n)
    if private_exponent is None:
        print("Could not find a private exponent for these values.")
        return

    print("Public key:", (public_exponent, modulus_n))
    print("Private key:", (private_exponent, modulus_n))

    message = int(input("Enter plaintext message as an integer: "))
    if message < 0 or message >= modulus_n:
        print("Message must be between 0 and", modulus_n - 1)
        return

    # Modular exponentiation computes message^e mod n efficiently.
    start_time = time.perf_counter()
    ciphertext = pow(message, public_exponent, modulus_n)
    encryption_time = time.perf_counter() - start_time
    print("Encrypted message:", ciphertext)
    print("Encryption time:", encryption_time, "seconds")

    # Applying the private exponent recovers the original message.
    start_time = time.perf_counter()
    decrypted_message = pow(ciphertext, private_exponent, modulus_n)
    decryption_time = time.perf_counter() - start_time
    print("Decrypted message:", decrypted_message)
    print("Decryption time:", decryption_time, "seconds")


# Repeat the menu until the user chooses Exit.
while True:
    print("\nAssignment 8")
    print("1. Check prime")
    print("2. Find GCD")
    print("3. Check relatively prime")
    print("4. Find modular inverse")
    print("5. RSA encryption and decryption")
    print("6. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        number = int(input("Enter a number: "))
        print(number, "is prime" if is_prime(number) else "is not prime")
    elif choice == 2:
        first = int(input("Enter first number: "))
        second = int(input("Enter second number: "))
        print("GCD =", gcd(first, second))
    elif choice == 3:
        first = int(input("Enter first number: "))
        second = int(input("Enter second number: "))
        result = "are" if are_coprime(first, second) else "are not"
        print("Numbers", result, "relatively prime")
    elif choice == 4:
        number = int(input("Enter number: "))
        modulus = int(input("Enter modulus: "))
        inverse = modular_inverse(number, modulus)
        if inverse is None:
            print("Multiplicative inverse does not exist")
        else:
            print("Multiplicative inverse =", inverse)
    elif choice == 5:
        run_rsa_demo()
    elif choice == 6:
        break
    else:
        print("Invalid choice")

# Small RSA numbers here are for learning; production RSA needs secure libraries.
