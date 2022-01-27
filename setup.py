import os
from setuptools import setup, find_packages

from channels_discord import __version__

readme = os.path.join(os.path.dirname(__file__), 'README.md')

setup(
    name='channels_discord',
    version=__version__,
    url='https://github.com/AdvocatesInc/django-channels-discord',
    author='Advocates, Inc',
    author_email='admin@adv.gg',
    description='Interface server connecting Django\'s channels and Discord',
    long_description=open(readme).read(),
    license='Proprietary and confidential',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'discord.py>=1.7.3',
        'channels>=3.0.0',
    ],
    entry_points={'console_scripts': [
        'channels-discord = channels_discord.cli:CLI.entrypoint'
    ]},
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
