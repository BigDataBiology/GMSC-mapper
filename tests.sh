set -e

echo "# GMSC-Mapper
AUTHORS: Yiqian Duan, Celio Dias Santos Junior, Luis Pedro Coelho"

echo "Creating mocking databases"
gmsc-mapper createdb -i examples/target.faa -o examples/ -m diamond
gmsc-mapper createdb -i examples/target.faa -o examples/ -m mmseqs

echo "Testing basic usage"
gmsc-mapper -i ./examples/example.fa -o ./examples_output/ --db ./examples/targetdb.dmnd --habitat ./examples/ref_habitat.txt --quality ./examples/ref_quality.txt --taxonomy ./examples/ref_taxonomy.txt
python tests/diamond_contig.py
gmsc-mapper --aa-genes examples/example.faa -o examples_output/ --db examples/targetdb.dmnd --habitat examples/ref_habitat.txt --quality examples/ref_quality.txt --taxonomy examples/ref_taxonomy.txt
python tests/diamond_protein.py
gmsc-mapper --nt-genes examples/example.fna -o examples_output/ --db examples/targetdb.dmnd --habitat examples/ref_habitat.txt --quality examples/ref_quality.txt --taxonomy examples/ref_taxonomy.txt
python tests/diamond_gene.py

echo "Testing tool flag - MMSeqs"
gmsc-mapper -i examples/example.fa -o examples_output/ --db examples/targetdb --habitat examples/ref_habitat.txt --quality examples/ref_quality.txt --taxonomy examples/ref_taxonomy.txt --tool mmseqs
python tests/mmseqs_contig.py