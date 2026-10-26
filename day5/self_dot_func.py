import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = np.array([[1, 2, 3, 4, ], [5, 6, 7, 8, ]])
d = np.array([0, 1, 2, 3])
e = np.array([[0, 1,], [2, 3] , [4, 5,] ,[6, 7, ]])

print(a.shape, b.shape, c.shape, d.shape, e.shape)

# 向量 × 向量 → 标量
print(np.dot(a, b) ) # 32

# 矩阵 × 向量 → 向量
print(np.dot(c, d)) # [20 44]

# c = [[1, 2, 3, 4],
#      [5, 6, 7, 8]]
# d = [0, 1, 2, 3]

# 第0行: 1×0 + 2×1 + 3×2 + 4×3 = 0+2+6+12  = 20
# 第1行: 5×0 + 6×1 + 7×2 + 8×3 = 0+6+14+24 = 44

print('---------------------', np.dot(c, e))


def ndim1_sum(a1, a2):
    sum = 0
    for v1, v2 in zip(a1, a2):
        sum = sum + (v1 * v2)
    return sum


def self_dot(a1, a2):
    # 排除其他类型，只允许数组类型
    if (a1.ndim ==1 and a2.ndim ==1):
        return ndim1_sum(a1, a2)
    elif ((a1.ndim ==1 and a2.ndim ==2) or (a1.ndim ==2 and a2.ndim ==1)):
        if (a1.shape[1] != a2.shape[0]):
            return
        two_array = a2
        one_array = a1
        if (a1.ndim == 2 ):
            two_array = a1
            one_array = a2
        res = []
        for i, v in two_array:
            res.append(ndim1_sum(v, one_array))
        return res
    elif a1.ndim == 2 and a2.ndim == 2:
        if (a1.shape[1] != a2.shape[0]):
            return
        # a1 = np.array([[1, 2, 3, 4, ], [5, 6, 7, 8, ]])
        # a2 = np.array([[0, 1,], [2, 3] , [4, 5,] ,[6, 7, ]])
        res = []
        for row in a1:  # 遍历直接拿行
            res_row = []
            for col_ind in range(a2.shape[1]): # 遍历拿索引
                # 取所有行，分别的每一个列
                a2_cur = a2[:, col_ind]
                res_row.append(ndim1_sum(row, a2_cur)) 
            res.push(res_row) # 最后拼形状
        return res




#  ● np.dot 内部不是普通循环                                                     
                                                                               
#    简短回答：NumPy 自己根本不写"逐元素相乘再求和"的循环，对 float64 的二维数组 
#    ，它直接把活外包给底层的 BLAS 线性代数库（NumPy 安装时自带的 OpenBLAS，或   
#    Intel MKL / macOS Accelerate），调用其中专门做矩阵乘法的例程 dgemm。        
                                                                               
#    调用链                                                                      
                                                                               
#    ```                                                                         
#      np.dot(a, b)                                                              
#        → C 层 array_dot                                                        
#        → PyArray_MatrixProduct                                                 
#        → cblas_matrixproduct  (numpy/_core/src/multiarray/cblasfuncs.c)        
#        → cblas_dgemm          (BLAS 库)                                        
#        → OpenBLAS/MKL 的优化 kernel                                            
#    ```                                                                         
                                                                               
#    dgemm 做的事情本质就是教科书公式 C[i][j] = Σ A[i][k]·B[k][j]——是循环，但绝不
#    是"普通的循环"。以 OpenBLAS 为例，它在这个三重循环上叠了五层优化：          
                                                                               
#    1. 分块（blocking）：把大矩阵切成适合 CPU 各级缓存的小块（比如 128×128、    
#       64×64），让内层循环的数据都留在 cache 里，避免频繁访问内存（内存比 CPU 慢
#       两个数量级，这才是朴素实现慢的主因）。                                   
#    2. 数据打包（packing）：把要计算的小块按 kernel 需要的顺序重排到连续内存中  
#       ，CPU 可以顺序流式读取。                                                 
#    3. SIMD 向量化：用 AVX2/AVX-512 的 FMA（乘加融合）指令，一条指令同时算 4~8  
#       个 double 的乘加。                                                       
#    4. 手写汇编微内核：针对具体 CPU 架构（Haswell、Skylake、Zen 各有专门版本）有
#       手工调优的汇编 kernel，寄存器分配、指令流水都安排好了。                  
#    5. 多线程：OpenBLAS/MKL 会自动把大矩阵按列块拆给多个核并行。                
                                                                               
#    所以算法复杂度还是 O(n³)，但常数项被压到了极致。                            
                                                                               
#    实测对比                                                                    
                                                                               
#    我刚在你机器上跑了 200×200 的矩阵乘法：                                     
                                                                               
#    ```                                                                         
#      np.dot  : 0.033 ms                                                        
#      Python 三重循环: 5.09 s    ← 差约 155 倍                                  
#    ```                                                                         
                                                                               
#    这 155 倍还是被纯 Python 的解释器开销拉低了的数字；n 再大些差距会到几千倍。 
                                                                               
#    什么时候 NumPy 会退回"普通循环"                                             
                                                                               
#    只有一种常见情况：输入不是数值类型（比如 dtype=object 的数组），BLAS 用不了 
#    ，NumPy 才走自己通用的 C 循环逐元素算。另外，如果你的数组内存不连续（比如大 
#    切片 a[::2]），它会先 copy 成连续数组再交给 BLAS，而不是用慢循环硬算。      
                                                                               
#    顺便说，你的 day5/self_dot_func.py 里那个 self_dot 就是朴素循环思路——正好和 
#    np.dot 形成对照：你写的版本是"按语义直译公式"，np.dot 是"把公式喂给做了几十 
#    年优化的工业级库"。                                          



# 为啥a[::2]的内存不连续

#  ● 因为切片是"视图"，跳过的数据在内存里还留在原地                              
                                                                               
#    先看内存里到底存的是什么                                                    
                                                                               
#    二维数组只是"看上去"是二维的，物理内存里其实是一维平铺的，按行依次排（叫 C  
#    连续 / 行优先）：                                                           
                                                                               
#    ```                                                                         
#      a 的内存:  [0 1 2 3][4 5 6 7][8 9 10 11]   ← 一整块连续空间               
#    ```                                                                         
                                                                               
#    每个 float64 占 8 字节，一行 4 个 = 32 字节，所以实验里 a.strides = (32,    
#    8)：往下一行走地址 +32，往右一格 +8。strides 刚好等于"紧凑排布该有的距离"， 
#    所以是连续的。                                                              
                                                                               
#    切片为什么不连续                                                            
                                                                               
#    a[::2] 取第 0、2 行。关键：NumPy 不会把选中的 8 个数复制到新内存，它只是改一
#    下视图的描述信息（shape 和 strides），数据还躺在原数组的缓冲区里——实验里    
#    np.shares_memory 返回 True， strides 从 (32, 8) 变成 (64, 8)：往下一行要跳过
#    2 行 = 64 字节。                                                            
                                                                               
#    于是视图的 8 个数在物理上散在 12 个槽位里，中间留着被跳过的第 1 行：        
                                                                               
#    ```                                                                         
#      a 的内存:    [0 1 2 3][4 5 6 7][8 9 10 11]                                
#      a[::2] 要的: [0 1 2 3]        [8 9 10 11]                                 
#                          ↑ 洞：被跳过的 [4..7] 物理上还在原地，只是视图假装看不
#    见                                                                          
#    ```                                                                         
                                                                               
#    这就是"内存不连续"的含义：数据块中间有洞，不是严丝合缝的一整块。a[:, ::2] 更
#    彻底——行内都不连续了（strides 第二维变成 16，连相邻两列中间都有洞）。       
                                                                               
#    为什么 BLAS 在乎这个                                                        
                                                                               
#    BLAS 定位元素只靠一个公式：基地址 + i×行距 + j×列距，它假设矩阵是紧密排布的 
#    一整块。把带洞的视图指针直接塞给它，它会按"第 0 行后面紧跟第 1 行"去读——读出
#    来的全是错位的数据（把 4 5 6 7 当成第二行）。所以 NumPy 只好先 copy 一份连续
#    的副本，再把副本交给 BLAS。                                                 
                                                                               
#    一个反直觉的点                                                              
                                                                               
#    不是所有切片都不连续。a[:2]（从头取前 2 行）就是连续的，因为它取的是内存前缀
#    ，一个洞都没留。判断标准从来不是"有没有切片"，而是 strides 是否恰好等于紧凑 
#    布局的距离——a[::2] 的洞让行距翻倍，破坏了这一点。                           
 

