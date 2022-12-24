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
    # Giới tính
    Gender = set()
    # Độ tuổi
    Age = set()
    
    # hàm khởi tạo đối tương trong python (__init__)
    def __init__(self, data):
        # Khởi tạo đối tượng
        # Dữ liệu bị thiếu được thay thế bằng chuỗi no_record
        self.name = data.Name
        self.platform = data.Platform
        try:
            self.year_of_release = int(data.Year_of_Release) 
        except ValueError:
            self.year_of_release = NO_INFORMATION
        
        self.genre = data.Genre
        self.publisher = data.Publisher
        self.rating = data.Rating
        self.gender = data.Gender
        self.age = data.Ages
        # ghi loại trò chơi
        Game.Platform.add(self.platform)
        # Tránh các loại trò chơi NaN trong menu thả xuống
        if self.genre != NO_INFORMATION:
            Game.Genre.add(self.genre)
        if self.year_of_release != NO_INFORMATION:
            Game.YearOfRelease.add(int(self.year_of_release))

        Game.Gender.add(self.gender)
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
