# -*- coding: utf-8 -*-

__author__ = "chipiga86@gmail.com"


from setuptools import setup

setup(
    name='nose-allure-plugin',
    version='1.0.6',
    description='Nose plugin for allure framework',
    long_description=open('README.rst').read(),
    author='Sergey Chipiga',
    author_email='chipiga86@gmail.com',
    packages=["nose_allure"],
    url="https://github.com/allure-framework/allure-nose-adaptor",
    install_requires=[
        'nose',
        'pytest-allure-adaptor'
    ],
    entry_points={
        'nose.plugins.0.10': [
            'allure = nose_allure:Allure'
        ]
    }
)
