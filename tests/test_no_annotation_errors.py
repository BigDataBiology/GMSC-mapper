import subprocess
import sys

def test_no_annotation_requires_input():
    """Test that --no-annotation requires --input to be specified"""
    
    test_cases = [
        {
            'cmd': ['gmsc-mapper', '--no-annotation', '--aa-genes', 'examples/example.faa', '-o', 'test_output'],
            'description': '--no-annotation with --aa-genes should fail'
        },
        {
            'cmd': ['gmsc-mapper', '--no-annotation', '--nt-genes', 'examples/example.fna', '-o', 'test_output'],
            'description': '--no-annotation with --nt-genes should fail'
        },
        {
            'cmd': ['gmsc-mapper', '--no-annotation', '-o', 'test_output'],
            'description': '--no-annotation without any input should fail'
        }
    ]
    
    ok = True
    for test_case in test_cases:
        try:
            result = subprocess.run(
                test_case['cmd'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Should fail (non-zero exit code)
            if result.returncode == 0:
                ok = False
                print(f'\nFailed: {test_case["description"]} - command succeeded but should have failed\n')
            else:
                # Check for expected error message
                if 'requires --input' in result.stderr or 'requires' in result.stderr.lower():
                    print(f'Passed: {test_case["description"]}')
                else:
                    print(f'Warning: {test_case["description"]} - failed but with unexpected error message')
                    print(f'  stderr: {result.stderr[:200]}')
        
        except subprocess.TimeoutExpired:
            ok = False
            print(f'\nFailed: {test_case["description"]} - command timed out\n')
        except Exception as e:
            ok = False
            print(f'\nFailed: {test_case["description"]} - exception: {str(e)}\n')
    
    if ok:
        print('\n--no-annotation error checking has passed.\n')
    else:
        sys.exit(1)

if __name__ == '__main__':
    test_no_annotation_requires_input()
