# Check Environment Values
This Github action perform a validation of environment variables in deployment


## Parameters

| Name        | Description                            | Required |
|-------------|----------------------------------------|----------|
|    addr     | ADDR, e.g: https://my.example.com:2345 |   True   |
|    token    | TOKEN to use in ADDR                   |   True   |
| root_engine | Root Engine Path                       |   True   |

## Dependencies

munditrade/get-changed-files

## Usage

- Usage in your workflow is like following example:

```yaml
name: MyWorkflow

on:
  push:

jobs:
  myexamplejob:
    runs-on: ubuntu-latest
    name: dosomething
    steps:
      - name: Check Envs
        uses: munditrade/action-check-envs@main
        id: check
        with:
          addr: ${{ secrets.ADDR }}
          token: ${{ secrets.TOKEN }}
          root_engine: ${{ secrets.ROOT_ENGINE }}

```
