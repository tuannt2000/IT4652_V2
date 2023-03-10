import os
import time
from time import sleep
from tkinter import Label, Frame, Button, Checkbutton, Tk, IntVar, filedialog, Radiobutton, ttk, Scale, HORIZONTAL
from Game import Game
from ActionData import ActionData
from Search import Search
from Rule import Rule
from Evaluation import Evaluation

# Một danh sách các intVars được liên kết với chín xếp hạng khác nhau. Khi nó là 1, điều đó có nghĩa là nó đã được chọn
intVar = []
# Bản ghi thứ n hiện đang được hiển thị, có thể được chuyển đổi bằng nút
selection = 0
# Lưu tất cả các bản ghi trò chơi trong cơ sở dữ liệu
game_list = []
# Trò chơi đáp ứng tiêu chí tìm kiếm của người dùng
rating_list =  [5, 4, 3, 2, 1]
# nghề nghiệp
job_list = ['Học sinh - sinh viên', 'Người đi làm']
# sở thích
interest_list = ['Công nghệ', 'Thể thao', 'Du lịch', 'Âm nhạc', 'Mạo hiểm', 'Nghệ thuật', 'Giao tiếp', 'Nấu ăn', 'Mua sắm']
# mục đích
purpose_list = ['Giải trí', 'Kết bạn', 'Học tập', 'Tăng kỹ năng']


# [Gọi phương thức lớp ActionData] Thay đổi nội dung hiển thị giao diện người dùng theo tương tác của người dùng
# Phương thức WHEN CHANGED kích hoạt goto_prev_property và goto_next_property
def switch_property(direction):
    if direction == 'prev':
        message = action_data_agent.goto_prev_property()
    else:
        message = action_data_agent.goto_next_property()
    result_message['text'] = message

def switch_property_suggest(direction):
    if direction == 'prev':
        message = action_data_agent.goto_prev_property()
    else:
        message = action_data_agent.goto_next_property()
    result_suggest_message['text'] = message

# [Daemon] Duyệt qua hàng đợi game_list để tìm các phiên bản đủ điều kiện theo điều kiện truy xuất của người dùng
# Liên kết các thành phần giao diện với daemon và xóa các phiên bản không phù hợp
# Lưu trữ các phiên bản đủ điều kiện trong ActionData.properties
def properties_filter():
    # Nhận các điều kiện truy vấn do người dùng chọn trong giao diện từ mỗi thành phần
    ActionData.properties.clear()
    
    args = {'pf': platform_select.get(),
            'ge': genre_select.get(),
            'lb': int(from_year_select.get()),
            'rb': int(to_year_select.get()),
            'age': int(ages_select.get())
            }
    allowed_rating = []
    for idx in range(len(intVar)):
        if intVar[idx].get():
            allowed_rating.append(rating_list[idx])
    args['ar'] = allowed_rating
    evaluate = Search(args)
    evaluate.print_rule()

    for game in game_list:
        if evaluate.qualified(game):
            ActionData.properties.append(game)
    
    # Kết quả lựa chọn thiết bị đầu cuối đáp ứng yêu cầu của người dùng
    print('【RESULT】', len(ActionData.properties))
    # Sắp xếp kết quả tìm kiếm theo năm theo thứ tự ngược lại
    ActionData.properties = sorted(ActionData.properties, key=lambda game: game.year_of_release if type(game.year_of_release) == int else -1, reverse=True)
    # Hiển thị bản ghi đầu tiên phù hợp với yêu cầu của người dùng trong cửa sổ
    # Cho dù số lượng kết quả kiểm tra là> 0
    if len(ActionData.properties):
        ActionData.selection = 0
        result_message['text'] = action_data_agent.change_display()
    else:
        result_message['text'] = 'Không có trò chơi phù hợp nào trong cơ sở dữ liệu'

def properties_filter_suggest():
    # Nhận các điều kiện truy vấn do người dùng chọn trong giao diện từ mỗi thành phần
    ActionData.properties.clear()
    
    args = {'jb': job_select.get(),
            'gd': int(radio.get()) or 0,
            'it': interes_select.get(),
            'pp': purpose_select.get(),
            'age': int(age_scale.get())
            }

    evaluate = Evaluation(args)
    evaluate.print_rule()
    for game in game_list:
        if evaluate.qualified(game, rule_list):
            ActionData.properties.append(game)

    # Kết quả lựa chọn thiết bị đầu cuối đáp ứng yêu cầu của người dùng
    print('【RESULT】', len(ActionData.properties))
    # Sắp xếp kết quả tìm kiếm theo năm theo thứ tự ngược lại
    ActionData.properties = sorted(ActionData.properties, key=lambda game: game.year_of_release if type(game.year_of_release) == int else -1, reverse=True)
    # Hiển thị bản ghi đầu tiên phù hợp với yêu cầu của người dùng trong cửa sổ
    # Cho dù số lượng kết quả kiểm tra là> 0
    if len(ActionData.properties):
        ActionData.selection = 0
        result_suggest_message['text'] = action_data_agent.change_display()
    else:
        result_suggest_message['text'] = 'Không có trò chơi phù hợp nào trong cơ sở dữ liệu'

def switch_suggest_screen():
    search_screen.pack_forget()
    suggest_screen.pack()

def switch_search_screen():
    search_screen.pack()
    suggest_screen.pack_forget()

if __name__ == '__main__':

    window = Tk()
    window.title("Play-Smart.expertsystem")
    window.geometry('1150x740')
    window.iconbitmap('./logo.ico')
    window.resizable(width=False, height=False)

    search_screen = Frame(window)
    suggest_screen = Frame(window)

    # Thông tin trò chơi được đề xuất được đặt ở hàng thứ 0 và hàng đầu tiên cho người dùng
    message = Label(search_screen, text='[Tìm kiếm game phù hợp]', font=('Microsoft YaHei', 18))
    result_window = Frame(search_screen, width=1024, height=180)
    # Giữ kích thước cửa sổ không thay đổi
    result_window.propagate(0)
    message.grid(row=0, columnspan=5)
    result_message = Label(result_window, text='Chưa có nội dung được đề xuất')
    result_message.pack()
    result_window.grid(row=1, columnspan=5)

    # Di chuyển đến màn hình suggest
    suggest_btn = Button(search_screen, text='Gợi ý', command=lambda:switch_suggest_screen())
    suggest_btn.grid(row=0, column=3, sticky='e', ipadx=20, pady=30)

    # Hàng thứ hai đặt nút, khi có nhiều thông tin được đề xuất, hãy sử dụng nút để chuyển
    prev_btn = Button(search_screen, text='Trước', command=lambda:switch_property('prev'))
    next_btn = Button(search_screen, text='Tiếp theo', command=lambda:switch_property('next'))
    prev_btn.grid(row=2, column=3, sticky='e', ipadx=20, pady=30)
    next_btn.grid(row=2, column=4, ipadx=20)

    # Dòng thứ ba được sử dụng để chọn nền tảng và loại trò chơi của trò chơi
    platform_label = Label(search_screen, text='Nền tảng', font=('tMicrosoft YaHei',12,'bold'))
    genre_label = Label(search_screen, text='Thể loại', font=('tMicrosoft YaHei',12,'bold'))
    platform_select = ttk.Combobox(search_screen)
    genre_select = ttk.Combobox(search_screen)
    platform_label.grid(row=3, column=0)
    platform_select.grid(row=3, column=1)
    genre_label.grid(row=3, column=2)
    genre_select.grid(row=3, column=3)

    # Dòng thứ tư, chọn khoảng thời gian phát hành trò chơi
    time_range_labelA = Label(search_screen, text='Thời gian phát hành từ', font=('tMicrosoft YaHei',12,'bold'))
    time_range_labelB = Label(search_screen, text='Thời gian phát hành đến', font=('tMicrosoft YaHei',12,'bold'))
    from_year_select = ttk.Combobox(search_screen)
    to_year_select = ttk.Combobox(search_screen)
    time_range_labelA.grid(row=4, column=0)
    time_range_labelB.grid(row=4, column=2)
    from_year_select.grid(row=4, column=1)
    to_year_select.grid(row=4, column=3)

    # độ tuổi
    ages = Label(search_screen, text='Tuổi', font=('tMicrosoft YaHei',12,'bold'))
    ages_select = ttk.Combobox(search_screen)
    ages.grid(row=5, column=0)
    ages_select.grid(row=5, column=1)

    # Dòng thứ sáu, xác nhận để gửi các yêu cầu về chỉ số trò chơi đã chọn
    submit_btn = Button(search_screen, text='Tìm kiếm', font=('Microsoft YaHei', 15), command=properties_filter)
    submit_btn.grid(row=6, column=2, ipadx=70, ipady=10, pady=10)

    # Cột ngoài cùng bên phải đặt danh sách Nhóm để chọn xếp hạng trò chơi
    rating_frame = Frame(search_screen)
    rating_frame.grid(row=3, column=4, rowspan=3)
    rating_note_label = Label(rating_frame, text='Xếp hạng trò chơi', font=('tMicrosoft YaHei',12,'bold'))
    rating_note_label.pack()
    for idx in range(len(rating_list)):
        intVar.append(IntVar(value=1))
        check = Checkbutton(rating_frame, text=rating_list[idx], variable=intVar[idx], onvalue=1, offvalue=0)
        check.pack(side='top', expand='yes', fill='both')
    
    # [Tải thuộc tính] Tải tệp csv sau khi tải giao diện người dùng
    # Tạo đối tượng ActionData action_data_agent
    # Kích hoạt KHI When_change để khởi tạo tất cả các bản ghi trong cơ sở dữ liệu
    print('SYSTEM: Đang chọn tải tệp CSV')
    print('SYSTEM: Thư mục hiện tại', os.getcwd())
    try:
        result_message['text'] = 'Tải dữ liệu...'
        csv_filepath = filedialog.askopenfilename(initialdir=os.getcwd(), title='Chọn tệp csv')
        start = time.time()
        print('SYSTEM: Tệp csv đang tải...')
        action_data_agent = ActionData()
        rule_data_agent = Rule()
        game_list = action_data_agent.load_properties(csv_filepath)
        rule_list = rule_data_agent.load_properties('rule.txt')
        counter = round(time.time() - start, 2)
        result_message['text'] = 'Dữ liệu được tải, mất thời gian{}s, Chưa có nội dung được đề xuất'.format(counter)
        print('SYSTEM: Tệp csv đã được tải, mất thời gian{}s'.format(counter))
    except Exception:
        print('ERROR: Không tải được tệp CSV')
        window.destroy()
        sleep(1)
        exit()

    # Tải nội dung của menu thả xuống trên trang chủ theo dữ liệu
    platform_select['value'] = ['Tất cả nền tảng'] + sorted(Game.Platform)
    genre_select['value'] = ['Tất cả thể loại'] + sorted(Game.Genre)
    from_year_select['value'] = list(Game.YearOfRelease)
    to_year_select['value'] = list(Game.YearOfRelease)
    ages_select['value'] = sorted(Game.Age)
    platform_select.current(0)
    genre_select.current(0)
    from_year_select.current(0)
    to_year_select.current(len(Game.YearOfRelease) - 1)
    ages_select.current(0)

    # Hiển thị màn hình tìm kiếm
    search_screen.pack()


    ########################################################################
    # Thông tin trò chơi được đề xuất được đặt ở hàng thứ 0 và hàng đầu tiên cho người dùng
    message_suggest = Label(suggest_screen, text='[Gợi ý game phù hợp]', font=('Microsoft YaHei', 18))
    result_suggest = Frame(suggest_screen, width=1024, height=180)
    # Giữ kích thước cửa sổ không thay đổi
    result_suggest.propagate(0)
    message_suggest.grid(row=0, columnspan=5)
    result_suggest_message = Label(result_suggest, text='Chưa có nội dung được đề xuất')
    result_suggest_message.pack()
    result_suggest.grid(row=1, columnspan=5)

    # Hàng thứ hai đặt nút, khi có nhiều thông tin được đề xuất, hãy sử dụng nút để chuyển
    prev_suggest_btn = Button(suggest_screen, text='Trước', command=lambda:switch_property_suggest('prev'))
    next_suggest_btn = Button(suggest_screen, text='Tiếp theo', command=lambda:switch_property_suggest('next'))
    prev_suggest_btn.grid(row=2, column=3, sticky='e', ipadx=20, pady=30)
    next_suggest_btn.grid(row=2, column=4, ipadx=20)

    # Di chuyển đến màn hình search
    search_btn = Button(suggest_screen, text='Tìm kiếm', command=lambda:switch_search_screen())
    search_btn.grid(row=0, column=3, sticky='e', ipadx=20, pady=30)

    # Dòng thứ tư được sử dụng để chọn nghề nghiệp và giới tính
    job_label = Label(suggest_screen, text='Nghề nghiệp', font=('tMicrosoft YaHei',12,'bold'))
    job_select = ttk.Combobox(suggest_screen)
    job_label.grid(row=4, column=0, ipady=15)
    job_select.grid(row=4, column=1)
    radio = IntVar()  
    gender_label = Label(suggest_screen, text='Giới tính', font=('tMicrosoft YaHei',12,'bold'))
    gender_label.grid(row=4, column=2, ipady=15)
    male_radio = Radiobutton(suggest_screen, text="Nam", variable=radio, value=1)
    female_radio = Radiobutton(suggest_screen, text="Nữ", variable=radio, value=2)
    male_radio.grid(row=4, column=3)
    female_radio.grid(row=4, column=4)

    # Dòng thứ năm được sử dụng để chọn sở thích và mục đích chơi
    interes_label = Label(suggest_screen, text='Sở thích', font=('tMicrosoft YaHei',12,'bold'))
    interes_select = ttk.Combobox(suggest_screen)
    interes_label.grid(row=5, column=0, ipady=15)
    interes_select.grid(row=5, column=1)
    purpose_label = Label(suggest_screen, text='Mục đích chơi game', font=('tMicrosoft YaHei',12,'bold'))
    purpose_select = ttk.Combobox(suggest_screen)
    purpose_label.grid(row=5, column=2, ipady=15)
    purpose_select.grid(row=5, column=3)
    # Dòng thứ sáu được sử dụng để chọn tuổi
    age_scale = Scale(suggest_screen, label='Tuổi', font=('tMicrosoft YaHei',12,'bold'), from_=list(Game.Age)[0], to=list(Game.Age)[len(Game.Age) - 1], orient=HORIZONTAL,
             length=400, showvalue=1, tickinterval=10, resolution=1)
    age_scale.grid(row=6, column=0, columnspan=2, ipady=15,)

    # Dòng thứ sáu, xác nhận để gửi các yêu cầu về chỉ số trò chơi đã chọn
    submit_suggest_btn = Button(suggest_screen, text='Gợi ý', font=('Microsoft YaHei', 15), command=properties_filter_suggest)
    submit_suggest_btn.grid(row=7, column=2, ipadx=70, ipady=10, pady=10)

    # Tải nội dung của menu thả xuống trên trang chủ theo dữ liệu
    job_select['value'] = [' '] + sorted(job_list)
    interes_select['value'] = [' '] + sorted(interest_list)
    purpose_select['value'] = [' '] + sorted(purpose_list)
    # radio.set(1)
    job_select.current(0)
    interes_select.current(0)
    purpose_select.current(0)


    # Được sử dụng cho các loại thuộc tính cụ thể và nội dung cụ thể trong các bảng đầu ra ban đầu
    Game.show_genre()
    Game.show_platform()

    window.mainloop()