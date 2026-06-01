import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime
import os

def run_and_capture(script_path, output_md=None):
    """
    Runs a Python script and captures its output to a markdown file.
    
    Args:
        script_path: Path to the Python script to run
        output_md: Optional custom output filename (default: {script_name}_outputs.md)
    """
    script_path = Path(script_path)
    
    # Validate script exists
    if not script_path.exists():
        print(f"Error: Script not found: {script_path}")
        sys.exit(1)
    
    if not script_path.suffix == '.py':
        print(f"Error: File must be a Python script (.py): {script_path}")
        sys.exit(1)
    
    # Determine output filename
    if output_md is None:
        output_md = script_path.stem + "_outputs.md"
    
    output_path = Path(output_md)
    
    print(f"Running: {script_path}")
    print(f"Output will be saved to: {output_path.resolve()}")
    print("-" * 80)
    
    # Buffer to capture all output
    output_buffer = []
    # Prepare environment for child process
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8:replace'
    try:
        # Run the script with real-time output capture
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=script_path.parent,
            encoding='utf-8',
            errors='replace',
            env=env                        # <-- pass the modified environment
        )
        
        # Read output line by line in real-time
        for line in process.stdout:
            # Print to console
            print(line, end='')
            # Save to buffer
            output_buffer.append(line)
        
        # Wait for process to complete
        process.wait()
        exit_code = process.returncode
        
        # Combine all output
        full_output = ''.join(output_buffer)
        
        # Create markdown content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        md_content = f"""# Output from `{script_path.name}`

**Executed:** {timestamp}  
**Script Path:** `{script_path.resolve()}`  
**Exit Code:** {exit_code}

---

## Terminal Output

{full_output.strip()}

---

## Execution Details

- **Python Interpreter:** `{sys.executable}`
- **Working Directory:** `{script_path.parent.resolve()}`
- **Output File:** `{output_path.resolve()}`

"""
        
        # Add error section if script failed
        if exit_code != 0:
            md_content += f"""
## ⚠️ Execution Status

**The script exited with code {exit_code}** (non-zero indicates an error occurred)

"""
        else:
            md_content += """
## ✓ Execution Status

**Script completed successfully** (exit code 0)

"""
        
        # Write to markdown file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print("-" * 80)
        print(f"[OK] Output saved to: {output_path.resolve()}")
        
        if exit_code != 0:
            print(f"[WARNING] Script exited with error code: {exit_code}")
            sys.exit(exit_code)
        
    except subprocess.SubprocessError as e:
        print(f"Error running script: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Process terminated by user")
        if process:
            process.terminate()
        sys.exit(130)

def main():
    parser = argparse.ArgumentParser(
        description="Run a Python script and save its output to a markdown file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python process_runner.py script.py
  python process_runner.py /path/to/script.py
  python process_runner.py script.py --output custom_name.md
  python process_runner.py analysis.py -o results.md
        """
    )
    
    parser.add_argument(
        'script',
        type=str,
        help='Path to the Python script to run'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Custom output markdown filename (default: {script_name}_outputs.md)'
    )
    
    args = parser.parse_args()
    
    run_and_capture(args.script, args.output)

if __name__ == "__main__":
    main()