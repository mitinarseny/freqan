import itertools
import os
import re
import sys
import typing
from pprint import pprint

COUNT_SPACES = bool(os.environ.get('COUNT_SPACES', False))
DEFAULT_REPLACEMENTS_FILENAME = 'replacements.txt'
PERMUTE_EACH = 5
RUSSIAN_TOP = list('оеаинтсрвлкмдпуяыьгзбчйхжшюцщэфъё')
BLANK_SYMBOL = '•'


def isplit(s: str, delimiter: str = r'\s'):
    return (m.group(0) for m in re.finditer(r"[^{}]+".format(delimiter), s))


def main(args: typing.List[str]):
    encrypted_frequencies = dict()

    encrypted_filename = args[0]
    replacements_filename = args[1] if len(args) > 1 else DEFAULT_REPLACEMENTS_FILENAME
    encrypted_text = open(encrypted_filename, 'r').read()
    for ch in encrypted_text.lower():
        if ch not in RUSSIAN_TOP:
            continue
        encrypted_frequencies[ch] = encrypted_frequencies.get(ch, 0) + 1
    pprint(encrypted_frequencies)
    most_frequent = [_[0] for _ in sorted(encrypted_frequencies.items(), key=lambda t: t[1], reverse=True)]
    replace_with = dict()
    # replace_with = dict.fromkeys(encrypted_frequencies, BLANK_SYMBOL)
    with open(replacements_filename) as replacements_file:
        for line in replacements_file:
            from_char, to_char = line.split()
            # if from_char in replace_with:
            #     raise SyntaxError('replacements file must be: \'<from_char> <to_char>\\n\'')
            replace_with[from_char] = to_char
            most_frequent.remove(from_char)
            RUSSIAN_TOP.remove(from_char)
    i = 0
    while len(replace_with) < len(encrypted_frequencies):
        permutations = list(itertools.permutations(RUSSIAN_TOP[PERMUTE_EACH * i:PERMUTE_EACH * (i + 1)]))
        choose_replace_with = dict()
        for n, permutation in enumerate(permutations):
            choose_replace_with[n] = dict(zip(most_frequent[PERMUTE_EACH * i:PERMUTE_EACH * (i + 1)], permutation))
            print(f"""{n:>3}: {', '.join('->'.join(c) for c in choose_replace_with[n].items()):{6 * PERMUTE_EACH}}""",
                  end=' | ')
            for word in isplit(encrypted_text):
                contains_current = False
                for p in choose_replace_with[n]:
                    if p in word.lower():
                        contains_current = True
                        break
                if not contains_current:
                    continue
                word_to_print = ''
                for ch in word.lower():
                    word_to_print += choose_replace_with[n].get(ch) or replace_with.get(ch,
                                                                                        BLANK_SYMBOL if ch in RUSSIAN_TOP else ch)
                print(f'{word_to_print:15}', end='', sep='')
            print('')
        chosen_permutation = permutations[int(input(f'Choose permutation [0-{len(permutations) - 1}]: '))]
        current_replace_with = dict(zip(most_frequent[PERMUTE_EACH * i:PERMUTE_EACH * (i + 1)], chosen_permutation))
        replace_with.update(current_replace_with)
        i += 1
    print(''.join(replace_with.get(i.lower(), i) for i in encrypted_text))


if __name__ == '__main__':
    main(sys.argv[1:])
