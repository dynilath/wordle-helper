def pattern_to_display(pattern):
    display = ["⬜", "🟨", "🟩"]
    ret = ""
    for i in range(0, 5):
        v = pattern % 3
        ret = "%s%s" % (display[v], ret)
        pattern = int(pattern / 3)
    return ret


def number_str_to_pattern(number):
    ret = 0
    for i in range(0, 5):
        v = 0
        if number[i] == '1':
            v = 1
        elif number[i] == '2':
            v = 2
        ret *= 3
        ret += v
    return ret


def filter_pattern(pattern, guess, src_list):
    ret = []
    for w in src_list:
        p = match_pattern(guess, w)
        if p == pattern:
            ret.append(w)
    return ret


def match_pattern(guess, target):
    ret = 0
    for i in range(5):
        v = 0
        if guess[i] == target[i]:
            v = 2
        elif target.find(guess[i]) >= 0:
            v = 1
        ret *= 3
        ret += v
    return ret
