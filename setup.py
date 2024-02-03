from setuptools import setup


# with open("requirements.txt") as f:
#     install_requires = [
#         req for req in f.read().splitlines()
#         if not req.startswith('#') and not req.startswith('-e')
#     ]


setup(name='pipebro',
      version='1.0.0',
      description='Asynchronous pipeline framework',
      url='https://github.com/doorskgs/pipebro',
      author='oboforty',
      author_email='rajmund.csombordi@hotmail.com',
      license='MIT',
      zip_safe=False,
      packages=['pipebro'],
      install_requires=[]
      )
