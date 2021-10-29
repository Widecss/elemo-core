~~~python
def decorator(name=None):
    def func_handler(func):
        def func2(d):
            print(f"d2={d}")
        return func2
    return func_handler

@decorator(name="a_func")
def func1(d):
    print(f"d1={d}")

def main():
    func1(1)

if __name__ == '__main__':
    main()
~~~

* 当 **decorator** 装饰器函数被@时，将直接运行装饰器函数，以及里面的 **func_handler**
* 当 **func1** 函数被调用时，装饰器函数和 **func_handler** 不会再次被调用
* 当 **main** 调用 **func1** 时，调用装饰器 **return** 的 **func2**
