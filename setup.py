from distutils.core import setup
setup(
    name = 'EventhubHandler',         
    packages = ['EventhubHandler'], 
    version = '0.1', 
    license='MIT',
    description = 'Push your logs to Azure Event hub',
    author = 'Patil, Parikshit',
    author_email = 'patil8698parikshit@gmail.com',
    url = 'https://github.com/PSKP-95/EventhubHandler',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/PSKP-95/EventhubHandler/archive/v_01.tar.gz',    # I explain this later on
    keywords = ['eventhub', 'python', 'logging', "azure"],
    install_requires=[  
        'azure.eventhub'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)
