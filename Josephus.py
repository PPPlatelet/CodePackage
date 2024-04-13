import math

"""
Josephus's Question
"""

def Josephus(num):
    # Count the number of bits in num
    count = 0
    temp = num
    while temp:
        temp >>= 1
        count += 1
    # Create a mask to XOR with num
    mask = 1 << (count-1)
    # Perform XOR operation to get the result
    return num ^ mask

def Josephusmath(num):
    # Calculate the power of 2 closest to num
    power = int(math.log2(num))
    # Calculate the remainder
    remainder = num - (1 << power)
    # Return the remainder
    return remainder

def Josephus2(num):
    # Count the number of bits in num
    count = 0
    temp = num
    while temp:
        temp >>= 1
        count += 1
    # Create a mask to AND with num
    mask = (1 << (count - 1)) - 1
    # Perform AND operation to get the result
    return num & mask

#Test code
def main():
    num = int(input("Enter a number: "))
    result = Josephus(num)
    #result = Josephusmath(num)
    #result = Josephus2(num)
    print(f"Result of Josephus: {result}")
    print(f"Result of correct position: {result * 2 + 1}")

if __name__ == "__main__":
    main()