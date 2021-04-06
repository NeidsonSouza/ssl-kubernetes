from setuptools import setup, find_packages

setup(
    name="sslautomation",
    packages=find_packages(),
    install_requires=[
        'pytest>=6.2.2,<=6.2.2',
        'certbot-dns-cloudflare>=1.13.0,<=1.13.0'
    ]
)