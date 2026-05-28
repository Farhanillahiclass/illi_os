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
        # Core UI
        'streamlit>=1.20.0', # For the main HUD
        'streamlit-option-menu>=0.3.0', # For enhanced UI components
        # System monitoring
        'psutil>=5.9.0',
        # Voice & audio
        'SpeechRecognition>=3.8.1', # For local STT
        'pyttsx3>=2.90', # For local TTS
        'pyaudio>=0.2.11', # Required by SpeechRecognition for microphone access
        # Image processing
        'Pillow>=9.0.0',
        # Browser & GUI automation
        'playwright>=1.40.0', # For web automation
        'pyautogui==0.9.54', # For GUI automation
        'selenium>=4.10.0', # Alternative for web automation
        # Input control
        'pynput>=1.8.0', # For global hotkeys
        'keyboard>=0.13.5', # Alternative for global hotkeys
        # Windows API
        'comtypes>=1.1.10', # For Windows COM objects (e.g., audio control)
        'pycaw>=20181226', # For Windows audio control
        'pywin32>=305', # For general Windows API access
        # Visualization
        'matplotlib>=3.7.0', # For plotting in UI (e.g., flowcharts)
        'networkx>=3.0', # For graph visualization in UI
        # Local LLM Support (Initial)
        'ollama>=0.1.0', # For local LLM inference
        'llama-cpp-python>=0.2.0', # For GGUF models
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
