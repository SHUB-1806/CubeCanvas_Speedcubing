sent = input("Enter sentence: ")
char = 0
for ch in sent:
    char+=1

word = 0
prev = ' '
for curr in sent:
    if curr != ' ' and prev == ' ':
        word+=1
    prev = curr

vowels = 0
for ch in sent:
    if ch.lower() in "aeiou":
        vowels+= 1

freq = {}
max_freq = 0
for ch in sent:
    if ch in freq:
        freq[ch] += 1
    else:
        freq[ch] = 1

    if freq[ch] > max_freq:
        max_freq = freq[ch]
        max_char = ch


print("Total Characters:", char)
print("Total Words:", word)
print("Total Vowels:", vowels)
print("\nCharacter Frequencies:")
for ch in freq:
    print(ch, ":", freq[ch])
print("\nMost Frequent Character:", max_char)