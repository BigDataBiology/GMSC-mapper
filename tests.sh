set -e

echo "# GMSC-Mapper
AUTHORS: Yiqian Duan, Celio Dias Santos Junior, Luis Pedro Coelho"

echo "Creating mocking databases"
gmsc-mapper createdb -i examples/target.faa -o examples/ -m diamond --quiet
gmsc-mapper createdb -i examples/target.faa -o examples/ -m mmseqs --quiet

echo "Testing basic usage"
gmsc-mapper -i examples/example.fa -o examples_output/ --db examples/diamond_targetdb.dmnd --habitat examples/ref_habitat.npy --habitat-index examples/ref_habitat_index.tsv --quality examples/ref_quality.txt --taxonomy examples/ref_taxonomy.npy --taxonomy-index examples/ref_taxonomy_index.tsv --domain examples/ref_domain.txt --quiet
python tests/diamond_contig.py

gmsc-mapper --aa-genes examples/example.faa -o examples_output/ --db examples/diamond_targetdb.dmnd --habitat examples/ref_habitat.npy --habitat-index examples/ref_habitat_index.tsv --quality examples/ref_quality.txt --taxonomy examples/ref_taxonomy.npy --taxonomy-index examples/ref_taxonomy_index.tsv --domain examples/ref_domain.txt --quiet
python tests/diamond_protein.py

gmsc-mapper --nt-genes examples/example.fna -o examples_output/ --db examples/diamond_targetdb.dmnd --habitat examples/ref_habitat.npy --habitat-index examples/ref_habitat_index.tsv --quality examples/ref_quality.txt --taxonomy examples/ref_taxonomy.npy --taxonomy-index examples/ref_taxonomy_index.tsv --domain examples/ref_domain.txt --quiet
python tests/diamond_gene.py

echo "Testing tool flag - MMSeqs"
gmsc-mapper -i examples/example.fa -o examples_output/ --db examples/mmseqs_targetdb --habitat ./examples/ref_habitat.npy --habitat-index ./examples/ref_habitat_index.tsv --quality examples/ref_quality.txt --taxonomy ./examples/ref_taxonomy.npy --taxonomy-index ./examples/ref_taxonomy_index.tsv --domain examples/ref_domain.txt --tool mmseqs --quiet
python tests/mmseqs_contig.py
