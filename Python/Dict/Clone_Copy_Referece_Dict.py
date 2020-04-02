import copy

if __name__ == '__main__':
    sample_dict = {"Key1": "Value1", "Key2": "Value2"}
    dict_has_list = {"Key1": [1,2,3,4], "Key2": [5,6,7,8]}

    # 浅copy

    copy_sample_dict = sample_dict.copy()
    copy_dict_has_list = dict_has_list.copy()

    copy_sample_dict['Key1'] = "Value3"

    # 注意浅copy中, 只有非引用的数据才会被copy, 像列表这种引用数据是不会被copy的
    copy_dict_has_list['Key1'][0] = 9

    # 但新建的key与value就不会影响到原有的dict
    copy_dict_has_list['Key3'] = [10,11,12]

    # 深copy

    deep_copy_dict_has_list = copy.deepcopy(dict_has_list)

    # 深copy中, 所有数据都被copy, 像列表这种引用数据也会被copy的, 但速度较慢
    deep_copy_dict_has_list['Key1'][0] = 10

    # 当然新建的key与value就不会影响到原有的dict
    deep_copy_dict_has_list['Key3'] = [10,11,12]

    print("原sample dict: ", sample_dict)
    print("原list dict: ", dict_has_list)

    print("浅copy后sample dict: ", copy_sample_dict)
    print("浅copy后list dict: ", copy_dict_has_list)

    print("深copy后list dict: ", deep_copy_dict_has_list)