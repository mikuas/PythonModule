from setuptools import setup, find_packages

setup(
    name='FluentWidgets',
    version='0.0.5',
    author='Mikuas',
    author_email="email@example.com",
    packages=find_packages(),
    install_requires=[
        "PySide6>=6.4.2",
        "PySide6-Fluent-Widgets[full]"
    ]
)
