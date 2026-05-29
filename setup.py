from setuptools import setup, find_packages

setup(
    name='illi',
    version='1.2.5',
    description='ILLI: A Fully Offline, Local-First, API-Free, Self-Improving AI Assistant',
    author='ILLI AI Core Team',
    author_email='core@illi.local',
    url='https://github.com/yourusername/illi_os',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=[
        'streamlit>=1.20.0',
        'psutil>=5.9.0',
        'SpeechRecognition>=3.8.1',
        'pyttsx3>=2.90',
        'Pillow>=9.0.0',
        'pynput>=1.8.0',
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
    ],
    extras_require={
        'automation': [
            'playwright>=1.40.0',
            'pyautogui==0.9.54',
            'selenium>=4.10.0',
            'comtypes>=1.1.10',
            'pycaw>=20181226',
            'pywin32>=305',
        ],
        'visual': [
            'matplotlib>=3.7.0',
            'networkx>=3.0',
        ],
        'data': [
            'sqlalchemy>=2.0.0',
        ],
        'llm': [
            'ollama>=0.1.0',
            'llama-cpp-python>=0.2.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'illi-ai=illi.cli:main',
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
