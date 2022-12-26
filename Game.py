NO_INFORMATION = 'chưa có thông tin'

class Game:
    games = []
    # set tương tự oject, tạo 1 đối tượng
    # Nền tảng
    Platform = set()
    # thể loại
    Genre = set()
    # Năm phát hành
    YearOfRelease = set()
    # Độ tuổi
    Age = set()
    
    # hàm khởi tạo đối tương trong python (__init__)
    def __init__(self, data):
        # Khởi tạo đối tượng
        # Dữ liệu bị thiếu được thay thế bằng chuỗi no_record
        self.name = data.Name
        self.platform = data.Platform
        self.year_of_release = int(data.Year_of_Release) 
        self.genre = data.Genre
        self.publisher = data.Publisher
        self.rating = int(data.Rating)
        self.age = int(data.Ages)

        try:
            self.developer = data.Developer
        except ValueError:
            self.developer = NO_INFORMATION

        self.price = data.Price
        self.number_of_player = data.Number_of_players

        # ghi loại trò chơi
        Game.Platform.add(self.platform)
        Game.Genre.add(self.genre)
        Game.YearOfRelease.add(int(self.year_of_release))
        Game.Age.add(self.age)
        Game.games.append(self)

    # In ra các loại trò chơi của các tệp dữ liệu được thu thập thông tin
    @ classmethod
    def show_genre(self):
        print(len(self.Genre), ' genres in total: ', self.Genre)
        
    # Có những nền tảng trò chơi nào để in ra các tệp dữ liệu đã thu thập thông tin?
    @ classmethod
    def show_platform(self):
        print(len(self.Platform), ' platforms in total: ', self.Platform)
