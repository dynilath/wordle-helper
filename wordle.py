import pattern
import data


def print_first5(src):
    for i in range(5):
        if i < len(src):
            print("%s - %f" % src[i])


if __name__ == "__main__":
    print("This is a resolver for wordle.")
    print("The program may suggests 5 words for input. The top one is the most suggested.")
    print("You may input as suggested, or just input what you want.")
    print("If there are no more than 5 words to suggest. The program will give as many suggest as possible, then terminate.")
    print("")
    print("The program may requires you to input guess and match.")
    print("In those cases, input something like 'wants 02121'. This stands for that you have input 'wants' in wordle and get ⬜🟩🟨🟩🟨 as result.")
    print("After each input, you will get some suggested words.")
    print("")
    print("Suggest input (word - weight):")

    possibles = data.get_possible_words_list()
    alloweds = data.get_allowed_words_list()
    possible_with_weight = data.get_word_list_with_entropy()

    while True:
        print_first5(possible_with_weight)

        if len(possible_with_weight) < 5:
            break

        a = input("Please input guess and match:\n")
        _guess, _result = a.split()
        pat = pattern.number_str_to_pattern(_result)
        guess = _guess[0:5]

        possibles = pattern.filter_pattern(pat, guess, possibles)
        alloweds = pattern.filter_pattern(pat, guess, alloweds)
        possible_with_weight = data.generate_word_list_with_entropy(
            possibles, alloweds)
