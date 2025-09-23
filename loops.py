#Print numbers 1–20, but say “Fizz” for multiples of 3 and “Buzz” for multiples of 5.

for i in range(1, 21):
    if i % 3 == 0 and i % 5 == 0: # Check if the number is a multiple of both 3 and 5
        print("FizzBuzz")
    elif i % 3 == 0: # Check if the number is a multiple of 3
        print("Fizz") # Then print "Fizz"
    elif i % 5 == 0: # Check if the number is a multiple of 5
        print("Buzz") # Then print "Buzz"
    else:
        print(i) # If the number is not a multiple of 3 or 5, print the number itself