import json
import os
import random
import re
import sys

#part 1: Understanding the Problem and Planning
HOW_MANY_BOOK = 3
LINE = 128
PAGE = 64
pages = {}
page_number=0
line_window = {}
line_number = 0
char_window = []

#part 2: Preparing and Cleaning Text
def clean_line(line):
    return line.strip().replace( '-', '' ) + ' '  # Adding a space instead of a newline.

#part 4: Combining Multiple Books
def process_books(*paths):
    for path in paths:
        #print(f'Reading {path}')
        read_book( path )
        #print(f'{len(pages)}, {len(pages[1])}, {pages[len(pages)]}')
        #the reason why gitBash is counting 131 char is bc when you copy/paste you included single quotes and space

def read_book(file_path):
    global char_window
    with open(file_path, 'r', encoding='utf-8-sig') as fp:
        for line in fp:
            line = clean_line(line)
            if line.strip():
                for c in line:
                    process_char(c)
    if len(char_window) > 0:
        add_line()
    if len(line_window) > 0:
        add_page()

#part 3: Building Page and Line Buffers
def process_char(char):
    global char_window
    char_window.append(char)
    if len(char_window) == LINE:
        add_line()

def add_line():
    global char_window, line_number
    line_number += 1
    process_page( ''.join(char_window), line_number )
    char_window.clear()

def process_page(line, line_num):
    global line_window, pages, page_number
    line_window[line_num] = line
    if len(line_window) == PAGE:
        add_page()

def add_page():
    global line_number, line_window, pages, page_number
    page_number += 1
    pages[page_number] = dict(line_window)
    line_window.clear()
    line_number = 0

#part 5: Building the Codebook
def generate_code_book():
    global pages
    code_book = {}
    for page, lines in pages.items():
        for num, line in lines.items():
            for pos, char in enumerate(line):
                code_book.setdefault(char, []).append(f'{page}-{num}-{pos}')
    return code_book

def save(file_path, book):
    with open(file_path, 'w') as fp:
        # json.dump(book, fp, indent=4)
        json.dump(book, fp)

def load(file_path, *key_books, reverse=False):
    # reverse=False is a variable to traceback the file to decrypt the message
    if os.path.exists(file_path):
        with open(file_path, 'r') as fp:
            return json.load(fp)
    else:
        process_books(*key_books)
        if reverse:
            save(file_path, pages)
            return pages
        else:
            code_book = generate_code_book()
            save(file_path, code_book)
            return code_book

#part 6: Encryption and Decryption
def encrypt(code_book, message):
    cipher_text = []
    for char in message:
        index = random.randint(0, len(code_book[char]) - 1)
        cipher_text.append(code_book[char].pop(index))
    return '-'.join(cipher_text)

def decrypt(rev_code_book, ciphertext):
    plaintext = []
    for cc in re.findall(r'\d+-\d+-\d+', ciphertext):
        page, line, char = cc.split('-')
        plaintext.append(
            rev_code_book[page][line][int(char)])
    return ''.join(plaintext)

#part 7: Main Menu and Putting It All Together
def main_menu():
    print("""1). Encrypt
2). Decrypt
3). Quit
""");
    return int(input("Make a selection [1,2,3]: "))

def main():
    key_books = ('books/gatsby.txt', 'books/tess.txt', 'books/shakespeare.txt', 'books/gullivers.txt')
    code_book_path = 'code_books/book2.json'
    rev_code_book_path = 'code_books/book2_r.json'
    while True:
        try:
            choice = main_menu()
            match (choice):
                case 1:
                    code_book = load(code_book_path, *key_books)
                    message = input("Please enter your secret message: ")
                    print(encrypt(code_book, message))
                    continue;
                case 2:
                    rev_code_book = load(rev_code_book_path, *key_books, reverse=True)
                    message = input("Please enter your cipher text: ")
                    print(decrypt(rev_code_book, message))
                    continue;
                case 3:
                    sys.exit(0)
        except ValueError as ve:
            print("Improper selection.")


if __name__ == '__main__':
    main()

#process_books('./books/gatsby.txt', './books/tess.txt')
#process_books('./books/test.txt')
#cb = generate_code_book()
#save('./code_books/book1.json', cb)
#cb = load('./code_books/book1_r.json','./books/gatsby.txt', './books/tess.txt', reverse=True)

#message = input("type your secret message: ")
#print(
    #encrypt(
        #load('./code_books/book1.json','./books/gatsby.txt', './books/tess.txt'), message))
#print(cb)

#for key, value in cb.items():
    #print(f'{key}: {value}')

#ciphertext = '108-47-88-75-53-56-49-44-24-114-58-89-68-59-100-43-21-6-19-47-5-53-35-44-113-9-30-51-49-32-69-62-45-92-45-70-14-51-88-36-33-59-80-1-24-117-44-100-46-64-14{}'
#print(
    #decrypt(
        #load('./code_books/book1_r.json','./books/gatsby.txt', './books/tess.txt', reverse=True)
    #, ciphertext))

#man =>  1-1-26-1-1-5-1-1-2
#man =>  1-1-30-1-1-40-1-1-8