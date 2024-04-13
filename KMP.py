"""
KMP search
"""

def BuildNext(patt):
    """
    Build the longest proper prefix which is also a suffix (lps) array for the pattern.
    """
    next = [0]
    prefix_len = 0 # Length of the previous longest prefix suffix
    i = 1
    while i < len(patt):
        if patt[prefix_len] == patt[i]:
            prefix_len += 1
            next.append(prefix_len)
            i += 1
        else:
            if prefix_len == 0:
                next.append(0)
                i += 1
            else:
                prefix_len = next[prefix_len - 1]
    return next

def KMPSearch(string, patt):
    """
    Search for occurrences of pattern in text using the Knuth-Morris-Pratt (KMP) algorithm.
    """
    next = BuildNext(patt)
    print(next)

    i = 0 # Index for text
    j = 0 # Index for pattern 
    while i < len(string):
        if string[i] == patt[j]:
            i += 1
            j += 1
        elif j > 0:
            j = next[j - 1]
        else:
            i += 1
        if j == len(patt):
            return i - j # Pattern found at index i - j
        
    return -1 # Pattern not found

def Test():
    # Example usage:
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    result = KMPSearch(text, pattern)
    if result != -1:
        print(f"Pattern found at index {result}")
    else:
        print("Pattern not found in the text")

if __name__ == "__main__":
    Test()