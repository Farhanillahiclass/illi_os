from setuptools import setup, find_packages

setup(
    name='illi_os',
    version='1.2.5',
    description='ILLI OS v1.2.5 - Local offline desktop AI agent with Ghost-Protocol HUD',
    author='ILLI AI Systems',
    author_email='core@illi.local',
    url='https://github.com/yourusername/illi_os',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=[
        # Core UI
        'streamlit>=1.20.0',
        'streamlit-option-menu>=0.3.0',
        # System monitoring
        'psutil>=5.9.0',
        # Voice & audio
        'SpeechRecognition>=3.8.1',
        'pyttsx3>=2.90',
        # Image processing
        'Pillow>=9.0.0',
        # Browser & GUI automation
        'playwright>=1.40.0',
        'pyautogui==0.9.54',
        'selenium>=4.10.0',
        # Input control
        'pynput>=1.8.0',
        'keyboard>=0.13.5',
        # Windows API
        'comtypes>=1.1.10',
        'pycaw>=20181226',
        'pywin32>=305',
        # Visualization
        'matplotlib>=3.7.0',
        'networkx>=3.0',
        # Async
        'trio>=0.22.0',
        # Database
        'sqlalchemy>=2.0.0',
        # Utilities
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
    ],
    entry_points={
        'console_scripts': [
            'illi-ai=illi_ai.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
    ],
)
