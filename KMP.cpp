#include <iostream>
#include <vector>
#include <string>

using namespace std;

vector<int> BuildNext(const string& pattern) 
{
    int prefix_len = 0; // Length of the previous longest prefix suffix
    vector<int> next(pattern.size(), 0);
    int i = 1;
    
    while (i < pattern.size()) {
        if (pattern[i] == pattern[prefix_len]) 
        {
            prefix_len++;
            next[i] = prefix_len;
            i++;
        } 
        else 
        {
            if (prefix_len != 0) prefix_len = next[prefix_len - 1];
            else 
            {
                next[i] = 0;
                i++;
            }
        }
    }
    return next;
}

int KMPSearch(const string& text, const string& pattern) {
    vector<int>*next = new vector<int>(BuildNext(pattern));
    int i = 0; // Index for text
    int j = 0; // Index for pattern
    
    while (i < text.size()) {
        if (pattern[j] == text[i]) {
            i++;
            j++;
            
            if (j == pattern.size()) 
            {
                delete next;
                return i - j; // Pattern found at index i - j
            }
        } else {
            if (j != 0) {
                j = (*next)[j - 1];
            } else {
                i++;
            }
        }
    }
    delete next;
    return -1; // Pattern not found
}

int main() {
    string text = "ABABDABACDABABCABAB";
    string pattern = "ABABCABAB";
    int result = KMPSearch(text, pattern);
    if (result != -1) {
        cout << "Pattern found at index " << result << endl;
    } else {
        cout << "Pattern not found in the text" << endl;
    }
    system("pause");
    return 0;
}
