from setuptools import setup

__version__ = (2, 0, 0)

setup(
    name="orca",
    version=".".join(str(d) for d in __version__),
    description="OPeNDAP Request Compiler Application",
    install_requires=["dask[dataframe]", "Flask", "netCDF4", "requests", "xarray"],
    packages=["orca"],
    zip_safe=True,
    scripts=["scripts/process.py"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
)
