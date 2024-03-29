set -e

echo "# GMSC-Mapper
AUTHORS: Yiqian Duan, Celio Dias Santos Junior, Luis Pedro Coelho"

echo "Creating mocking databases"
gmsc-mapper createdb -i examples/target.faa -o examples/ -m diamond --quiet
gmsc-mapper createdb -i examples/target.faa -o examples/ -m mmseqs --quiet

echo "Testing basic usage"
gmsc-mapper -i examples/example.fa -o examples_output/ --dbdir examples/ --quiet
python tests/diamond_contig.py

gmsc-mapper --aa-genes examples/example.faa -o examples_output/ --dbdir examples/ --quiet
python tests/diamond_protein.py

gmsc-mapper --nt-genes examples/example.fna -o examples_output/ --dbdir examples/ --quiet
python tests/diamond_gene.py

echo "Testing tool flag - MMSeqs"
gmsc-mapper -i examples/example.fa -o examples_output/ --dbdir examples/ --tool mmseqs --quiet
python tests/mmseqs_contig.py
