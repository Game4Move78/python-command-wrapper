from setuptools import setup

setup(
    name="py_wrapper",
    version="0.1.0",
    license="MPL-2.0",
    py_modules=["py_wrapper"],
    entry_points={
        "console_scripts": [
            "py_wrapper = py_wrapper:main"
        ]
    },
    install_requires=[],
)
