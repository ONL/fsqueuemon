#!/usr/bin/env python

from distutils.core import setup
from babel.messages import frontend as babel

setup(name='fsqueuemon',
      version='0.1.1',
      author='Markus Lindenberg',
      description='Call Center Queue Monitor for FreeSwitch',
      url='https://github.com/gonicus/fsqueuemon',
      py_modules=['queuemon'],
      install_requires=["flask", "flask_babel"],
      extras_require={"test": ["pytest", "coverage"]},
      cmdclass = {'compile_catalog': babel.compile_catalog,
                'extract_messages': babel.extract_messages,
                'init_catalog': babel.init_catalog,
                'update_catalog': babel.update_catalog},
      )
