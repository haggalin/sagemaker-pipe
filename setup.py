from setuptools import setup, find_packages
import os
import sys
from setuptools.command.test import test as TestCommand


def generate_version(packages):
    """Attempts to find the version number from git describe.
    returns 'unknown-version' if not found.
    """
    try:
        import subprocess
        bashCommand="git describe --tags --long --dirty"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        version = output.decode('utf-8').replace("\n","")
        if version[0] == "v":
            version = version[1:]
        version = version.replace("-",".")
        split = version.split(".")
        version_map = {"major": split[0],
                       "minor": split[1],
                       "patch": split[2],
                       "build": os.environ.get("BUILD_NUMBER","0"),
                       "ext": ".dev" if "dirty" in split else "",
                       "commit": split[3]}
    except:
        version_map = {"major": "0",
                       "minor": "0",
                       "patch": "0",
                       "build": "0",
                       "ext": ".dev",
                       "commit": ""}
    version_format = "{major}.{minor}.{patch}.{build}{ext}"
    version = version_format.format(**version_map)
    for pack in packages:
        with open("{}/version.py".format(pack),"w") as f:
            f.write('__version__="{}"\n'.format(version))
    return version


class Tox(TestCommand):
    # Run tox as a test runner for all tests
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        cov.stop()
        sys.exit(errcode)


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


requires = [
    "boto3",
    "mxnet"
]


packages = find_packages(exclude=['test*'])
__version__ = generate_version(packages)

setup(
    name='sagemaker_pipe',
    version=__version__,
    description=("Simple implementation of SageMaker Training's internal IO subsystem that is able to pipe channel data files to an algorithm"),
    long_description=read('README.md'),
    author='Ishaaq Chandy',
    packages=packages,
    test_suite="test",
    tests_require=['tox'],
    cmdclass = {'test': Tox},
    entry_points={
              'console_scripts': [
                  'sagemaker-pipe = sagemaker_pipe.__init__:main'
              ]
          },
    install_requires=requires,
    keywords=('testing', 'sagemaker', 'aws')
)
