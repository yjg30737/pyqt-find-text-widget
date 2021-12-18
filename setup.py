from setuptools import setup, find_packages

setup(
    name='pyqt-find-text-widget',
    version='0.0.1',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'pyqt_find_text_widget.style': ['button.css'],
                  'pyqt_find_text_widget.ico': ['prev.png', 'next.png', 'case.png', 'regex.png', 'close.png']},
    description='PyQt5 find text widget',
    url='https://github.com/yjg30737/pyqt-find-text-widget.git',
    install_requires=[
        'PyQt5>=5.8',
        'pyqt-resource-helpee @ git+https://git@github.com/yjg30737/pyqt-resource-helpee.git@main'
    ]
)