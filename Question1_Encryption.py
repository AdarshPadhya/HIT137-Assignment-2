'''
HIT137 - Group Assignment 2

Question 1: This program reads text from a file named raw_text.txt and encrypts its contents using a custom encryption method.The encryption 
depends on whether characters are lowercase or uppercase and their position in the alphabet. Two user inputs, shift1 and shift2, are used to 
determine how much each character is shifted. The encrypted result is then saved in a new file called encrypted_text.txt.

Group Name: DAN/EXT 26
Group Members:
- Adarsh Padhya - S401743
- Aaditya Kulkarni - S403124
- Aaron Menezes- S401432
- Krupa Maria Salim - S398540

Program Description: This Python program performs file-based text encryption using a rule-based shifting technique. It first takes two integer 
inputs (shift1 and shift2) from the user. The program reads the content of raw_text.txt and processes each character individually.

For lowercase letters:

Characters from 'a' to 'm' are shifted forward by shift1 * shift2
Characters from 'n' to 'z' are shifted backward by shift1 + shift2

For uppercase letters:

Characters from 'A' to 'M' are shifted backward by shift1
Characters from 'N' to 'Z' are shifted forward by shift2²

All other characters such as spaces, numbers, and symbols remain unchanged. The encrypted text is written to encrypted_text.txt. The program uses a
function-based approach for better structure and readability.

'''

#Code begins


#Take shift values from user
shift1 = int(input("Enter shift1: "))
shift2 = int(input("Enter shift2: "))


#Read the content of the input file
with open("raw_text.txt", "r") as file:
    text = file.read()


#Function to encrypt the given text
def encrypt(text, shift1, shift2):

    #store final encrypted result
    encrypted_text = ""

    #Loop through each character in the text
    for char in text:

        #Check if character is lowercase (a-z)
        if char.islower():

            #If character is in first half (a-m)
            if 'a' <= char <= 'm':

                #calculate forward shift
                shift = shift1 * shift2
                #convert letter to position (0-25)
                pos = ord(char) - ord('a')
                #apply shift and wrap around
                pos = (pos + shift) % 26
                #convert back to letter
                new_char = chr(pos + ord('a'))

            #If character is in second half (n-z)
            else:

                #calculate backward shift
                shift = shift1 + shift2
                #convert letter to position (0-25)
                pos = ord(char) - ord('a')
                #shift backward and wrap
                pos = (pos - shift) % 26
                #convert back to letter
                new_char = chr(pos + ord('a'))

        #Check if character is uppercase (A-Z)
        elif char.isupper():

            #If character is in first half (A-M)
            if 'A' <= char <= 'M':

                #backward shift
                shift = shift1
                pos = ord(char) - ord('A')
                pos = (pos - shift) % 26
                new_char = chr(pos + ord('A'))
            
            #If character is in second half (N-Z)
            else:

                #forward shift (square of shift2)
                shift = shift2 ** 2
                pos = ord(char) - ord('A')
                pos = (pos + shift) % 26
                new_char = chr(pos + ord('A'))

        #If character is not a letter (space, number, symbol)
        else:

            #keep it unchanged
            new_char = char  

        #Add the encrypted character to result
        encrypted_text += new_char


    #Return the final encrypted text
    return encrypted_text


#Call the encryption function
encrypted_text = encrypt(text, shift1, shift2)


#Write the encrypted text to a new file
with open("encrypted_text.txt", "w") as file:
    file.write(encrypted_text)


#Print confirmation message
print("Encryption completed! Check encrypted_text.txt")

def decrypt(text, shift1, shift2):

    # this will store the final decrypted message
    decrypted_text = ""

    # go through each character one by one
    for char in text:

        # check if the character is lowercase
        if char.islower():

            # if it belongs to first half (a-m)
            if 'a' <= char <= 'm':
                # during encryption we moved forward, so now we move backward
                shift = shift1 * shift2
                pos = ord(char) - ord('a')
                pos = (pos - shift) % 26
                new_char = chr(pos + ord('a'))

            else:
                # for second half (n-z), encryption moved backward, so now we go forward
                shift = shift1 + shift2
                pos = ord(char) - ord('a')
                pos = (pos + shift) % 26
                new_char = chr(pos + ord('a'))

        # check if the character is uppercase
        elif char.isupper():

            # if in first half (A-M)
            if 'A' <= char <= 'M':
                # encryption moved backward, so here we move forward
                shift = shift1
                pos = ord(char) - ord('A')
                pos = (pos + shift) % 26
                new_char = chr(pos + ord('A'))

            else:
                # encryption moved forward, so now we reverse it (move backward)
                shift = shift2 ** 2
                pos = ord(char) - ord('A')
                pos = (pos - shift) % 26
                new_char = chr(pos + ord('A'))

        else:
            # if it's not a letter, just keep it as it is
            new_char = char

        # add the decrypted character to final result
        decrypted_text += new_char

    # return the full decrypted string
    return decrypted_text

# open the encrypted file and read its content
with open("encrypted_text.txt", "r") as file:
    encrypted_data = file.read()

# decrypt the content of the file using decryption function
decrypted_text = decrypt(encrypted_data, shift1, shift2)

# save the decrypted result into a new file
with open("decrypted_text.txt", "w") as file:
    file.write(decrypted_text)

print("Decryption completed! Check decrypted_text.txt")

def verify():

    # read the original file
    with open("raw_text.txt", "r") as file:
        original = file.read()

    # read the decrypted file
    with open("decrypted_text.txt", "r") as file:
        decrypted = file.read()

    # compare both contents
    if original == decrypted:
        print("Decryption was Successful! Both the files are matching.")
    else:
        print("Decryption has Failed! Files are not the same.")

verify()