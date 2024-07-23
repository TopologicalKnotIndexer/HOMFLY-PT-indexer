# 这里不是简单的桥接
# 要用 slow_dict_reader 去读 HOMFLY-PT-polynomial-list 中的数据
import os
DIRNOW = os.path.dirname(os.path.abspath(__file__))
SUBDIR = os.path.join(DIRNOW, "slow_dict_reader", "src") # 子包路径
HOMDMP = os.path.join(DIRNOW, "HOMFLY-PT-polynomial-list", "data", "sorted_HOMFLY-PT.txt")
assert os.path.isfile(HOMDMP) # 验证数据文件存在性

# ======================================== BEGIN IMPORT FROM PATH ======================================== #
import importlib
import json
import sys
def load_module_from_path(path: str, mod_name: str): # 从指定路径导入一个包
    assert os.path.isdir(path)                       # 路径必须存在
    path         = os.path.abspath(path)             # 获得绝对路径
    old_sys_path = json.loads(json.dumps(sys.path))  # 存档旧的 sys.path
    sys.path     = [path] + sys.path                 # 将新的路径加入 sys.path
    mod          = importlib.import_module(mod_name) # 加载指定的包
    sys.path     = old_sys_path                      # 恢复旧的 sys.path
    return mod
# ======================================== END IMPORT FROM PATH ======================================== #

def get_knotname_by_homflypt(homflypt: str) -> list:
    homflypt = homflypt.strip()
    dic = load_module_from_path(SUBDIR, "slow_dict_reader").slow_dict_reader(HOMDMP)
    if dic.get(homflypt) is None: # 没有找到相应的扭结名称
        return []
    return dic[homflypt] # 找到了相应的扭结名称

if __name__ == "__main__": # 测试
    print(get_knotname_by_homflypt("-L^6*M^2 + L^4*M^4 + 2*L^6 - 4*L^4*M^2 + 3*L^4"))