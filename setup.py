# coding: utf-8
from setuptools import setup

setup(
  name="asyncio-rpc-aiopqueue",
  # version is handled dynamically by setuptools_scm
  use_scm_version = True,
  description="multiprocessing commlayer for nens/asyncio-rpc using AioQueue",
  keywords="",
  url="",
  author="Shahriar Heidrich",
  author_email="smheidrich@weltenfunktion.de",
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
  ],
  modules=["asyncio_rpc_aiopqueue"],
  python_requires=">3.7,<4",
  setup_requires=[
    "pytest-runner",
    "setuptools_scm",
  ],
  install_requires=[
    "aioprocessing>=2,<3",
    "asyncio-rpc>=0.1,<0.2",
  ],
)
