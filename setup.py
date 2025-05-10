from setuptools import setup, find_packages

setup(
    name="cyber-nexus",
    version="1.0.0",
    description="Advanced Cybersecurity CLI Tool",
    author="Your Name",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cyber-nexus = main:main'
        ]
    },
    install_requires=[
        "requests",
        "rich"
    ],
    include_package_data=True,
)
