# Write a function is_even(n) that returns True/False

def is_even(n): # Define the function is_even that takes one argument n
    return n % 2 == 0
# depending on whether the number is even or odd.
# Then write another function that uses is_even to print out all the even numbers from 1 to 20.
for i in range(1, 21):
    if is_even(i):
        print(i)