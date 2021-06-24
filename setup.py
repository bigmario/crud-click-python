from setuptools import setup


setup(
    name='bv',
    version='0.1',
    py_modules=['bv'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        bv=bv:cli
    ''',
)