from urllib.request import urlopen, hashlib
import time
import string
import sys
from itertools import chain, product

# ---
# global variables
#
attempts = 0
start = 0
end = 0

# ---
# provides a menu with 4 options
#
def menulist():
    global attempts
    # resets the number of attempts to 0 for a new attack run.
    attempts = 0
    print(
        "Welcome to the password cracker. \n\n" \
        + "Press 1 if you need to hash your password. \n" \
        + "Press 2 to enter an already hashed password for a dictionary attack. \n" \
        + "Press 3 to enter an already hashed password for a brute force attack. \n" \
        + "Press 4 to exit. \n")
    menu = int(input("How would you like to proceed:  "))

    # if you only have the plaintext password, this will provide an md5 hash of that password, and then prompt user on how to move forward
    if menu == 1:

        password = input("\nInput the password to hash:\n>")
        print("\nMD5 hash:\n")
        setpass = bytes(password, 'utf-8')
        hash_object = hashlib.md5(setpass)
        guess_pw = hash_object.hexdigest()
        print(guess_pw)
        print("\nCopy and paste the above hash into the password cracker.\n\nHow would you ready to proceed?")
        passwordhashmenu = input("Press 'd' for Dictionary Attack, " \
                                 + "'b' for Brute Force Attack, " \
                                 + "or any other key to return to the main menu:\n").lower()

        # prompt user on how to move forward
        if passwordhashmenu == "d":
            dictionaryattack()

        elif passwordhashmenu == "b":
            bruteforceattack()

        else:
            menulist()

    # if you already have an md5 hash, then dictionaryattack() (defined below) will run for a dictionary attack
    elif menu == 2:
        dictionaryattack()

    # if you already have an md5 hash, then bruteforceattack() (defined below) will run for a dictionary attack
    elif menu == 3:
        bruteforceattack()

    # if you select this option the program will end
    elif menu == 4:
        sys.exit("Thank you for using our password cracking program!")

    # if you provide an option other than 1, 2, 3 or 4
    else:
        print("Invalid entry.  Try again")
        menulist()

# ---
# dictionary attack function
#
def dictionaryattack():
    # reference global variable start
    global start

    # the user selects the dictionary to use
    print("Do you have a dictionary you would like to use?")
    dictChoice = input("Please enter 'y' for yes or 'n' for no\n").lower()

    if dictChoice == 'y':
        # user enters the file they would like to use
        file = input("Please enter the name of the file you would like to use.\n")
        # the file is opened for reading
        passwordFile = open(file, 'r')
        PASSWORD_LIST = str(passwordFile.read())

    elif dictChoice == 'n':
        # this provides a password list of the top 10,000 passwords
        PASSWORD_LIST = str(urlopen(
            'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt').read(),
                            'utf-8')

    else:
        # the user did not enter a valid input and is ask to enter a valid input
        print("Invalid entry.  Try again")
        dictionaryattack()

    # the user inputs the md5 hash to crack
    md5hash = input("\nPlease input the hash to crack:\n>")

    # asks the user if they would like to use mangle rules
    print("Do you want to apply mangle rules?")
    rules = input("Please enter 'y' to apply rules, or any other key to continue without applying rules.\n").lower()

    # start the cracking timer
    start = time.time()
    
    if rules == 'y':
        # mangle rules
        # the code for this was based off of the leetspeak code on google
        ruleOne = {'a':'@', 'b':'8', 'c':'(', 'd':'6', 'e':'3', 'f':'#', 'g':'9', 'h':'#', 'i':'1', 'k':'<', 'l':'1', 'o':'0', 'q':'9', 's':'5', 't':'+', 'v':'>', 'w':'uu', 'x':'%', 'y':'?'}
        ruleTwo = {'tt':'2T', 'i':'!', 's':'$', 'a':'4', 'you':'j00', 'b':'B', 't':'7', 'T':'7'}
        for guess in PASSWORD_LIST.split('\n'):
            wordR1 = guess
            wordR2 = guess
            #applies the first set of rules from every word in the wordlist to test
            for x, y in ruleOne.items():
                wordR1 = wordR1.replace(x, y)
                hashcompare(md5hash, wordR1)

            #applies the second set of rules from every word in the wordlist to test
            for x, y in ruleTwo.items():
                wordR2 = wordR2.replace(x, y)
                hashcompare(md5hash, wordR2)

            #tests every word in the wordlist    
            hashcompare(md5hash, guess)
            
        # if the password list is exhausted and no match is found
        print("\nPassword not in database, we'll get them next time.\n")
        menulist()
    else:
        # a for loop to look line by line at each of the entries in the file
        for guess in PASSWORD_LIST.split('\n'):
            hashcompare(md5hash, guess)

        # if the password list is exhausted and no match is found
        print("\nPassword not in database, we'll get them next time.\n")
        menulist()

    # close out the file
    passwordFile.close()

# ---
# brute force attack function
#
def bruteforceattack():
    # brute force menu
    print("\nPlease select minimum and maximum password lengths:")

    # ensure minimum length is a number
    while True:
        try:
            minimum_length = int(input("Minimum Length:  "))
            break
        except ValueError:
            print("\nPlease insert a valid number!\n")

    # ensure maximum length is a number
    while True:
        try:
            maximum_length = int(input("Maximum Length:  "))
            break
        except ValueError:
            print("\nPlease insert a valid number!\n")

    # select character set to be used for brute force method
    print("\nPlease select your prefered Character Set from the following options: \n" \
          + "Press 1 for alphabetical characters: [a-zA-Z] \n" \
          + "Press 2 for alphanumeric characters: [a-zA-Z0-9] \n" \
          + "Press 3 for alphanumeric characters + punctuation: [a-zA-Z0-9!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~] \n")

    character_set_menu = int(input("Character Set:  "))

    # character set variables
    # https://stackoverflow.com/questions/16060899/alphabet-range-in-python
    LOWERCASE_LIST = list(string.ascii_lowercase)  # "abcdefghijklmnopqrstuvwxyz"
    UPPERCASE_LIST = list(string.ascii_uppercase)  # "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    DIGITS_LIST = list(string.digits)  # "0123456789"
    PUNCTUATION_LIST = list(string.punctuation)  # "!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"

    # combine specified character set as selected by user
    # alphabetical
    if character_set_menu == 1:
        character_set = LOWERCASE_LIST + UPPERCASE_LIST

    # alphanumeric
    elif character_set_menu == 2:
        character_set = LOWERCASE_LIST + UPPERCASE_LIST + DIGITS_LIST

    # alphanumeric + punctuation
    elif character_set_menu == 3:
        character_set = LOWERCASE_LIST + UPPERCASE_LIST + DIGITS_LIST + PUNCTUATION_LIST

    # if you provide an option other than 1, 2, or 3
    else:
        print("Invalid entry.  Try again")
        bruteforceattack()

    # send variables to bruteforceiterate() function
    bruteforceiterate(minimum_length, maximum_length, character_set)

# ---
# brute force iteration function
#
def bruteforceiterate(min, max, characters):
    # reference global variable start
    global start

    # the user inputs the md5 hash to crack
    md5hash = input("\nPlease input the hash to crack:\n>")

    # start the cracking timer
    start = time.time()

    # uses python's built-in chain and product functions in order to perform iterations across the specified character set
    # https://docs.python.org/3/library/itertools.html#itertools.chain
    # https://docs.python.org/3/library/itertools.html#itertools.product
    # https://www.youtube.com/watch?v=1C8cmzZeho4
    for chars in chain.from_iterable(product(characters, repeat=i) for i in range(min, max + 1)):
        guess = str("".join(chars))
        hashcompare(md5hash, guess)

    # if the password list is exhausted and no match is found
    print("\nPassword not in database, we'll get them next time.\n")

# ---
# hash compare function
#
def hashcompare(md5hash_compare, guess_compare):
    # reference global variables end and attempts
    global end
    global attempts

    # a condensed version of what we did in menu option 2 above, where we hash the common passwords from the list
    hashedGuess = hashlib.md5(bytes(guess_compare, 'utf-8')).hexdigest()

    # comparing each of the hashed common passwords to the user input to determine if there is a match
    if hashedGuess == md5hash_compare:
        end = time.time()
        # if they match, print the correct guess and quit the program.
        print("\nThe password is", str(guess_compare))
        if attempts == 1:
            print("It took", str(end - start), "seconds\nand", str(attempts), "attempt to crack your password\n")
        else:
            print("It took", str(end - start), "seconds\nand", str(attempts), "attempts to crack your password\n")
        menulist()

    # or else, if they don't match, continue to the next hashed password and compare those
    elif hashedGuess != md5hash_compare:
        # print("Password guess", str(guess_compare), "does not match, trying next...")
        attempts += 1


# ---
# initiates the program
#
menulist()
