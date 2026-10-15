
# 得到前20项的斐波那契数列

n1 = 0
n2 = 1

res = [n1, n2]

for i in range(18):
    n = n1 + n2
    res.append(n)
    n1 = n2
    n2 = n


# 更加简洁的写法

res = [0, 1]

for _ in range(18):
    res.append(res[-1] + res[-2])


# 找1-100的素数

res = []
def is_prime (n) :
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

res = []
for i in range(1, 101):
    if  is_prime(i) :
        res.append(i)

# 优化版本，如果是合数，其中一个因数肯定小于根号n
# 遍历次数变为根号n次
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True
