from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bancointer-python",
    version="0.7",
    description="Emita boletos bancários utilizando a API do Banco Inter PJ.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/renatojdev/bancointer-python",
    author="Renato P. Eduardo Jr",
    author_email="renato@paulaeduardo.com",
    license="MIT",
    packages=["bancointer"],
    install_requires=["requests"],
    zip_safe=False,
)
