from setuptools import setup, find_packages

setup(
    name='pyqt-find-text-widget',
    version='0.3.2',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'pyqt_find_text_widget.ico': ['prev.svg', 'next.svg', 'case.svg', 'word.svg',
                                                'regex.svg', 'close.svg']},
    description='PyQt5 find text widget',
    url='https://github.com/yjg30737/pyqt-find-text-widget.git',
    install_requires=[
        'PyQt5>=5.8',
        'pyqt-svg-icon-pushbutton @ git+https://git@github.com/yjg30737/pyqt-svg-icon-pushbutton.git@main'
    ]
)