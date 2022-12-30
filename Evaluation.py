class Evaluation():
    def __init__(self, args):
        self.job = args['jb']
        self.gender = args['gd']
        self.interes = args['it']
        self.purpose = args['pp']
        self.age = args['age']

    # các lựa chọn của người dùng
    def print_rule(self):
        print('【RULE】',self.job, self.gender, self.interes, self.purpose, self.age)

    def filter_gender(self, rule_list):
        result = []
        for rule in rule_list:
            if self.gender == 1 and rule['input'] == 'Nam':
                result.append(rule['output'])
            elif self.gender == 2 and rule['input'] == 'Nữ':
                result.append(rule['output'])
        return result
    
    def filter(self, rule_list, filter):
        result = []
        for rule in rule_list:
            if filter == rule['input']:
                result.append(rule['output'])
        return result

    # sử dụng luật đưa ra kết quả
    def qualified(self, game, rule_list):
        form = {}
        form['gd'] = self.filter_gender(rule_list) or game.Genre
        form['it'] = self.filter(rule_list, self.interes) or game.Genre
        form['jb'] = self.filter(rule_list, self.job) or ["Mất phí", "Miễn phí"]
        form['pp'] = self.filter(rule_list, self.purpose) or game.Genre

        if self.age <= 12:
            min_age = 0
            max_age = 12
        elif self.age <= 18:
            min_age = 13
            max_age = 18
        else:
            min_age = 19
            max_age = 100

        return (game.genre in form['pp'] or game.number_of_player in form['pp']) \
        and game.genre in form['gd'] \
        and game.price in form['jb'] \
        and (game.genre in form['it'] or game.number_of_player in form['it']) \
        and (min_age <= game.age and max_age >= game.age)