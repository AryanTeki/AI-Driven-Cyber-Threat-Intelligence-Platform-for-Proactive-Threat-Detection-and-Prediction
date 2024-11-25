from setuptools import setup, find_packages

setup(
    name="real-time-threat-intelligence",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask>=2.0.1',
        'numpy>=1.21.2',
        'scikit-learn>=0.24.2',
        'pandas>=1.3.3',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Real-Time Threat Intelligence Integration System",
    keywords="cybersecurity, threat-intelligence, machine-learning",
    url="https://github.com/yourusername/real-time-threat-intelligence",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/real-time-threat-intelligence/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)