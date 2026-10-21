import numpy as np
import matplotlib.pyplot as plt

def get_M_Map(w, h, maxit=20, r=2):
    # 此时的xy表示两个方向上的底图的像素点的坐标，一维数组
    x = np.linspace(-2.5, 1.5, 4*w+1)
    y = np.linspace(-1.5, 1.5, 3*h+1)

    # meshgrid相当于把一维的东西变为二维的，显示利用广播规则进行扩展。
    # 对于x， 变成（None, :）, 也就是1行xx列， [[1, 2, 3, ...]]
    # 对于y， 变成（:, None）, 也就是xx行1列， [[1], [2], [3], ...]
    # 然后让x沿着行方向（因为要把1行扩展成多行）复制， 让y沿着列方向（因为要把1列扩展成多列）复制

    # 此时得到的A， B都是二维数组，分别是横坐标和纵坐标，用于计算得到一个复数的坐标点
    A, B = np.meshgrid(x, y)

    # 相当于C = x[None, :] + y[:, None]*1j
    # 不能直接c = x + y*1j，因为x和y是一维数组，出来的c也是一维数组，无法表达一个面，只能表达一个对角线
    # B 的每个元素（y轴作为虚部，x轴作为实部）乘以虚数单位 j，从"实数 y"变成"纯虚数 yi"
    # 这样C就是复数的类型，complex128
    C = A + B*1j

    z = np.zeros_like(C)
    # 记录离散的循环轮数，只需要记录第一次的离散的那些，因为一个坐标可能在循环内离散多次，只有第一次有意义
    # divided = maxit + np.zeros(z.shape, dtype=np.int_)
    divided = np.full(C.shape, maxit, dtype=np.int_)

    for i in range(maxit):
        # 执行核心公式
        z = z ** 2 + C
        # 判断数是否离散，数字是否大于r，大于就是离散
        is_lisan = abs(z) > r
        # 判断是不是第一次离散， 本次是离散，并且之前的divided没有被赋值，还是初始值
        # 不能用0来作为初始化，因为无法区分【第0次循环离散】【没有离散过】
        is_first_lisan = is_lisan & (divided == maxit)

        # 记录第一次离散的循环轮数
        divided[is_first_lisan] = i
        # 让已经离散的坐标记录为r，防止数字爆炸（已经离散过的已经被记录了，是没有意义的）
        z[is_lisan] = r
    return divided


def main():
    plt.clf()
    data = get_M_Map(100, 100)
    plt.imshow(data, cmap="hot", origin="lower")
    plt.title("Mandelbrot Set")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    main()



