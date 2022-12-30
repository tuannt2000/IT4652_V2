from pandas import read_csv

class Rule:
    rules = []

    def load_properties(self, rule_filepath):
        # WHEN CHANGED
        dataFrame = read_csv(rule_filepath)
        # _ là index, iterrows là mảng dữ liệu (thư viện pandas)
        for _, row in dataFrame.iterrows():
            Rule.rules.append({'input': row.Input, 'output' : row.Output})

        return Rule.rules