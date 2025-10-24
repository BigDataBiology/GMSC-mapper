import os
import sys
import filecmp

def test_no_annotation():
    """Test that --no-annotation flag produces expected output"""
    ok = True
    
    # Check that predicted.filterd.smorf.faa exists
    output_file = "./examples_output_no_annotation/predicted.filterd.smorf.faa"
    if not os.path.exists(output_file):
        ok = False
        print('\n--no-annotation: predicted.filterd.smorf.faa was not created.\n')
    else:
        # Check that the file has content
        if os.path.getsize(output_file) == 0:
            ok = False
            print('\n--no-annotation: predicted.filterd.smorf.faa is empty.\n')
        else:
            print(f'--no-annotation: predicted.filterd.smorf.faa created successfully ({os.path.getsize(output_file)} bytes)')
    
    # Check that summary.txt exists
    summary_file = "./examples_output_no_annotation/summary.txt"
    if not os.path.exists(summary_file):
        ok = False
        print('\n--no-annotation: summary.txt was not created.\n')
    else:
        print('--no-annotation: summary.txt created successfully')
    
    # Check that alignment and annotation files were NOT created
    files_that_should_not_exist = [
        "alignment.out.smorfs.tsv",
        "mapped.smorfs.faa",
        "habitat.out.smorfs.tsv",
        "taxonomy.out.smorfs.tsv",
        "quality.out.smorfs.tsv",
        "domain.out.smorfs.tsv"
    ]
    
    for filename in files_that_should_not_exist:
        filepath = f"./examples_output_no_annotation/{filename}"
        if os.path.exists(filepath):
            ok = False
            print(f'\n--no-annotation: {filename} should not exist but was found.\n')
    
    if ok:
        print('\n--no-annotation flag checking has passed.\n')
    else:
        sys.exit(1)

if __name__ == '__main__':
    test_no_annotation()
