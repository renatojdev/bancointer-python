from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bancointer-python",
    version="0.10",
    description="Emita boletos bancários utilizando a API do Banco Inter PJ.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/renatojdev/bancointer-python",
    author="Renato P. Eduardo Jr",
    author_email="renatojdev@outlook.com",
    license="MIT",
    packages=[
        "bancointer",
        "bancointer.banking",
        "bancointer.banking.extrato",
        "bancointer.banking.models",
        "bancointer.cobranca_v3",
        "bancointer.cobranca_v3.cobranca",
        "bancointer.cobranca_v3.models",
        "bancointer.utils",
    ],
    install_requires=["requests", "certifi"],
    zip_safe=False,
)
