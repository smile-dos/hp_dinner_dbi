from setuptools import setup, find_packages


setup(
    name="dinner-order-service",
    author="zhangdong",
    description="Rpc service for dinner",
    packages =find_packages(),
    version="1.0.0",
    install_requires=[
        "sqlalchemy",
        "kombu",
        "mysqlclient"
    ],
    entry_points={
        "console_scripts": [
            "happy-dinner=data_service.entry.service_admin:start"
        ]
    }
)
