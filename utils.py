def letter_count_in_word(word):
    letters = ''.join(([f'{chr(x + ord("a"))}{chr(x + ord("A"))}' for x in range(26)])) + 'ąćęłńóśźż' + 'ĄĆĘŁŃÓŚŹŻ'
    return sum(1 for c in word if c in letters)
