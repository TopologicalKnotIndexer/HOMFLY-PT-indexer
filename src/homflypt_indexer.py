# 根据 PD_CODE 确定 HOMFLY-PT 多项式
# 再根据 HOMFLY-PT 多项式 确定扭结名称

from get_homflypt_by_pd_code  import get_homflypt_by_pd_code
from get_knotname_by_homflypt import get_knotname_by_homflypt

def homflypt_indexer(pd_code: list) -> list[str]: # 给定 PD_CODE，确定扭结名称
    khovanov = get_homflypt_by_pd_code(pd_code)
    knotname_list = get_knotname_by_homflypt(khovanov)
    return knotname_list

if __name__ == "__main__": # 测试
    print(homflypt_indexer([[2, 8, 3, 7], [4, 10, 5, 9], [6, 2, 7, 1], [8, 4, 9, 3], [10, 6, 1, 5]]))