def getprimes(number: int) -> list[int]:
    cnt = 0
    if number <= 1:
        return []
    
    isprime = [True] * (number + 1)
    isprime[1] = False
    primes = [0] * (number + 1)
    for i in range(2, number + 1, 1):
        if isprime[i]:
            cnt += 1
            primes[cnt] = i
        
        j = 1
        prime = primes[j]
        while j <= cnt and i * prime <= number:
            isprime[i * prime] = False
            if i % prime == 0:
                break
            j += 1
            prime = primes[j]

    return primes[1:cnt + 1]

def main():
    number = int(input())
    primes: list[int] = getprimes(number)

    for prime in primes:
        print(prime, end = " ")

if __name__ == '__main__':
    main()