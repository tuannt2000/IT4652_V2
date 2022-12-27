NORECORD = 'chưa có thông tin'

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

    def filter_gender(self):
        result = []
        if self.gender == 1:
            result = ['Hành động', 'Nhập vai', 'Chiến thuật', 'Kinh dị', 'Mô phỏng', 'Phiêu lưu', 'Thể thao', 'Giải đố', 'Đối kháng', 'Đua xe', 'Giải trí', 'Bắn súng']
        elif self.gender == 2:
            result = ['Giải trí', 'Mô phỏng', 'Âm nhạc', 'Giải đố', 'Thời trang', 'Nấu ăn']
        return result
    
    def filter_interes(self):
        if self.interes == 'Công nghệ':
            result = ['Chiến thuật', 'Bắn súng', 'Mô phỏng']
        elif self.interes == 'Du lịch':
            result = ['Phiêu lưu']
        elif self.interes == 'Mạo hiểm':
            result = ['Hành động', 'Kinh dị', 'Phiêu lưu', 'Đua xe', 'Bắn súng']
        elif self.interes == 'Mua sắm':
            result = ['Thời trang']
        elif self.interes == 'Nấu ăn':
            result = ['Nấu ăn']
        elif self.interes == 'Nghệ thuật':
            result = ['Nhập vai', 'Mô phỏng', 'Âm nhạc', 'Thời trang']
        elif self.interes == 'Giao tiếp':
            result = ['Đồng đội nhiều người']
        else:
            result = [self.interes]
        return result

    # sử dụng luật đưa ra kết quả
    def qualified(self, game):
        form = {}
        form['gd'] = self.filter_gender() or game.Genre
        form['it'] = self.filter_interes()

        return game.genre in form['gd'] \
        and (game.genre in form['it'] or game.number_of_player in form['it'])