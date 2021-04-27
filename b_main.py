from b_down_file import b_single_part
from b_down_file import b_more_part


def main():
    while True:
        print('*'*20)
        print('欢迎使用B站视频下载工具~')
        print('输入exit,退出程序')
        choice = input('单P下载，请输入1, 多P下载请输入2:')
        print('*'*20)
        if choice == '1':
            b_single_part.main()
        elif choice == '2':
            b_more_part.main()
        elif choice == 'exit':
            break
            

if __name__ == '__main__':
    main()
