import os
import subprocess
import json

print("Starting Git history export...")

# Config paths
order_file = 'conf/policy_order.txt'
usermap_file = 'conf/usermap.json'
policy_dir = 'policy'
output_dir = 'build'
output_file = os.path.join(output_dir, 'git_history.json')

# Load usermap
try:
    with open(usermap_file, 'r') as f:
        usermap = json.load(f)
except Exception as e:
    print(f"Error loading usermap {usermap_file}: {e}")
    usermap = {} # Continue with empty map if not found

# Ensure build directory exists
os.makedirs(output_dir, exist_ok=True)

all_history = {}

# Read policy order
try:
    with open(order_file, 'r') as f:
        for policy_filename in f:
            policy_filename = policy_filename.strip()
            if not policy_filename:
                continue
            
            file_path = os.path.join(policy_dir, policy_filename)
            print(f"Getting history for: {file_path}")
            
            # Git command to get log: Commit Hash | Author Name | Date | Commit Subject
            # --follow tracks file renames
            cmd = [
                'git', 'log',
                '--pretty=format:%H|%an|%ad|%s',
                '--date=short',
                '--follow',
                '--', file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            file_commits = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                try:
                    hash, author_name, date, subject = line.split('|', 3)
                    # Map the author name, default to the git name if not in map
                    mapped_name = usermap.get(author_name, author_name)
                    
                    file_commits.append({
                        'hash': hash,
                        'author_name': mapped_name,
                        'date': date,
                        'subject': subject
                    })
                except ValueError:
                    print(f"  Skipping malformed log line: {line}")
            
            all_history[policy_filename] = file_commits

except Exception as e:
    print(f"Error during Git history processing: {e}")
    exit(1)

# Write all history to the build file
with open(output_file, 'w') as f:
    json.dump(all_history, f, indent=2)

print(f"Git history successfully exported to {output_file}")