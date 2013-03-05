from distutils.core import setup
import pytz


setup(
    name='django-nonrel-pytz',
    version=pytz.__version__,
    url='https://github.com/potatolondon/django-nonrel-pytz/',
    license='MIT',
    author='Luke Benstead',
    author_email='lukeb@potatolondon.com',
    description='A version of pytz for Django on Google App Engine.',
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['pytz'],
    include_package_data=True,
    package_data={'pytz': ['zoneinfo.zip']},
)
