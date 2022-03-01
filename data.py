import os
import math
import json
import pickle
from tkinter.tix import Tree
from tqdm import tqdm

import pattern

data_dir = os.path.join(os.getcwd(), "data")

source_js_file = os.path.join(os.getcwd(), "main.bfba912f.js")

possible_words_file = os.path.join(data_dir, "possible_words.txt")
allowed_words_file = os.path.join(data_dir, "allowed_words.txt")
possible_words_with_entropy_file = os.path.join(
    data_dir, "possible_words_with_entropy.pickle")


def get_word_from_source(file, signature):
    if not os.path.exists(file):
        print("Please downloads the javascript source from the wordle website and paste it in %s." % os.getcwd())
        print("You can find a script named \"main.<some hex digits>.js\" from the html source.")
        exit(1)
    text = ""
    with open(file, "r", encoding="utf8") as fp:
        text = "".join(fp.readlines())
    i_sign = text.find(signature)
    if i_sign < 0:
        print("signature word not found!")
        exit(1)
    i_l_bracket = text.rfind("[", 0, i_sign)
    i_r_bracket = text.find("]", i_sign)
    word_list_str = text[i_l_bracket:i_r_bracket+1]
    return json.loads(word_list_str)


def set_word_list(file, src):
    first_line = True
    with open(file, "w+", encoding="utf8") as fp:
        for w in src:
            if first_line:
                first_line = False
            else:
                fp.write("\n")
            fp.write(w)


def guess_vs_possibles(guess, possible_list):
    ret = {}
    for w in possible_list:
        pat = pattern.match_pattern(guess=guess, target=w)
        if pat not in ret:
            ret.setdefault(pat, 1)
        else:
            ret[pat] = ret[pat] + 1
    return ret


def average_info_entropy(guess, possible_list):
    guess_result_pat = guess_vs_possibles(guess, possible_list)
    aver_ent = 0
    cnt = len(guess_result_pat)
    for k, v in guess_result_pat.items():
        aver_ent += -math.log2(v/len(possible_list))
    return aver_ent/cnt


def set_words_with_entropy_file(file, possible_with_entropy):
    with open(file, "wb+") as fp:
        fp.write(pickle.dumps(possible_with_entropy))


def get_word_list(file):
    ret = []
    with open(file) as fp:
        ret.extend([word.strip() for word in fp.readlines()])
    return ret


def generate_word_list_with_entropy(possibles, alloweds, progress=True):
    ret = []
    if progress:
        for w in tqdm(alloweds):
            e = average_info_entropy(w, possibles)
            ret.append((w, e))
    else:
        for i in alloweds:
            e = average_info_entropy(w, possibles)
            ret.append((w, e))
    ret.sort(key=lambda x: x[1], reverse=True)
    return ret


def get_words_with_entropy(file):
    if os.path.exists(file):
        with open(file, "rb") as fp:
            return pickle.loads(fp.read())
    else:
        words_with_ent = generate_word_list_with_entropy(
            possbile_words, allowed_words)

        with open(file, "wb+") as fp:
            fp.write(pickle.dumps(words_with_ent))
        return words_with_ent


def get_possible_words_list():
    return get_word_list(possible_words_file)


def get_allowed_words_list():
    return get_word_list(allowed_words_file)


def get_word_list_with_entropy():
    return get_words_with_entropy(
        possible_words_with_entropy_file)


if __name__ == "__main__":
    signature_possible = "\"forge\""
    signature_allowed = "\"aceta\""

    possbile_words = get_word_from_source(source_js_file, signature_possible)
    allowed_words = get_word_from_source(source_js_file, signature_allowed)

    allowed_words.extend(possbile_words)
    set_word_list(possible_words_file, possbile_words)
    set_word_list(allowed_words_file, allowed_words)

    possible_with_entropy = get_words_with_entropy(
        possible_words_with_entropy_file)
