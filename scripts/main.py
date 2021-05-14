

choice = input("Which Tool Would You Like To Use Today?:\n1. Cross Reference Stepper\n2. Cross Reference Explorer\n3. n  to exit\n")
if choice == '1':
    import runstepper
elif choice == '2':
    import thomascsv
elif choice == "n":
    print("Thank you!")
    exit()
else:
    print("Please put in a valid input (1, 2, or n)\n")