set -v
set -e

echo "# GMSC-Mapper
AUTHORS: Yiqian Duan, Celio Dias Santos Junior, Luis Pedro Coelho"

echo "Creating mocking databases"
gmsc-mapper createdb -i examples/target.faa -o examples/ -m diamond
gmsc-mapper createdb -i examples/target.faa -o examples/ -m mmseqs

echo "Testing basic usage"
gmsc-mapper -i examples/example.fa --db examples/targetdb.dmnd --habitat examples/ref_habitat.txt --quality examples/ref_quality.txt --taxonomy examples/ref_taxonomy.txt
gmsc-mapper --aa-genes examples/example.faa --db examples/targetdb.dmnd --habitat examples/ref_habitat.txt --quality examples/ref_quality.txt --taxonomy examples/ref_taxonomy.txt
gmsc-mapper --nt-genes examples/example.fna --db examples/targetdb.dmnd --habitat examples/ref_habitat.txt --quality examples/ref_quality.txt --taxonomy examples/ref_taxonomy.txt

echo "Testing flags for no alternative results"
gmsc-mapper -i examples/example.fa --db examples/targetdb.dmnd --habitat examples/ref_habitat.txt --quality examples/ref_quality.txt --taxonomy examples/ref_taxonomy.txt --nohabitat --notaxonomy --noquality

echo "Testing tool flag - MMSeqs"
gmsc-mapper -i examples/example.fa --db examples/targetdb --habitat examples/ref_habitat.txt --quality examples/ref_quality.txt --taxonomy examples/ref_taxonomy.txt --tool mmseqs

echo "Testing tool flag - Diamond"
gmsc-mapper -i examples/example.fa --db examples/targetdb --habitat examples/ref_habitat.txt --quality examples/ref_quality.txt --taxonomy examples/ref_taxonomy.txt --tool diamond

