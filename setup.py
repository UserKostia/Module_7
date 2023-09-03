from setuptools import setup


setup(name='clean_folder',
      version='0.0.1',
      description='Use this code to sort files in your folders',
      url='',
      author='Kostia Striletskiy',
      author_email='kostastriletski@gmail.com',
      license='MIT',
      packages=['clean_folder'],
      zip_safe=False,
      include_package_data=True,
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']})
