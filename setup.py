from setuptools import setup, find_packages
import platform

requirements = [
    'pyunormalize==15.1.0'
]

if platform.system() == 'Windows':
    requirements.append('pywin32==306')

setup(
    name='secured_health_record_system',
    version='1.0.0',
    packages=find_packages(),
    install_requires=requirements,
)