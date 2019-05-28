import argparse

'''
argparse 使用
官方帮助文档
https://docs.python.org/3/library/argparse.html
简单示例
我们先来看一个简单示例。主要有三个步骤：

创建 ArgumentParser() 对象
调用 add_argument() 方法添加参数
使用 parse_args() 解析添加的参数
'''

# 参数形式1, 没有选项,只以参数位置来定位参数

# parser = argparse.ArgumentParser()
# parser.add_argument("square", help="display a square of a given number", type=int)
# args = parser.parse_args()
# print(args.square**2)

# 参数形式2, 以指定开关来定位参数

# parser = argparse.ArgumentParser()
#
# parser.add_argument("--s", help="display a square of a given number", type=int)
# parser.add_argument("--c", help="display a cubic of a given number", type=int)
#
# args = parser.parse_args()
#
# if args.s:
#     print(args.s ** 2)
#
# if args.c:
#     print(args.c ** 3)

# 上面两种方式混合用

parser = argparse.ArgumentParser(description='Process some integers.')
# 解析第一个位置参数,这个参数预期是int类型,个数1个以上, 解析后会被存入一个名叫integers的list中
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')

# 解析可选参数,如果有指定这个可选参数的话,就执行const指定的内容(这里是执行内置方法sum)
# 如果没有指定,就执行default指定的内容(这里是执行内置方法max)
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))

args2 = parser.parse_args(['-1','7','14', '--sum']) #其实可以在程序里指定参数而不必一定要从外面传入
print(args2.accumulate(args2.integers))

'''
argparse.ArgumentParser（）方法参数须知

prog=None - 程序名, 默认是以当前运行的py文件名为当前运行程序名的
    例子:
    parser = argparse.ArgumentParser()
    如果使用-h,或者出错后自动显示提示信息,会打印出
    usage: myprogram.py [-h] [--foo FOO]
    如果更改了prog,比如
    parser = argparse.ArgumentParser(prog='MyApp')
    对应的信息就会显示为
    usage: Myapp [-h] [--foo FOO]

description=None, - help时显示的开始文字, 一般只会指定这个
    例子: 如果有指定,就会在中间显示这段文字
    parser = argparse.ArgumentParser(prog="MyApp", description="It is my first app")
    那么会显示为
    usage: Myapp [-h] [--foo FOO]
    It is my first app

usage, 用于指定usage行的输出,默认是自动分析所有参数项后自动生成
    例子: 如果无指定,就会自动分析所有参数项后自动生成包含所有的
    usage: myprogram.py [-h] [--foo FOO]
    如果有指定,就会在中间显示这段文字
    parser = argparse.ArgumentParser(prog="MyApp", usage='%(prog)s [options]')
    那么会显示为
    usage: Myapp [options]

epilog=None, - help时显示的结尾文字
    例子:
    parser = argparse.ArgumentParser(epilog="THE END")
    就会显示:
    usage: myprogram.py [-h]
    A foo that bars
    optional arguments:
     -h, --help  show this help message and exit
    THE END
parents=[], -若与其他参数的一些内容一样，可以继承
formatter_class=argparse.HelpFormatter, - 自定义帮助信息的格式
prefix_chars='-', - 命令的前缀，默认是‘-’
fromfile_prefix_chars=None, - 命令行参数从文件中读取
argument_default=None, - 设置一个全局的选项缺省值，一般每个选项单独设置
conflict_handler='error',     - 定义两个add_argument中添加的选项名字发生冲突时怎么处理，默认处理是抛出异常
add_help=True    - 是否增加-h/--help选项，默认是True)

'''


'''
add_argument() 方法定义如何解析命令行参数： 

例子:
ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices]
                            [, required][, help][, metavar][, dest])
 

每个参数解释如下:

name or flags - 选项字符串的名字或者列表，例如 foo 或者 -f, --foo。如果不指定dest, 传入到程序中的参数变量会取包括--那一个name or flag
例子:
parser.add_argument('--ver', '-v', action = 'store_true', help = 'hahaha') #这里解析出来的就是ver
args = parser.parse_args()
print(args.ver)

action - 命令行遇到参数时的动作，默认值是 store。
store_const，表示赋值为const；
append，将遇到的值存储成列表，也就是如果参数重复则会保存多个值;
append_const，将参数规范中定义的一个值保存到一个列表；
count，存储遇到的次数；此外，也可以继承 argparse.Action 自定义参数解析；
nargs - 应该读取的命令行参数个数，可以是具体的数字，或者是?号，当不指定值时对于 Positional argument 使用 default，
        对于 Optional argument 使用 const；或者是 * 号，表示 0 或多个参数；或者是 + 号表示 1 或多个参数。
例子: 指定这个参数后面的value有多少个，默认为1
parser.add_argument('filename', nargs = 2, type = int)
即是执行的命令行可以这样写 command test1 test2 #test1 与 test2都为参数filename的值被传入
nargs还可以'*'用来表示如果有该位置参数输入的话，之后所有的输入都将作为该位置参数的值；
‘+’表示读取至少1个该位置参数。'?'表示该位置参数要么没有，要么就只要一个        

const - action 和 nargs 所需要的常量值。
default - 不指定参数时的默认值。
type - 命令行参数应该被转换成的类型。
choices - 参数可允许的值的一个容器。
例子: 表示该参数能接受的值只能来自某几个值候选值中，除此之外会报错,如果像下面这样写, file参数只能是test1与test2的其中一个
parser.add_argument('file', choices = ['test1', 'test2'])
args = parser.parse_args()

required - 可选参数是否可以省略 (仅针对可选参数)。
例子: 如果像下面这样写, --ver 或者 -v这个参数就一定要加入到执行命令行中,不然会报错
parser.add_argument('--ver', '-v', required = True, type = int)

help - 参数的帮助信息，当指定为 argparse.SUPPRESS 时表示不显示该参数的帮助信息.
metavar - 在 usage 说明中的参数名称，对于必选参数默认就是参数名称，对于可选参数默认是全大写的参数名称.
dest - 解析后的参数名称，默认情况下，对于可选参数选取最长的名称，中划线转换为下划线.
'''

