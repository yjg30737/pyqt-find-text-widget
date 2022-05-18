from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name='pyqt-find-text-widget',
    version='0.0.11',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'pyqt_find_text_widget.ico': ['prev.svg', 'next.svg', 'case.svg', 'word.svg',
                                                'regex.svg', 'close.svg']},
    description='PyQt widget which can be used to find text in QTextEdit/QTextBrowser',
    url='https://github.com/yjg30737/pyqt-find-text-widget.git',
    long_description_content_type='text/markdown',
    long_description=long_description,
    install_requires=[
        'PyQt5>=5.8',
        'pyqt-svg-button>=0.0.1'
    ]
)