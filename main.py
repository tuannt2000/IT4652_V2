import os
import time
from time import sleep
from tkinter import Label, Frame, Button, Checkbutton, Tk, IntVar, HORIZONTAL, Scale, filedialog
from tkinter import ttk
from Game import Game
from ActionData import ActionData
from Evaluation import Evaluation

# Một danh sách các intVars được liên kết với chín xếp hạng khác nhau. Khi nó là 1, điều đó có nghĩa là nó đã được chọn
intVar = []
# Bản ghi thứ n hiện đang được hiển thị, có thể được chuyển đổi bằng nút
selection = 0
# Lưu tất cả các bản ghi trò chơi trong cơ sở dữ liệu
game_list = []
# Trò chơi đáp ứng tiêu chí tìm kiếm của người dùng
rating_list =  [5, 4, 3, 2, 1]

# [Gọi phương thức lớp ActionData] Thay đổi nội dung hiển thị giao diện người dùng theo tương tác của người dùng
# Phương thức WHEN CHANGED kích hoạt goto_prev_property và goto_next_property
def switch_property(direction):
    if direction == 'prev':
        message = action_data_agent.goto_prev_property()
    else:
        message = action_data_agent.goto_next_property()
    result_message['text'] = message


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
            'gd': genders_select.get(),
            'age': int(ages_select.get())
            }
    allowed_rating = []
    for idx in range(len(intVar)):
        if intVar[idx].get():
            allowed_rating.append(rating_list[idx])
    args['ar'] = allowed_rating
    evaluate = Evaluation(args)
    evaluate.print_rule()

    for game in game_list:
        if evaluate.qualified(game):
            ActionData.properties.append(game)
            print(ActionData.properties)
    
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


if __name__ == '__main__':

    window = Tk()
    window.title("Play-Smart.expertsystem")
    window.geometry('1050x640')
    window.iconbitmap('./logo.ico')
    window.resizable(width=False, height=False)

    # Thông tin trò chơi được đề xuất được đặt ở hàng thứ 0 và hàng đầu tiên cho người dùng
    message = Label(window, text='[Gợi ý game phù hợp]', font=('Microsoft YaHei', 18))
    result_window = Frame(window, width=1024, height=180)
    # Giữ kích thước cửa sổ không thay đổi
    result_window.propagate(0)
    message.grid(row=0, columnspan=5)
    result_message = Label(result_window, text='Chưa có nội dung được đề xuất')
    result_message.pack()
    result_window.grid(row=1, columnspan=5)

    # Hàng thứ hai đặt nút, khi có nhiều thông tin được đề xuất, hãy sử dụng nút để chuyển
    prev_btn = Button(window, text='Trước', command=lambda:switch_property('prev'))
    next_btn = Button(window, text='Tiếp theo', command=lambda:switch_property('next'))
    prev_btn.grid(row=2, column=3, sticky='e', ipadx=20, pady=30)
    next_btn.grid(row=2, column=4, ipadx=20)

    # Dòng thứ ba được sử dụng để chọn nền tảng và loại trò chơi của trò chơi
    platform_label = Label(window, text='Nền tảng', font=('tMicrosoft YaHei',12,'bold'))
    genre_label = Label(window, text='Thể loại', font=('tMicrosoft YaHei',12,'bold'))
    platform_select = ttk.Combobox(window)
    genre_select = ttk.Combobox(window)
    platform_label.grid(row=3, column=0)
    platform_select.grid(row=3, column=1)
    genre_label.grid(row=3, column=2)
    genre_select.grid(row=3, column=3)

    # Dòng thứ tư, chọn khoảng thời gian phát hành trò chơi
    time_range_labelA = Label(window, text='Thời gian phát hành từ', font=('tMicrosoft YaHei',12,'bold'))
    time_range_labelB = Label(window, text='Thời gian phát hành đến', font=('tMicrosoft YaHei',12,'bold'))
    from_year_select = ttk.Combobox(window)
    to_year_select = ttk.Combobox(window)
    time_range_labelA.grid(row=4, column=0)
    time_range_labelB.grid(row=4, column=2)
    from_year_select.grid(row=4, column=1)
    to_year_select.grid(row=4, column=3)

    # Giới tính, độ tuổi
    genders = Label(window, text='Giới tính', font=('tMicrosoft YaHei',12,'bold'))
    ages = Label(window, text='Tuổi', font=('tMicrosoft YaHei',12,'bold'))
    genders_select = ttk.Combobox(window)
    ages_select = ttk.Combobox(window)
    genders.grid(row=5, column=0)
    ages.grid(row=5, column=2)
    genders_select.grid(row=5, column=1)
    ages_select.grid(row=5, column=3)

    # Dòng thứ sáu, xác nhận để gửi các yêu cầu về chỉ số trò chơi đã chọn
    submit_btn = Button(window, text='Gửi đi', font=('Microsoft YaHei', 15), command=properties_filter)
    submit_btn.grid(row=6, column=2, ipadx=70, ipady=10, pady=10)

    # Cột ngoài cùng bên phải đặt danh sách Nhóm để chọn xếp hạng trò chơi
    rating_frame = Frame(window)
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
        game_list = action_data_agent.load_properties(csv_filepath)
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
    genders_select['value'] = ['Cả nam và nữ'] + sorted(Game.Gender)
    ages_select['value'] = sorted(Game.Age)
    platform_select.current(0)
    genre_select.current(0)
    from_year_select.current(0)
    to_year_select.current(len(Game.YearOfRelease) - 1)
    genders_select.current(0)
    ages_select.current(0)

    # Được sử dụng cho các loại thuộc tính cụ thể và nội dung cụ thể trong các bảng đầu ra ban đầu
    Game.show_genre()
    Game.show_platform()

    window.mainloop()