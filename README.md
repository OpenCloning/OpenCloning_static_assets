# OpenCloning Static Assets

This repository manages and aggregates static assets from various OpenCloning-related repositories. It serves as a centralized location for accessing and serving important data files and resources used across the OpenCloning tools.

## Purpose

This repository collects and organizes static assets from multiple repositories (more to come):
- SnapGene crawler data
- SEVA plasmids index
- Annotated iGEM distribution
- OpenCloning submission data

## Building

Just run `./get_assets.sh` to fetch the latest versions. It needs `jq` and `git` to be installed.

The repositories, commits and paths pulled are defined in the `versions.json` file.

## Structure

The build will generate the following directory structure for a static site:

```
assets/
├── SnapGene_crawler/
│   └── index.json
├── seva_plasmids_index/
│   └── index.json
├── annotated-igem-distribution/
│   ├── results/
│   │   ├── index.json
│   │   └── plasmids/
├── OpenCloning-submission/
│   ├── index.json
│   └── processed/
├── ...
└── index.html
```

### Asset Sources

The assets are pulled from the following repositories at specific commits:

- **SnapGene_crawler**: Repository for SnapGene data crawling
- **seva_plasmids_index**: SEVA plasmids database
- **annotated-igem-distribution**: iGEM distribution data with annotations
- **OpenCloning-submission**: OpenCloning submission data


## Adding new entries

To add a new entry to the `versions.json` file, you need to add the following information:

- `repository`: The URL of the repository
- `commit`: The commit hash to pull
- `paths`: The paths to pull from the repository

The `paths` are relative to the repository root.

## Deployment

For now, I am just doing manual deployments to netlify. If it gets updated more often, I will set up a CI/CD pipeline.
