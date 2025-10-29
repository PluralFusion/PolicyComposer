import os
import subprocess
import json
from datetime import datetime

print("Starting Git history export...")

# Config paths
order_file = 'conf/policy_order.txt'
usermap_file = 'conf/usermap.json'
policy_dir = 'policies'
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

# --- 1. Get the Current Build Commit Info ---
# We get this from the environment variables set by the GitHub Action
print("Getting current build commit info...")
try:
    actor = os.environ['CURRENT_COMMIT_ACTOR']
    current_commit = {
        'hash': os.environ['CURRENT_COMMIT_SHA'],
        'author_name': usermap.get(actor, actor), # Map the name
        'date': datetime.now().strftime('%Y-%m-%d'),
        'subject': os.environ['CURRENT_COMMIT_MSG']
    }
except KeyError:
    print("Could not get current commit info from env variables. Aborting.")
    exit(1)


# --- 2. Get File-Specific History ---
print("Getting file-specific history...")
file_history = {}

try:
    with open(order_file, 'r') as f:
        for policy_filename in f:
            policy_filename = policy_filename.strip()
            if not policy_filename:
                continue
            
            file_path = os.path.join(policy_dir, policy_filename)
            
            # Git command to get log *for this file only*
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
                    hash_val, author_name, date, subject = line.split('|', 3)
                    mapped_name = usermap.get(author_name, author_name)
                    
                    file_commits.append({
                        'hash': hash_val,
                        'author_name': mapped_name,
                        'date': date,
                        'subject': subject
                    })
                except ValueError:
                    print(f"  Skipping malformed log line: {line}")
            
            file_history[policy_filename] = file_commits

except Exception as e:
    print(f"Error during Git history processing: {e}")
    exit(1)

# --- 3. Write all data to the JSON file ---
final_history_data = {
    "current_build_commit": current_commit,
    "file_history": file_history
}

with open(output_file, 'w') as f:
    json.dump(final_history_data, f, indent=2)

print(f"Git history successfully exported to {output_file}")
