from setuptools import setup, find_packages

setup(
    name="video-editor-assistant",
    version="1.0.0",
    author="Author",
    author_email="author@example.com",
    description="智能视频剪辑助手",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/video-editor-assistant",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.8',
    install_requires=[
        line.strip()
        for line in open('requirements.txt', encoding='utf-8')
        if line.strip() and not line.startswith('#')
    ],
    entry_points={
        'console_scripts': [
            'video-editor=main:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['static/*', 'config.json'],
    },
)