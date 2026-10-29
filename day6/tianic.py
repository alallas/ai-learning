import numpy as py
import pandas as pd


train_data = pd.read_csv('train.csv')
# print(train_data.head())

women = train_data.loc[train_data['Sex'] == 'female', 'Survived']

# print(women)

women_v2 = train_data.groupby("Sex")

# print(women_v2['Survived'].mean())





# 第一部分：热身（索引练习）

# **Q1.** 用 `loc` 选出 **所有女性乘客** 的 `Survived` 列，再算出女性存活率。
print(train_data.loc[train_data['Sex'] == 'female', 'Survived'].mean())

# **Q2.** 用 `loc` 选出 **Pclass == 1 且 Age > 50** 的乘客，看他们有多少人、存活了多少人
people = train_data.loc[(train_data['Pclass'] == 1) & (train_data['Age'] > 50)]
print(len(people), people['Survived'].sum())


# **Q3.** 用 `sort_values` 找出**票价最高的 5 位乘客**，打印他们的 Name、Pclass、Fare、Survived。
print(train_data.sort_values('Fare', ascending=False)[['Name', 'Pclass', 'Fare', 'Survived']].head(5))



## 第二部分：分组聚合（groupby）

# **Q4.** 用 `groupby` 计算**每个舱位等级（Pclass）的存活率**，并按存活率从高到低排序。
# （提示：对 0/1 列取 mean 就是比率）

a4 = train_data.groupby('Pclass')['Survived'].mean().sort_values(ascending=False)
print(a4)


# **Q5.** 用一次 `groupby` + `agg`，同时算出**每种性别**的：人数、存活人数、存活率、平均年龄。
# （提示：`.agg({'Survived': ['count', 'sum', 'mean'], ...})` 或者 named aggregation）

a5 = train_data.groupby('Sex').agg({'Survived': ['count', 'sum', 'mean'], 'Age':'mean'})
a5_v2 = train_data.groupby('Sex').agg(people_count=('Survived', 'count'), survived_count=('Survived', 'sum'), survived_rate=('Survived', 'mean'), mean_age=('Age', 'mean'))
print(a5,)


## 第三部分：透视表（pivot_table）

# **Q6.** 做一个透视表：**行 = Sex，列 = Pclass，值 = 存活率**。
# （提示：`pd.pivot_table(df, values=..., index=..., columns=..., aggfunc=...)`）
# values='Survived' —— 对哪一列算
# aggfunc='mean' —— 怎么算（默认就是 mean，不写也行）

a6 = pd.pivot_table(train_data, values='Survived', index='Sex', columns='Pclass', aggfunc='mean',  margins=True)
print(a6)



# **Q7.** 做一个透视表：**行 = Pclass，列 = Embarked，值 = 平均票价（Fare）**，并观察缺失值（NaN 出现在哪里？为什么？）。

a7 = pd.pivot_table(train_data, values='Fare', index='Pclass', columns='Embarked')
print(a7)



## 第四部分：缺失值处理（fillna / dropna）

# 先运行 `df.isna().sum()` 看看哪些列有缺失、缺多少。
print(train_data.isna().sum())

# **Q8.** Cabin 列缺失严重。创建一个**新列** `HasCabin`：有舱房号的记为 1，缺失的记为 0（用 `fillna` 或 `notna` 实现）。然后对比：有舱房号 vs 无舱房号 两组人的存活率有什么差别？

train_data['HasCabin'] = train_data['Cabin'].notna().astype(int)

# 把 NaN 填成 0，然后"不等于 0"的为 True，再转 1/0
# 但是，fillna 填入的值必须和列的类型兼容——字符串列填整数，就是这个警告的根源
# train_data['HasCabin'] = train_data['Cabin'].fillna(0).ne(0).astype(int)

train_data.groupby('HasCabin')['Survived'].mean()



# **Q9.** 对 Age 列做缺失值填充：用**各舱位等级的中位数**填充对应缺失值（分组中位数填充，而不是全局填一个数）。
# （提示：`groupby + transform` 是标准做法；想挑战的话试试纯 `fillna` 怎么写）
# .fillna() 默认并不会改原数据，它只是"算出一个填好的新列"还给你，改不改原表由你决定。
# 关键：pandas 大部分方法默认"返回新对象"

# transform是把算出来的值全部覆盖回去到每一行
# transform 自己不修改任何原数据，它只是返回一个长度和原表一样的新 Series：
target_num = train_data.groupby('Pclass')['Age'].transform('median')

train_data["Age"] = train_data["Age"].fillna(target_num)


# **Q10.** 只保留 **Age、Embarked 都无缺失** 的行（`dropna` + `subset`），并说明清洗后还剩多少人、删掉了多少人。
# subset —— 只关心某些列（Q10 要用的关键）
# how —— 缺失到什么程度才删
# axis —— 删行还是删列

before = len(train_data)

train_data = train_data.dropna(subset=['Age', 'Embarked'])

after = len(train_data)

print(before, after, before - after)

print('=============================')

## 第五部分：综合大题（5 个数据问题，请给出数字 + 一句话结论）

# **问题 1：各舱位的存活率分别是多少？舱位和存活的关系是什么？**

a11 = train_data.groupby('Pclass')['Survived'].mean().sort_values(ascending=False)
print(a11)
# 仓位等级越高，存活率越高


# **问题 2：性别与存活的关系是什么？"妇女优先"在数据里成立吗？**

a12 = train_data.loc[train_data['Sex'] == 'female', 'Survived'].mean()
print(a12)

# 女性存活率高，妇女优先成立



# **问题 3：获救者与遇难者的年龄分布有什么不同？**
# （提示：分组的 `describe()` 或分箱 `pd.cut` 后统计）

a13 = train_data.groupby('Survived')['Age'].describe()
print(a13)

train_data['AgeGroup'] = pd.cut(train_data['Age'], bins=[0, 12, 18, 35, 60, 100], labels=['儿童', '少年', '青年', '中年', '老年'])
a13_2 = train_data.groupby('AgeGroup', observed=True)['Survived'].mean()
print(a13_2)

# **问题 4：独自登船的人（SibSp 和 Parch 都为 0）和有家属同行的人，谁的存活率更高？**
# （提示：先造一个 `FamilySize = SibSp + Parch` 列，或直接造布尔列）

train_data['HasFamily'] = (train_data['SibSp'] + train_data['Parch']) > 0
a14 = train_data.groupby('HasFamily')['Survived'].mean()
print(a14)

a14_2 = pd.pivot_table(train_data, values='Survived', index='HasFamily', columns='Pclass')
print(a14_2)


# **问题 5：登船港口（Embarked）和存活率有关吗？这种关系是"真信号"还是假象？**
# （提示：看看各港口乘客的舱位构成是否不同——用透视表交叉验证）

a15_1 = train_data.groupby('Embarked')['Pclass'].describe()
a15_2 = pd.pivot_table(train_data, values='Survived', index='Embarked', columns='Pclass')
print(a15_1, a15_2)



