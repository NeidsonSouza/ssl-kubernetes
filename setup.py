from setuptools import setup, find_packages

setup(
    name="sslautomation",
    packages=find_packages(),
    install_requires=[
        'certbot-dns-cloudflare>=1.13.0,<=1.13.0'
    ]
)