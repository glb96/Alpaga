import setuptools
from setuptools.command.egg_info import egg_info


#
# with open("README.md", "r") as fh:
#     long_description = fh.read()

class egg_info_ex(egg_info):
    """Includes license file into `.egg-info` folder."""

    def run(self):
        # don't duplicate license into `.egg-info` when building a distribution
        if not self.distribution.have_run.get('install', True):
            # `install` command is in progress, copy license
            self.mkpath(self.egg_info)
            self.copy_file('LICENSE.txt', self.egg_info)

        egg_info.run(self)


setuptools.setup(
    name="Alpaga", # Replace with your own username
    version="1.2",
    author="Guillaume Le Breton, Fabien Rondepierre, Maxime Fery, Oriane Bonhomme",
    author_email="guillaume.le-breton@ens-lyon.fr, fabien.rondepierre@univ-lyon1.fr, maxime.fery@univ-lyon1.fr, oriane.bonhomme@univ-lyon1.fr",
    description="AnaLyse en PolArisation de la Generation de second hArmonique",
#    long_description=long_description,
#    long_description_content_type="text/markdown",
    url="https://doi.org/10.5281/zenodo.5639393",
    zip_safe=False,
    packages=setuptools.find_packages(),
    package_data={'': ['Data_tutorial/SHS/Eau_polar_V/*.dat', 'Data_tutorial/SHS/Single_acquisition/*.dat', 'Data_tutorial/SSHG/*.p', 'Data_tutorial/SHS/*.p']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public v2.1.",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['numpy', 'matplotlib', 'scipy'],
    license='Lesser GPL v2.1',
    license_files=('LICENSE.txt',)
)

