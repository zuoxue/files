import requests
import re
import string

def ngrams(text,n):
    text = text.replace(string.punctuation," ").replace("\n+"," ")
    inp = text.lower().split(" ")
    arr = {}
    for i in range(len(inp)-n+1):
        mm = inp[i:i+n]
        splitC = " ".join(mm).lower()
        if splitC in text.lower():
            arr[splitC] = 0
            continue
        arr[splitC] += 1

    print(arr)

if __name__ == "__main__":
    url = "http://pythonscraping.com/files/inaugurationSpeech.txt"
    text = requests.get(url).text
    ngrams(text,2)
