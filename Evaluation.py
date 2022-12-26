NORECORD = 'chưa có thông tin'

class Evaluation():
    def __init__(self, args):
        self.platform = args['pf']
        self.genre = args['ge']
        self.lb = args['lb']
        self.rb = args['rb']
        self.age = args['age']
        self.allowed_rating = args['ar']

    # các lựa chọn của người dùng
    def print_rule(self):
        print('【RULE】',self.platform, self.genre, self.lb, self.rb, self.age)

    # sử dụng luật đưa ra kết quả
    def qualified(self, game):
        form = {}
        if self.platform == 'Tất cả nền tảng':
            form['pf'] = True
        else:
            form['pf'] = self.platform

        if self.genre == 'Tất cả thể loại':
            form['ge'] = True
        else:
            form['ge'] = self.genre

        return (game.platform == form['pf'] or bool(game.platform) == form['pf']) \
            and (game.genre == form['ge'] or bool(game.genre) == form['ge']) \
            and (game.year_of_release == NORECORD or game.year_of_release >= self.lb and game.year_of_release <= self.rb)\
            and game.age <= self.age \
            and game.rating in self.allowed_rating