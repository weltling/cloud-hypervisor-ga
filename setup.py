import setuptools
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="cloud-hypervisor-ga",
    version="0.0.1",
    author="Karissa Sanchez, Anatol Belski",
    author_email="kasanchez519@gmail.com, anbelski@microsoft.com",
    packages=["src/guest_agent", "test"],
    description="A guest agent for cloud hypervisor VMs",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/kasanchez519/ch-guest-agent.git",
    license='BSD-2-Clause',
    python_requires='>=3.8',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'cloud-hypervisor-ga = src.guest_agent.guest_agent:main',
        ]
    }
)
