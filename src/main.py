# 从标准输入流输入一个 PD_CODE
# 输出可能与之对应的扭结的名称序列（每行一个），找不到相应的扭结则什么都不输出

import sys
from homflypt_indexer import homflypt_indexer

def main():
    pd_code = eval(sys.stdin.read())
    for knotname in homflypt_indexer(pd_code):
        print(knotname)

if __name__ == "__main__":
    main()