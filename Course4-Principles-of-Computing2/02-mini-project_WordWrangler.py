"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

#preventing code running time limet:
codeskulptor.set_timeout(100)


WORDFILE = "assets_scrabble_words3.txt"

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    output = []
    for item in list1:
        if item not in output:
            output.append(item)
    return output

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    output = []
    for item in list1:
        if item in list2:
            output.append(item)
    return output


# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    output = []
    #choose the smaller-sized list to be the iterating list in the
    #for loop
    copy1 = []
    copy2 = []
    if len(list1) <= len(list2):
        copy1 = list1[:]
        copy2 = list2[:]
    else:
        copy1 = list2[:]
        copy2 = list1[:]

    while (len(copy1) > 0) and (len(copy2) > 0):
        copy1_item = copy1[0]
        copy2_item = copy2[0]
        if copy1_item <= copy2_item:
            output.append(copy1_item)
            copy1.pop(0)
        else:
            output.append(copy2_item)
            copy2.pop(0)

    if len(copy1) > 0:
        output.extend(copy1)
    elif len(copy2) > 0:
        output.extend(copy2)
    #print output
    return output

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
# base case for empty/one item lists

    if len(list1) <= 1:
        return list1
# determine midsection of the list

    else:
        half = len(list1)/2
        first_half = list1[ :half]
        second_half = list1[half: ]
#        list2 = merge(first_half, second_half)
        return merge(merge_sort(first_half), merge_sort(second_half))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]
    elif len(word) == 1:
        return [""] + [word]
    else:
        first_letter = word[0]

        rest_letters = word[1: ]

        rest_strings = gen_all_strings(rest_letters)

        first_letter_strings = []
        for rest_word in rest_strings:
            for index in range(len(rest_word)+1):
                string = ""
                if index == 0:
                    string = first_letter + rest_word
                elif index == len(rest_word):
                    string = rest_word + first_letter
                else:
                    string = rest_word[ :index] + first_letter + rest_word[index: ]
                first_letter_strings.append(string)

    return first_letter_strings + rest_strings

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(WORDFILE)
    netfile = urllib2.urlopen(url)

    word_list = []
    for word in netfile.readlines():
        word = word[:-1]
        word_list.append(word)

    return word_list

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

# TESTS
# Test remove_duplicates(list1)
print remove_duplicates([1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8])
print remove_duplicates([1])
print remove_duplicates([])
print remove_duplicates([1, 1, 1, 1, 1, 2, 3, 3, 3, 3, 3])
print remove_duplicates([1, 1, 2, 2, 1])
print remove_duplicates([1, 1, 2, 2])
print ""

# Test intersect(list1, list2)
print intersect([1, 2, 3, 4], [2, 4, 5])
print intersect([1, 2, 3, 4, 4], [2, 4, 5])
print intersect([1, 2, 3, 4, 4], [2, 2, 4, 5])
print intersect([1, 2, 3, 4, 4], [2, 4, 4, 5])
print intersect([1, 3, 4, 4], [2, 5])
print intersect([], [1, 2, 3])
print ""

# Test merge(list1, list2)
print merge([1, 2, 3, 4], [2, 4, 5])
print merge([1, 2, 3, 4, 4], [2, 4, 5])
print merge([1, 2, 3, 4, 4], [2, 2, 4, 5])
print merge([1, 2, 3, 4, 4], [2, 4, 4, 5])
print merge([1, 3, 4, 4], [2, 5])
print merge([], [1, 2, 3])
print merge([], [])
print ""

# Test merge_sort(list1)
print merge_sort([1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8])
print merge_sort([1])
print merge_sort([])
print merge_sort([1, 1, 1, 1, 1, 2, 3, 3, 3, 3, 3])
print merge_sort([1, 1, 2, 2, 1])
print merge_sort([1, 1, 2, 2])
print ""

# Test gen_all_strings(word)
print gen_all_strings("")
print gen_all_strings("a")
print gen_all_strings("ab")
print gen_all_strings("abc")
