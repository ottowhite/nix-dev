import os
import sys

NO_PAGER_VAR='LESS="${LESS:+$LESS }-X -F"'

def create_patch_folder():
    assert os.path.exists(".git"), "Not a git repository"

    if not os.path.exists(".git/patches"):
        os.system("mkdir .git/patches")

def get_current_patch_names():
    patch_names = os.popen("stg series").read().split("\n")
    patch_names = list(filter(lambda x: x != "", patch_names))

    applied_patches = []
    remaining_patches = []

    for patch_name in patch_names:
        if patch_name.startswith("+"):
            # Already applied patches
            applied_patches.append(patch_name[2:])
        elif patch_name.startswith(">"):
            # Current patch is the last one
            applied_patches.append(patch_name[2:])
        else:
            remaining_patches.append(patch_name[2:])

    return applied_patches, remaining_patches

def get_n_commit_hashes(n):
    commit_hashes = os.popen(f"{NO_PAGER_VAR} git log -n{n} --pretty=format:%H").read().split("\n")
    return list(reversed(commit_hashes))

# Turn named patches into commits and store patch names for each commit hash
def logged_commit(filename):
    applied_patches, remaining_patches = get_current_patch_names()

    # Store patch names in a file
    # Check if the file exists, create it if it doesn't
    if not os.path.exists(filename):
        pass

    # Commit the applied patches
    os.system(f"stg commit --all")

    # Find commit hashes of the applied patches
    commit_hashes = get_n_commit_hashes(len(applied_patches))
    patches_and_commit_hashes = list(zip(commit_hashes, applied_patches))

    with open(filename, "w") as f:
        for commit_hash, patch_name in patches_and_commit_hashes:
            f.write(f"{commit_hash},{patch_name}\n")

def uncommit_and_get_patch_name():
    return os.popen(f"stg uncommit --number 1").read().split("\n")[0][2:]

# Turn commits back into named patches
def uncommit_with_patch_names(filename):
    commit_hashes_to_patch_names = {}
    with open(filename, "r") as f:
        lines = f.read().split("\n")
        lines = list(filter(lambda x: x != "", lines))
        for line in lines:
            [commit_hash, patch_name] = line.split(",")
            commit_hashes_to_patch_names[commit_hash] = patch_name
        
    commit_hashes = list(reversed(get_n_commit_hashes(len(commit_hashes_to_patch_names))))

    for i in range(len(commit_hashes_to_patch_names)):
        print("Popping commit", commit_hashes[i])
        commit_hash = commit_hashes[i]
        original_patch_name = commit_hashes_to_patch_names[commit_hash]
        new_patch_name = uncommit_and_get_patch_name()

        print("New patch name", new_patch_name)
        print("Original patch name", original_patch_name)
        os.system(f"stg rename {new_patch_name} {original_patch_name}")

if __name__ == "__main__":
    create_patch_folder()

    # get arg which is either commit or uncommit, the next is the filename
    arg = sys.argv[1]
    filename = os.path.join(".git/patches", sys.argv[2])
    if not os.path.exists(filename):
        os.system("touch " + filename)
    if arg == "commit":
        logged_commit(filename)
    elif arg == "uncommit":
        uncommit_with_patch_names(filename)

