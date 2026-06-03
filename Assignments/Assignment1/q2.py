colors = ["W", "Y", "R", "O", "B", "G"]
face = [ ["R", "R", "G"], ["R", "W", "G"], ["B", "B", "Y"] ]

for a in face:
    for b in a:
        if b in colors:
            print(b, end = " ")
        else:
            print("(Invalid)", end = " ")
    print(" ")

freq = {}
for a in face:
    for b in a:
        if b in freq:
            freq[b] += 1
        else:
            freq[b] = 1

print("\nColor Frequencies:")
for color in freq:
    print(color, ":", freq[color])

print(" ")
for a in face:
    for b in a:
        if b in colors:
            if b == "R":
                b = "X"
            print(b, end = " ")
        else:
            print("(Invalid)", end = " ")
    print(" ")

most_common = ""
max_count = 0

for color in freq:
    if freq[color] > max_count:
        max_count = freq[color]
        most_common = color

print("\nMost common color:", most_common)

identical_row = False

for a in face:
    if a[0] == a[1] == a[2]:
        identical_row = True

if identical_row:
    print("\nA row contains all identical colors.")
else:
    print("\nNo row contains all identical colors.")