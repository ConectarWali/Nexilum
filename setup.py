from setuptools import setup, find_packages

def load_requirements(filename):
    with open(filename, "r") as f:
        return f.read().splitlines()
    
#print(load_requirements("requirements.txt"))

setup(
    name='Nexilum',
    version='0.0.2',
    description='A Python library for simplifying HTTP integrations with REST APIs, featuring decorators for authentication handling and request management.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Conectar Wali SAS',
    author_email='dev@conectarwalisas.com.co',
    url='https://github.com/ConectarWali/Nexilum',
    packages=find_packages(),
    install_requires=['anyio==4.8.0', 'bidict==0.23.1', 'certifi==2024.12.14', 'charset-normalizer==3.4.1', 'h11==0.14.0', 'httpcore==1.0.7', 'httpx==0.28.1', 'idna==3.10', 'python-engineio==4.11.2', 'python-socketio==5.12.1', 'requests==2.32.3', 'simple-websocket==1.1.0', 'sniffio==1.3.1', 'typing_extensions==4.12.2', 'urllib3==2.3.0', 'websockets==14.1', 'wsproto==1.2.0'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    license_files=['LICENSE'],
    python_requires='>=3.9',
)
