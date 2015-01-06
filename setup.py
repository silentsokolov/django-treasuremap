from distutils.core import setup

setup(
    name='django-treasuremap',
    version='0.2',
    url='https://github.com/silentsokolov/django-treasuremap',
    license='MIT',
    author='Dmitriy Sokolov',
    author_email='silentsokolov@gmail.com',
    description='django-treasuremap app, makes it easy to store and display the location on the map using different providers (Google, Yandex).',
    packages=['treasuremap'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'django>=1.6',
    ],
    tests_require=['Django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)