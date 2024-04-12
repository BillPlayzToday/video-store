def generate_bit_combinations(n):
    if (n == 0):
        return [""]
    else:
        sub_combinations = generate_bit_combinations(n - 1)
        combinations = []
        for sub_combination in sub_combinations:
            combinations.append(sub_combination + "0")
            combinations.append(sub_combination + "1")
        return combinations