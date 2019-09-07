#!/usr/bin/env python3
# coding: utf-8

"""Phonetic transcription of Slovak language."""

import re
import sys


# function for the phonetic transcription of Slovak language to IPA
def ipa_slovak(text):
    """Phonetic transcription to IPA of given Slovak text or word."""
    # set transription table (IPA)
    vowels = {'a': 'a', 'e': 'ɛ', 'i': 'ɪ', 'y': 'ɪ', 'o': 'ɔ', 'u': 'u',
              'á': 'aː', 'é': 'ɛː', 'í': 'iː', 'ý': 'iː', 'ó': 'ɔː',
              'ú': 'uː', 'ô': 'u̯ɔ', 'ä': 'æ'}

    sonors = {'l': 'l', 'm': 'm', 'n': 'n', 'ň': 'ɲ', 'r': 'r', 'j': 'j',
              'ŕ': 'rː', 'ĺ': 'ɭː', 'ľ': 'ʎ'}

    voice_voice = {'dz': 'd͡z', 'dž': 'd͡ʒ', 'v': 'v', 'g': 'ɡ', 'b': 'b',
                   'z': 'z', 'ž': 'ʒ', 'd': 'd', 'ď': 'ɟ', 'h': 'ɦ',
                   'ch': 'ɣ', 'x': 'ks', 'w': 'v', 'q': 'kv'}

    voice_voiceless = {'dz': 't͡s', 'dž': 't͡ʃ', 'v': 'f', 'g': 'k', 'b': 'p',
                       'z': 's', 'ž': 'ʃ', 'd': 't', 'ď': 'c', 'h': 'x',
                       'ch': 'x', 'x': 'ks', 'w': 'f', 'q': 'kf'}

    voiceless_voiceless = {'c': 't͡s', 'č': 't͡ʃ', 'f': 'f', 'k': 'k',
                           'p': 'p', 's': 's', 'š': 'ʃ', 't': 't', 'ť': 'c'}

    voiceless_voice = {'c': 'd͡z', 'č': 'd͡ʒ', 'f': 'v', 'k': 'ɡ', 'p': 'b',
                       's': 'z', 'š': 'ʒ', 't': 'd', 'ť': 'ɟ'}

    # exceptions
    vowel_prefixes = ('nade', 'obe', 'pode', 'roze', 'se', 've', 'ná',
                      'vze', 'ze', 'ne', 'vele', 'ante', 'de', 'pre', 're',
                      'vice', 'na', 'za', 'leda', 'pa', 'pra', 'sotva', 'ana',
                      'dia', 'extra', 'hepta', 'hexa', 'infra', 'intra',
                      'kontra', 'meta', 'para', 'supra', 'tetra', 'ultra',
                      'mimo', 'okolo', 'polo', 'skoro', 'alo', 'hetero',
                      'homo', 'hypo', 'iso', 'kvadro', 'makro', 'mezzo',
                      'mikro', 'proto', 'pseudo', 'retro', 'mono', 'mili',
                      'kilo', 'zá')

    # TODO: foreign words

    # split on clauses
    text = text.replace('...', '.')
    parts = re.split(r'[,;\.\!\?\"\-\–$]', text)
    delimiters = [l for l in text if l in ',;.!?"-–']

    # transcript clauses
    transcripted_parts = list()
    for part in parts:
        # check input
        if not part:
            transcripted_parts.append('')
            continue

        # prepare text to list of letters to transcript
        part = part.lower().strip()
        part = part.replace('ch', 'A').replace('dz', 'B').replace('dž', 'C')
        digraphs = {'A': 'ch', 'B': 'dz', 'C': 'dž'}
        part = list(part)
        for l in range(len(part)):
            if part[l] in digraphs:
                part[l] = digraphs[part[l]]

        # transcripted input
        ipa = [l for l in part]

        # find out intervals for neutralization and assimilation
        posit_vowel = [-1] + [i for i in range(len(part)) if part[i] in vowels]
        posit_sonor = [i for i in range(len(part)) if part[i] in sonors]

        # neutralization
        j = posit_vowel[-1]
        if posit_sonor and posit_sonor[-1] > posit_vowel[-1]:
            j = posit_sonor[-1]

        i = len(part) - 1
        while i > j:
            if part[i] in voice_voiceless:
                ipa[i] = voice_voiceless[part[i]]
            elif part[i] in voiceless_voiceless:
                ipa[i] = voiceless_voiceless[part[i]]
            elif part[i] in sonors:
                ipa[i] = sonors[part[i]]
            i -= 1

        # transctiption and assimilation
        while posit_vowel:
            i, k = j, j
            j = posit_vowel.pop()
            voice = None  # assimil. type (N=uknown, T=voice, F=voiceless)
            while i > j:
                # transcription of vowels
                if part[i] in vowels:
                    # diphtongs ou, eu, au
                    if part[i] in 'aeo' and len(part) > i+1 \
                       and part[i+1] == 'u':
                        test = [True if p == ''.join(part[i+1-len(p):i+1])
                                else False
                                for p in vowel_prefixes]
                        if any(test):
                            ipa[i] = vowels[part[i]] + ' ʔ'
                        else:
                            ipa[i] = vowels[part[i]] + 'u̯'
                            ipa[i+1] = ''
                    # diphtongs ia, ie, iu
                    elif (part[i] == 'i' and i < len(part) - 1 and
                          part[i+1] in 'aeu'):
                        test = [True if p == ''.join(part[i+1-len(p):i+1])
                                else False
                                for p in vowel_prefixes]
                        if any(test):
                            ipa[i] = vowels[part[i]] + ' ʔ'
                        else:
                            ipa[i] = 'i̯' + ipa[i+1]
                            ipa[i+1] = ''
                    # otherwise
                    else:
                        ipa[i] = vowels[part[i]]
                    # initial of word (glotal plosive)
                    if i == 0 or part[i-1] == ' ' and part[i-2] in vowels:
                        ipa[i] = 'ʔ ' + ipa[i]

                # transcription of sonors and consonants
                elif k != i:
                    # sonors
                    if part[i] in sonors:
                        voice = None
                        # nn
                        if part[i] == 'n' and part[i+1] == 'n':
                            ipa[i] = ''
                        # nk, ng
                        elif part[i] == 'n' and part[i+1] in 'kg':
                            ipa[i] = 'ŋ'
                        # ni, ní, ne, nie, niu, nia
                        elif part[i] == 'n' and part[i+1] in 'eií':
                            ipa[i] = 'ɲ'
                        # li, lí, le, lie, liu, lia
                        elif part[i] == 'l' and part[i+1] in 'eií':
                            ipa[i] = 'ʎ'
                        # mv, mf
                        elif part[i] == 'm' and part[i+1] in 'vf':
                            ipa[i] = 'ɱ'
                        # otherwise
                        else:
                            ipa[i] = sonors[part[i]]
                    # kk
                    elif part[i] == 'k' and part[i+1] == 'k':
                        ipa[i] = ''
                    # choose type of assimilation
                    elif voice is None:
                        # voiced
                        if part[i] in voice_voice:
                            voice = True
                            # v
                            if part[i] == 'v':
                                voice = None
                            # di, dí, de, dia, die, diu
                            elif part[i] == 'd' and part[i+1] in 'iíe':
                                ipa[i] = 'ɟ'
                            # otherwise
                            else:
                                ipa[i] = voice_voice[part[i]]
                        # voiceless
                        elif part[i] in voiceless_voiceless:
                            voice = False
                            # ti, tí, te, tia, tie, tiu
                            if part[i] == 't' and part[i+1] in 'iíe':
                                ipa[i] = 'c'
                            # otherwise
                            else:
                                ipa[i] = voiceless_voiceless[part[i]]
                    # assimilation
                    else:
                        # voiced group
                        if voice is True and part[i] in voice_voice:
                            ipa[i] = voice_voice[part[i]]
                        elif voice is True and part[i] in voiceless_voice:
                            ipa[i] = voiceless_voice[part[i]]
                        # voiceless group
                        elif voice is False and part[i] in voice_voiceless:
                            ipa[i] = voice_voiceless[part[i]]
                        elif voice is False and part[i] in voiceless_voiceless:
                            ipa[i] = voiceless_voiceless[part[i]]

                i -= 1

        # clean empty cells and save transcripted clauses
        ipa = list(filter(None, ipa))
        transcripted_parts.append(ipa)

    # return transcripted text
    transcripted_parts = [' '.join(part) for part in transcripted_parts]
    transcripted = ''
    i = 0
    while i < len(delimiters):
        transcripted += transcripted_parts[i] + delimiters[i]
        i += 1
    if i < len(transcripted_parts):
        transcripted += transcripted_parts[-1]

    transcripted = re.sub(r'\.|\?|\!|\;|\"', '   ||   ', transcripted)
    transcripted = re.sub(r'\,|\-|\–', '   |   ', transcripted)
    return transcripted


# running script if it is used in shell (with stdin or path to file)
if __name__ == '__main__':

    if not sys.stdin.isatty():  # read from stdin
        for line in sys.stdin:
            print(ipa_slovak(line.strip()), sep='\t')

    else:  # read from file
        if len(sys.argv) == 2:
            with open(sys.argv[1], mode='r', encoding='utf-8') as f:
                for line in f:
                    print(ipa_slovak(line.strip()), sep='\t')
        else:
            print('Error: Use script in pipeline or give the path '
                  'to the relevant file in the first argument.')
