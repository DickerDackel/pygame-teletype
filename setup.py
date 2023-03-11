from setuptools import find_packages, setup

setup(
    name='pygame-teletype',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame-ce',
    ],
    package_data={
        'beep': ['beep.wav'],
    },
    data_files=[
        'beep.wav'
    ],
    entry_points={
        'console_scripts': [
            'teletype-demo = teletype.demo:main',
        ],
    },
)
