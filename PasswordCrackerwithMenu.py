from urllib.request import urlopen, hashlib

#provides a menu with 3 options
def menulist():
    print(
        "Welcome to the password cracker.  \n Press 1 to enter an already hashed password \n Press 2 if you need to hash your password \n Press 3 for brute force without hashing \n")
    menu = input("How would you like to proceed?\n")

#if you already have an md5 hash, then alreadyhashed (defined below) will run
    if menu == "1":
        alreadyhashed()

#if you only have the plaintext password, this will provide an md5 hash of that password, and then loop you back to run alreadyhashed from the first menu option
    elif menu == "2":
        password = input("Input the password to hash\n>")
        print("\nMD5 hash:\n")
        setpass = bytes(password, 'utf-8')
        hash_object = hashlib.md5(setpass)
        guess_pw = hash_object.hexdigest()
        print(guess_pw)
        print("Copy and paste the above hash into the password cracker.\n Are you ready to proceed?")
        passwordhashmenu=input("press Y to continue or any other key to return to the main menu:\n")
        if passwordhashmenu =="Y" or passwordhashmenu=="y":
            alreadyhashed()
        else:
            menulist()

#this will run a brute force on your password
    elif menu == "3":
        bruteforce()

#if you provide an option other than 1, 2, or 3
    else:
        print("Invalid entry.  Try again")
        menulist()

def alreadyhashed():
    # the user inputs the md5 hash to crack
    md5hash = input("Please input the hash to crack.\n>")

    # this provides a password list of the top 10,000 passwords
    LIST_OF_COMMON_PASSWORDS = str(urlopen(
        'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt').read(),
                               'utf-8')

    # a for loop to look line by line at each of those 10,000 passwords
    for guess in LIST_OF_COMMON_PASSWORDS.split('\n'):

        # a condensed version of what we did in menu option 2 above, where we hash the common passwords from the list
        hashedGuess = hashlib.md5(bytes(guess, 'utf-8')).hexdigest()

        # comparing each of the hashed common passwords to the user input to determine if there is a match
        if hashedGuess == md5hash:

            # if they match, print the correct guess and quit the program.
            print("The password is", str(guess))
            quit()
        # or else, if they don't match, continue to the next hashed password and compare those
        elif hashedGuess != md5hash:
            print("Password guess ", str(guess), " does not match, trying next...")

    # if the password list is exhausted and no match is found
    print("Password not in database, we'll get them next time.")

def bruteforce():
    print("We're still working on that")

#initiates the program
menulist()