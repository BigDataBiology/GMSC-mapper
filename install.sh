set -v
set -e

# This is set in travis
if [[ x$PYTHON_VERSION == x ]]; then
    PYTHON_VERSION=3.9
fi


echo "
# GMSC-Mapper
AUTHORS: Yiqian Duan, Celio Dias Santos Junior, Luis Pedro Coelho
"

if ! which conda > /dev/null; then
    echo "[ Conda not found. Please install miniconda and add 'conda' to the PATH: "
    echo "    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    echo "    sh Miniconda3-latest-Linux-x86_64.sh"
    exit 1
fi

eval "$(conda shell.bash hook)"

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


echo "# Creating new environment for GMSC-mapper"
mkdir -p envs

conda config --env --add channels defaults
conda config --env --add channels bioconda
conda config --env --add channels conda-forge

if ! which mamba > /dev/null; then
    CONDA_INSTALL_CMD=conda
else
    echo "# Installing packages with MAMBA"
    CONDA_INSTALL_CMD=mamba
fi

${CONDA_INSTALL_CMD} env create \
          -p $BASEDIR/envs/gmscmapper \
          -f $BASEDIR/environment.yml

# only activate AFTER install all the packages to get the right environmental variables
source activate $BASEDIR/envs/gmscmapper
python3 $BASEDIR/setup.py install
bash $BASEDIR/tests.sh

echo "############ Installation procedures finished
****** Thank you for installing GMSC-Mapper ********
--- Please submit bugreports/comments to
https://github.com/BigDataBiology/GMSC-mapper/issues"

