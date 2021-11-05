import random

if __name__ == '__main__':
    # 生成随机数
    print(random.random())

    # 在数组中随机选择其中一个
    print(random.choice([1, 2, 3, 4, 5, 6, 7, 8]))

    # 在数组中随机选择其中几个 (获得的几个数据中, 有可能有重复数据)
    for i in range(100):
        result = random.choices([1, 2, 3, 4, 5, 6, 7, 8], k=2)
        if result[0] == result[1]:
            print(str(i) + ": ", result)

    # 在数组中随机选择其中几个 (获得的几个数据中, 不会有重复数据)
    print(random.sample([1, 2, 3, 4, 5, 6, 7, 8], k=2))

    print(random.randint(1, 591))

