from setuptools import find_packages, setup

setup(
    name='neostructure',
    version='0.1',
    packages=find_packages(),  # This will include the 'neostructure' package
    install_requires=[
        'requests',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'neostructure=neostructure.app:app',  # Updated entry point
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
