import threadpool #threadpool 是外部包


# def func(name):
#     print('hi {}\n'.format(name))
#
# if __name__ == '__main__':
#     data = ['xijun.gong', 'xijun', 'gxjun']
#     pool = threadpool.ThreadPool(5)
#     reqs = threadpool.makeRequests(func, data)
#     [pool.putRequest(req) for req in reqs]
#     pool.wait()

def testing_steps(*params):
    page, driver, device_platform, device_name = params
    print(params)


def run_steps_t(func, pages, drivers, devices):
    pars = []
    for d in devices.keys():
        # 由于makeRequests使用了动态参数,所以参数第一个为要进行多线程的方法名
        # 第二就是方法的参数列表(即是*args),第三就是方法的参数字典(即是**kwargs)
        # 使用列表传入数据,就要制作一个列表,格式是[(var_list1,None),(var_list2, None)]
        # 其中None表明不使用参数字典
        # 如果要使用参数字典而不使用参数列表,就反转,格式是[(None,var_dict1),(None,var_dict2)]
        # 我在这里使用的是参数列表,所以要在后面加None
        pars.append(((pages[d], drivers[d], devices[d], d), None))
    print(pars)
    task_pool = threadpool.ThreadPool(len(devices))
    requests = threadpool.makeRequests(func, pars)
    for req in requests:
        task_pool.putRequest(req)
    task_pool.wait()

if __name__ == '__main__':
    pages = {"Note5": "Pages_Note5", "Pixel": "Pages_Pixel"}
    drivers = {"Note5": "Drivers_Note5", "Pixel": "Drivers_Pixel"}
    devices = {"Note5": "Devices_Note5", "Pixel": "Devices_Pixel"}
    run_steps_t(testing_steps, pages, drivers, devices)





