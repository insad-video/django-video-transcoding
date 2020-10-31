import os
import re
import subprocess
from setuptools import setup, find_packages  # type: ignore
from pathlib import Path

with open('README.md') as f:
    long_description = f.read()

version_re = re.compile('^Version: (.+)$', re.M)
package_name = 'django_video_transcoding'


def get_version():
    """
    Reads version from git status or PKG-INFO

    https://gist.github.com/pwithnall/7bc5f320b3bdf418265a
    """
    d: Path = Path(__file__).absolute().parent
    git_dir = d.joinpath('.git')
    if git_dir.is_dir():
        # Get the version using "git describe".
        cmd = 'git describe --tags --match [0-9]*'.split()
        try:
            version = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            return None

        # PEP 386 compatibility
        if '-' in version:
            version = '.post'.join(version.split('-')[:2])

        # Don't declare a version "dirty" merely because a time stamp has
        # changed. If it is dirty, append a ".dev1" suffix to indicate a
        # development revision after the release.
        with open(os.devnull, 'w') as fd_devnull:
            subprocess.call(['git', 'status'],
                            stdout=fd_devnull, stderr=fd_devnull)

        cmd = 'git diff-index --name-only HEAD'.split()
        try:
            dirty = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            return None

        if dirty != '':
            version += '.dev1'
    else:
        # Extract the version from the PKG-INFO file.
        try:
            with open('PKG-INFO') as v:
                version = version_re.search(v.read()).group(1)
        except FileNotFoundError:
            version = None

    return version


setup(
    name='django_video_transcoding',
    version=get_version() or 'dev',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(
        where='src',
        exclude=['dvt', 'video_transcoding.tests']),
    package_dir={"": "src"},
    include_package_data=True,
    url='https://github.com/just-work/django-video-transcoding',
    license='MIT',
    author='Sergey Tikhonov',
    author_email='zimbler@gmail.com',
    description='Simple video transcoding application for Django framework',
    install_requires=[
        # Django
        'Django>=2.2,<3.2',
        'django-model-utils~=4.0.0',
        # Background processing
        'Celery~=5.0.1',
        'kombu~=5.0.2',
        'billiard~=3.6.3.0',
        # Uploading
        'requests~=2.24.0',
        # Video processing
        'pymediainfo~=4.2.1',
        'fffw~=3.1.0',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Multimedia :: Video :: Conversion',
    ]
)
