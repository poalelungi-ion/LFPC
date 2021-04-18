from string import ascii_letters
import copy
import re


def large(rules, let, new_rules):
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            if len(values[i]) > 2:

                for j in range(0, len(values[i]) - 2):
                    # replace first rule
                    if j == 0:
                        rules[key][i] = rules[key][i][0] + let[0]
                    # add new rules
                    else:
                        rules.setdefault(new_key, []).append(values[i][j] + let[0])
                    new_rules.append(let[0])
                    # save letter, as it'll be used in next rule
                    new_key = copy.deepcopy(let[0])
                    # remove letter from free ascii_letters list
                    let.remove(let[0])
                # last 2 ascii_letters remain always the same
                rules.setdefault(new_key, []).append(values[i][-2:])

    return rules, let, new_rules


# Remove empty
def empty(rules, new_rules):
    # list with keys of empty rules
    e_list = []

    # find  non-terminal
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            # if key gives an empty state and is not in list, add it
            if values[i] == 'e' and key not in e_list:
                e_list.append(key)
                # remove empty state
                rules[key].remove(values[i])
        # if key doesn't contain any values, remove it from dictionary
        # used to remove the e rules via dictionary
        if len(rules[key]) == 0:
            if key not in rules:
                new_rules.remove(key)
            rules.pop(key, None)

    # delete empty
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            # check for rules in the form A->BC or A->CB, where B is in e_list
            # and C in vocabulary
            if len(values[i]) == 2:
                # check for rule in the form A->BC, excluding the case that
                # gives A->A as a result)
                if values[i][0] in e_list and key != values[i][1]:
                    rules.setdefault(key, []).append(values[i][1])
                # check for rule in the form A->CB, excluding the case that
                # gives A->A as a result)
                if values[i][1] in e_list and key != values[i][0]:
                    if values[i][0] != values[i][1]:
                        rules.setdefault(key, []).append(values[i][0])

    return rules, new_rules


# remoev short
def short(rules, new_rules):
    D = dict(zip(new_rules, new_rules))

    for key in D:
        D[key] = list(D[key])

    for letter in new_rules:  # letter = S
        for key in rules:
            if key in D[letter]:  # key = S
                values = rules[key]  # values = ['B']
                for i in range(len(values)):
                    if len(values[i]) == 1 and values[i] not in D[letter]:
                        D.setdefault(letter, []).append(values[i])

    rules, D = short1(rules, D)
    return rules, D


def short1(rules, D):
    # remove short rules (with length in right side = 1)
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            #       if values[i] == 'B':
            #           values[i] = 'AE'
            if len(values[i]) == 1:
                rules[key].remove(values[i])
        if len(rules[key]) == 0: rules.pop(key, None)

    # replace each rule A->BC with A->B'C', where B' in D(B) and C' in D(C)
    for key in rules:
        values = rules[key]
        for i in range(len(values)):
            # search all possible B' in D(B)
            for j in D[values[i][0]]:
                # search all possible C' in D(C)
                for k in D[values[i][1]]:
                    # concatenate B' and C' and insert a new rule
                    if j + k not in values:
                        rules.setdefault(key, []).append(j + k)

    return rules, D


def final_rules(rules, D, S):
    for let in D[S]:

        if not rules[S] and not rules[let]:
            for v in rules[let]:
                if v not in rules[S]:
                    rules.setdefault(S, []).append(v)

    return rules
# Print rules


def print_rules(rules):
    for key in rules:
        values = rules[key]
        for i in range(len(values)):
            if values[i].islower():
                ceva=values[i]
                ceva1=ceva[0]
                print(key + '->' + ceva1)
            else:
                print(key + '->' + values[i])
    return 1


def main():
    rules = {}
    new_rules = []

    let = list(ascii_letters[26:]) + list(ascii_letters[:25])

    let.remove('e')

    # Number of grammar rules
    while True:

        user_input = input('Give number of rules')
        try:
            # check if N is integer >=2
            N = int(user_input)
            if N <= 2:
                print('N must be a number >=2!')
            else:
                break
        except ValueError:
            print("That's not an int!")

    # Initial state
    while True:
        S = input('Give initial state')
        if not re.match("[A-Z]*$", S):  # ayy I love these things
            print('Initial state must be a single and capital character!')
        else:
            break
    for i in range(N):
        fr, to = map(str, input('Rule #' + str(i + 1)).split())
        for l in fr:
            if l != 'e' and l not in new_rules: new_rules.append(l)
            if l in let: let.remove(l)
        for l in to:
            if l != 'e' and l not in new_rules: new_rules.append(l)
            if l in let: let.remove(l)
        # Insert rule to dictionary
        rules.setdefault(fr, []).append(to)

    # remove large rules and print new rules
    print('\nRules after large rules removal')
    rules, let, new_rules = large(rules, let, new_rules)
    print_rules(rules)

    # remove empty rules and print new rules
    print('\nRules after empty rules removal')
    rules, new_rules = empty(rules, new_rules)
    print_rules(rules)
    # print new_rules

    print('\nRules after short rules removal')
    rules, D = short(rules, new_rules)
    print_rules(rules)

    print('\nFinal rules')
    rules = final_rules(rules, D, S)
    print_rules(rules)


if __name__ == '__main__':
    main()
