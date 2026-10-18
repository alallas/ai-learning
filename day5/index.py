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

