from b_down_file import b_single_part
from b_down_file import b_more_part


def main():
    while True:
        print('*'*50)
        print('欢迎使用B站视频下载工具~')
        choice_list = ['单P下载输入: 1', '多P下载输入: 2', '退出输入: exit']
        for choice in choice_list:
            print(choice)
        print('*'*50)
        choice = input('请输入:')
        print('*'*50)
        if choice == '1':
            b_single_part.main()
        elif choice == '2':
            b_more_part.main()
        elif choice == 'exit':
            break
            

if __name__ == '__main__':
    main()
