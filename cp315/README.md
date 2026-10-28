# pyyaml-cp315

This branch publishes [`pyyaml-cp315`](https://pypi.org/project/pyyaml-cp315/) on PyPI: PyYAML 6.0.3, unmodified, with
CPython 3.15 wheels (`cp315` and `cp315t`), until PyYAML publishes its own
([yaml/pyyaml#981](https://github.com/yaml/pyyaml/issues/981)).

Without a wheel, installers build PyYAML from its sdist. That build needs a C compiler and the libyaml headers, and when
they are missing it silently falls back to a pure Python install, without `yaml.CSafeLoader` and the other libyaml
classes.

## What differs from PyYAML 6.0.3

The branch starts from upstream's `release/6.0` branch: the 6.0.3 release, plus upstream's CI update for 3.15.

- `setup.py`: the distribution name, and metadata (description, URLs, 3.15 classifier). The library code and the
  `yaml` and `_yaml` packages are unchanged.
- The CI is replaced by [`cp315.yml`](../.github/workflows/cp315.yml), which only builds the 3.15 wheels:
  - The sdist and the wheels are built without isolation, with the build dependencies hash-pinned in
    [`build-requirements.txt`](build-requirements.txt).
  - libyaml 0.2.5, the version PyYAML's own wheels bundle, is downloaded with a hash check and linked statically.
  - Every wheel is checked to be built with the libyaml extension, and is tested with PyYAML's test suite.
  - The sdist and wheels carry build provenance attestations, verified before publishing.

| Python | Platforms |
|---|---|
| 3.15, 3.15t | manylinux and musllinux (x86_64, aarch64), macOS (arm64, x86_64) |

Other platforms install from the sdist.

## Usage

`pyyaml-cp315` provides the same `yaml` package as PyYAML, so the two can't be installed together, and other packages
keep depending on `pyyaml`. With uv, exclude `pyyaml` from the resolution and depend on `pyyaml-cp315` instead:

```toml
[project]
dependencies = ["pyyaml-cp315==6.0.3"]

[tool.uv]
exclude-dependencies = ["pyyaml"]
```

Once PyYAML publishes 3.15 wheels on PyPI, go back to `pyyaml` and remove the exclusion.

## Releasing

Push a `cp315-<version>` tag (`cp315-6.0.3`): the tag must match the version in `setup.py`. After an approval on the
`release` environment, the release job publishes the sdist and the wheels to PyPI with trusted publishing.

To regenerate `build-requirements.txt`, run the command at its top.

## Repository setup

- Create a `release` environment with required reviewers, and a trusted publisher on PyPI for the `cp315.yml` workflow
  and the `release` environment.
- Protect `cp315-*` tags with a ruleset.
