import pris3
from pris3.running import process_command

def main():
    # 直接传入命令，无需等待用户输入
    process_command("obtain facial expressions")
    process_command("render depth map")
    process_command("generate facial animation")
    
if __name__ == '__main__':
    main()
