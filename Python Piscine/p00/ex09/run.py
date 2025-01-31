import os
from tqdm import tqdm


def build():
    with tqdm(total=100, desc='Build ') as prog_bar:
        os.system("python3 setup.py sdist bdist_wheel > /dev/null 2>&1")
        prog_bar.update(100)
    print()


def install():
    with tqdm(total=100, desc='Install') as prog_bar:
        os.system("pip3 install ./dist/ft_package-0.0.1.tar.gz \
                  > /dev/null 2>&1")
        prog_bar.update(100)
    print()


def show():
    with tqdm(total=100, desc='Display') as prog_bar:
        os.system("pip3 install ./dist/ft_package-0.0.1.tar.gz \
                  > /dev/null 2>&1")
        prog_bar.update(100)
    print()
    os.system("pip3 show -v ft_package")
    print()


def test():
    with tqdm(total=100, desc='Test') as prog_bar:
        os.system("pip3 install ./dist/ft_package-0.0.1.tar.gz \
                  > /dev/null 2>&1")
        prog_bar.update(100)
    print()
    os.system("python3 tester.py")
    print()


if __name__ == '__main__':
    build()
    install()
    show()
    test()
