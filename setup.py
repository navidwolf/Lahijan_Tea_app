from setuptools import setup, find_packages

setup(
    name="tea_lahijan",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],  # کتابخانه‌هایی که نیاز داری (مثلاً numpy, pandas)
    entry_points={
        "console_scripts": [
            "tea=src.main:main",  # یعنی کاربر بتونه فقط tea بزنه و برنامه اجرا شه
        ],
    },
    author="Your Name",
    description="برنامه مدیریت کسب‌وکار چای لاهیجان",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/Tea-Project",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
