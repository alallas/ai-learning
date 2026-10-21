import numpy as np

a = np.arange(15).reshape(3, 5)

print(a)

print(a.ndim, a.shape, a.size, a.dtype, a.itemsize, a.data)

print(type(a))

b = np.zeros([3, 5],dtype=np.int64 )
c = np.ones([2, 3, 4], dtype=np.int64)
d = np.empty([2, 3, 4])

print(b, c, d)

e = np.arange(0, 2, 0.3)

f = np.linspace(0, 2, 10)

print(e, f)

g = np.array([10, 20, 30, 40, 50])
h = np.array([1, 2, 3, 4, 5])

i = g - h

print(i)

A = np.array([[1, 1],
              [0, 1]])
B = np.array([[2, 0],
              [3, 4]])

j = A * B
k = A @ B

print(j, k)

rg = np.random.default_rng(1)
a1 = np.ones((2, 3), dtype=np.int_)
b1 = rg.random((2, 3))

b1 += a1

# 可以存入浮点数的b1
print('b1', b1)

# a1 += b1
# 不能从浮点数存入整数的数组
print('a1', a1)

c1 = np.arange(12).reshape(3, 4)

c1.sum()
print(c1.sum(axis=1))
print(c1.min(axis=1))
print(c1.max(axis=1))
print(c1.cumsum(axis=1))

# axis=0 表示"沿着行的方向移动，把沿途的元素加起来"，而不是"得到每一行的和"。


print('=============================')

d1 = np.arange(10)**3
print(d1, d1[2], d1[:], d1[2:5], d1[:6:2], d1[::-1])


def f(x, y):
    return 10 * x + y

e1 = np.fromfunction(f, (5, 4), dtype=np.int_)
print('=============================')
print(e1, e1[2, 3], e1[:, 1], e1[1:3, 1], e1[1:3, :])




f1 = np.arange(12).reshape(2, 2, 3)
print(f1)


g1 = np.floor(10* rg.random((3, 4)))

print('=============================')
print(g1, g1.ravel(), g1.ravel(order='F'), g1.reshape(2, 6), g1.T, )


h1 = 10 * rg.random((2, 2))
i1 = 10 * rg.random((2, 2))

print('=============================')
print(np.vstack((h1, i1)), np.hstack((h1, i1)))

j1 = np.array([2, 3, 4])
k1 = np.array([5, 6, 7])

print(np.column_stack((j1, k1)))

# 对于数字，r_就是把所有数字拼起来，成为一个数组
# 对于一维数组，r_就是vstack，c_就是column_stack
# 对于二维数组，r_就是vstack， c_就是hstack



