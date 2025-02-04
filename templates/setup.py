from setuptools import setup

setup(
    name="{module_name}",
    version="0.1.0",
    license="MPL-2.0",
    py_modules=["{module_name}"],
    entry_points={{
        "console_scripts": [
            "{output_name} = {module_name}:main"
        ]
    }},
    install_requires=[],
)
