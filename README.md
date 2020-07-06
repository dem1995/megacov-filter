# Megacov Dataset Filter
Python command-line script for filtering portions of the Megacov Twitter ID dataset (paper [here](https://arxiv.org/abs/2005.06012), files [here](https://github.com/UBC-NLP/megacov)) and isolating the resulting Twitter IDs by themselves for hydration
## Usage
To use `megacov-filter`, clone the repo (`git clone https://github.com/dem1995/megacov-filter.git`), make sure Python is installed, and run `python megacov_filter <inputfile1 inputfile2...> <outputfile>`. Tarballed+gzipped file collections are supported as inputs by setting the `-tgz` filter.
