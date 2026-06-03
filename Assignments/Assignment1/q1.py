marks = []
tot, min, max = 0, 101, 0
i = 1
while i<=10:
    mark = int(input("Enter marks of student " + str(i) + ": "))
    marks.append(mark)
    i += 1
    tot+=mark
    if max < mark:
        max = mark
    if min > mark:
        min = mark

avg = tot/(i-1)
abv_avg = 0
for mark in marks:
    if mark > avg:
        abv_avg += 1

grades = {"A": 0, "B": 0, "C": 0, "D": 0}
for mark in marks:
    if mark >= 90:
        grades["A"] += 1
    elif mark >= 75:
        grades["B"] += 1
    elif mark >= 60:
        grades["C"] += 1
    else:
        grades["D"] += 1

print("Total marks =",tot)
print("Highest marks =", max)
print("Lowest marks =", min)
print("Average marks =", avg)
print("Students scoring above average =", abv_avg)
print("Grade distribution =", grades)