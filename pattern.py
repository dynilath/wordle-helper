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
    v = [0, 0, 0, 0, 0]
    vret = [0, 0, 0, 0, 0]

    for i in range(5):
        if guess[i] == target[i]:
            v[i] = 2
            vret[i] = 2

    for i in range(5):
        for j in range(5):
            if v[j] > 0:
                continue
            elif guess[i] == target[j]:
                v[j] = 1
                vret[i] = 1
                break

    ret = 0
    for i in range(5):
        ret *= 3
        ret += vret[i]
    return ret
