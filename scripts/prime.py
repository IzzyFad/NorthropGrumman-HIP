import sys
input = int(sys.argv[1])
for number in range (2, input):
    prime = True
    for i in range (2, number):
        if (number%i==0):
            prime = False
    if prime:
        print (number)
