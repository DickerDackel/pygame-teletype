from setuptools import find_packages, setup

setup(
    name='pygame-teletype',
    version='0.1.0',
    author='Michael Lamertz',
    author_email='michael.lamertz@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'cooldown @ git+https://github.com/dickerdackel/cooldown',
        'pygame-ce',
    ],
    entry_points={
        'console_scripts': [
            'teletype-demo = teletype.demo:main',
        ],
    },
)
