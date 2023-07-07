from setuptools import setup
def readme():
    with open('README.md','r') as f:
        return f.read()
setup(
    name='jitbf',
    description='Brainfuck JIT interpreter in Python',
    long_description=readme(),
    keywords=['brainfuck','jit-interpreter','llvm'],
    long_description_content_type='text/markdown',
    url='https://github.com/none-None1/jitbf',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Interpreters'
    ],python_requires='>=3',version='1.0.0',entry_points={
        'console_scripts':[
            'jitbf=jitbf:_test'
        ]
    },py_modules=['jitbf']
)
