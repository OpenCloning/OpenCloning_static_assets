#!/bin/bash
set -e

# Create assets directory if it doesn't exist
mkdir -p assets

# Copy index.html to assets directory
cp index.html assets/index.html

# Copy headers file
cp _headers assets/_headers

# Read the versions.json file and create directories
for dir in $(jq -r 'keys[]' versions.json); do
    # Create the directory if it doesn't exist
    mkdir -p "assets/$dir"

    # Get the repository URL
    repo_url=$(jq -r ".\"$dir\".repository" versions.json)

    # Get the commit hash
    commit_hash=$(jq -r ".\"$dir\".commit" versions.json)

    # Get the paths
    paths=$(jq -r ".\"$dir\".paths[]" versions.json)

    # echo them
    echo "--------------------------------"
    echo "Repository: $repo_url"
    echo "Commit: $commit_hash"
    echo "Paths: $paths"

    # Download the entire repository at temp directory
    temp_dir=temp
    git clone "$repo_url" "$temp_dir"
    cd "$temp_dir"
    git checkout "$commit_hash"
    cd ..

    # Copy the files to the assets directory
    for path in $paths; do
        mkdir -p "assets/$dir/$(dirname "$path")"
        cp -r "$temp_dir/$path" "assets/$dir/$path"
    done

    # Remove the temp directory
    rm -rf "$temp_dir"

    echo ""
done
