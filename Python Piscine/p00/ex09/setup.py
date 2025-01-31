from setuptools import setup, find_packages

setup(
    name='ft_package',
    version="0.0.1",
    description="A sample package",
    author='makhtar',
    author_email="makhtar@student.42abudhabi.ae",
    url='https://github.com/muazzam-akhtar/PythonPiscine/p00/ex09/ft_package',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [],
    },
)
