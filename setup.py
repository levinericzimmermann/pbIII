from setuptools import setup

setup(
    name="pbIII",
    version="0.0.001",
    license="GPL",
    description="",
    author="Levin Eric Zimmermann",
    author_email="levin-eric.zimmermann@folkwang-uni.de",
    url="https://github.com/uummoo/pbII",
    packages=[
        "pbIII",
        "pbIII.fragments",
        "pbIII.globals",
        "pbIII.segments",
    ],
    package_data={},
    include_package_data=True,
    setup_requires=[""],
    tests_require=["nose"],
    install_requires=[""],
    extras_require={},
    python_requires=">=3.6",
)
