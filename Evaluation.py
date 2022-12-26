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

    # sử dụng luật đưa ra kết quả
    def qualified(self, game):
        form = {}
        if self.gender == 1:
            form['gd'] = ['Hành động', 'Nhập vai', 'Chiến thuật', 'Kinh dị', 'Mô phỏng', 'Phiêu lưu', 'Thể thao', 'Giải đố', 'Đối kháng', 'Đua xe', 'Giải trí', 'Bắn súng']
        else:
            form['gd'] = ['Giải trí', 'Mô phỏng', 'Âm nhạc', 'Giải đố', 'Thời trang', 'Nấu ăn']

        if self.interes == 'Công nghệ':
            form['it'] = ['Chiến thuật', 'Bắn súng', 'Mô phỏng']
        elif self.interes == 'Thể thao':
            form['it'] = ['Thể thao']
        elif self.interes == 'Du lịch':
            form['it'] = ['Phiêu lưu']
        elif self.interes == 'Âm nhạc':
            form['it'] = ['Âm nhạc']
        elif self.interes == 'Mạo hiểm':
            form['it'] = ['Hành động', 'Kinh dị', 'Phiêu lưu', 'Đua xe', 'Bắn súng']
        elif self.interes == 'Nghệ thuật':
            form['it'] = ['Nhập vai', 'Mô phỏng', 'Âm nhạc', 'Thời trang']
        elif self.interes == 'Giao tiếp':
            form['it-'] = ['Đồng đội nhiều người']

        form['gr'] = [i for i in form['gd'] if i in form['it']]

        return game.genre in form['gr']