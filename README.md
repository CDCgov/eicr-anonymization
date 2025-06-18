
# eICR Anonymization Tool
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> [!CAUTION]
> This tool should be considered in an early **alpha** (not feature complete) state. At this stage, you should assume sensitive data will be left in, or otherwise inappropriately removed or replaced. Every anonymized eICR should be thoroughly checked for sensitive data.

## Overview
This tool removes and replaces sensitive data in eICR XML files with fake Star Wars–themed data. Its aim is to preserve the original structure, formatting, and relationships in real-world eICRs so that the resulting files can still be helpful for testing and development. By replacing data with plausible but clearly fictitious values, it becomes possible to share eICRs for troubleshooting or collaboration without exposing private information.

### Problem Scope
Electronic Initial Case Reports (eICRs) contain sensitive patient information that cannot be shared or used freely for development and testing without serious privacy precautions. While fabricated eICRs can be used, these often fail to capture the quirks and irregularities of actual data. As a result:

- Developers must make assumptions when working solely with fabricated examples, potentially missing real-world edge cases.
- Users experiencing issues cannot safely share the exact eICRs related to the problem.
- Simple anonymization methods often remove or alter key data patterns and formatting, inadvertently making the files less representative of real-world data or otherwise unusable.

Therefore, there is a need for a tool that removes or replaces sensitive data while preserving as much of the document's original “flavor” as possible, adhering to anonymization best practices without sacrificing realism.

### Goals
The tool is designed around the following principles and requirements, in approximate order of importance:
1. **Adhere to De-Identification Best Practices**
   - The resulting eICR document should at least satisfy the [Safe Harbor method of de-identification](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html#safeharborguidance).
2. **Plausible Yet Clearly Fake Data:**
   - Substituted information should look realistic enough to test real-world scenarios but still be obviously fictional to avoid confusion with actual, sensitive data.
3. **Preserve Formatting:**
   - Maintain case, including uppercase, lowercase, and titlecase.
   - Keep whitespace, including leading and trailing spaces.
   - Retain punctuation, symbols, and other special characters.
4. **Consistent Replacement:**
   - Whenever the same value appears multiple times, it should be replaced by the same placeholder.
   - This includes when a value is formatted differently across instances.

## How to Use

### Requirements

#### Required
- [Python version >= 3.7](https://www.python.org/)
- [Pip (should be installed alongside Python)](http://pip.pypa.io/en/stable/)

#### Recommended
If using the anonymization tool as a command-line tool outside of a Python virtual environment, it is recommended to use [Pipx](https://pipx.pypa.io/stable/) to avoid dependency conflicts.

### Installation
1. Clone this repo.
2. Install:
   At the root of the directory
   - With Pip:
   ```bash
   pip install .
   ```
   - With Pipx:
   ```bash
   pipx install .
   ```

### Use
#### Basic Usage
```bash
anonymize_eicr /path/to/eicrs
```
This will create a copy of each eicr file prepended with `.anonymized.xml` in the same directory.

#### Patient Only Configuration
```bash
anonymize_eicr /path/to/eicrs --patient_only
```
In some cases the default behavior of the anonymizer may be too aggressive. The patient only configuration will keep all data, apart from data directly related to the patient (name, date of birth, contact, guardian, etc), dates related to the patient encounter, and clinical notes.

#### Help
```bash
anonymize --help
usage: anonymize_eicr [-h] [--debug] input_location

Anonymize eICR XML files.

positional arguments:
  input_location  Directory containing eICR XML files.

options:
  -h, --help      show this help message and exit
  --debug, -d     Print table showing original and replacement tags. Will show sensitive information.
```

### Development
#### Required
- [uv (Python package manager)](https://docs.astral.sh/uv/)

#### Set Up
1. This repo uses `uv` as the Python package manager. Install at the root of the directory
   - With Pip:
   ```bash
   pip install uv
   ```
    - With Pipx:
   ```bash
   pipx install uv
   ```
2. Install dependencies with `uv`:
   ```bash
   uv sync
   ```

#### Run unit/snapshot tests
```bash
uv run pytest
```
To update snapshot tests, run:
```bash
uv run pytest --snapshot-update
```

#### Add dependencies
```bash
uv add <dependency>
```
This is used for runtime dependencies. Add the `--dev` flag if you're adding is a development-only dependency.

#### Updating CDA Structure YAML
The `cda_structure.yaml` is created by running `uv run tools/cda_structure_generator.py`. To run that script the JSON FHIR `StructureDefinition`s for CDA need to be [downloaded from hl7](https://build.fhir.org/ig/HL7/CDA-core-2.0/downloads.html) and unzipped into `tools/definitions`.

#### Debugging
You can add the following flags to `uv run anonymize_eicr /path/to/file` to help with debugging:
```bash
  -d, --debug                Print table showing original and replacement tags. Will show sensitive information.
  -s, --seed [SEED]          Set the random seed. If no value is provided, the seed will be set to `1`.
  --siso, --same_in_same_out The same value will always be replaced with the same new value regardless of run or seed. This will set the seed to its default `1`, if a seed is not provided
```

## Related documents

* [Open Practices](open_practices.md)
* [Rules of Behavior](rules_of_behavior.md)
* [Disclaimer](DISCLAIMER.md)
* [Contribution Notice](CONTRIBUTING.md)
* [Code of Conduct](code-of-conduct.md)

## Public Domain Standard Notice
This repository constitutes a work of the United States Government and is not
subject to domestic copyright protection under 17 USC § 105. This repository is in
the public domain within the United States, and copyright and related rights in
the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
All contributions to this repository will be released under the CC0 dedication. By
submitting a pull request you are agreeing to comply with this waiver of
copyright interest.

## License Standard Notice
The repository utilizes code licensed under the terms of the Apache Software
License and therefore is licensed under ASL v2 or later.

This source code in this repository is free: you can redistribute it and/or modify it under
the terms of the Apache Software License version 2, or (at your option) any
later version.

This source code in this repository is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the Apache Software License for more details.

You should have received a copy of the Apache Software License along with this
program. If not, see http://www.apache.org/licenses/LICENSE-2.0.html

The source code forked from other open source projects will inherit its license.

## Privacy Standard Notice
This repository contains only non-sensitive, publicly available data and
information. All material and community participation is covered by the
[Disclaimer](DISCLAIMER.md)
and [Code of Conduct](code-of-conduct.md).
For more information about CDC's privacy policy, please visit [http://www.cdc.gov/other/privacy.html](https://www.cdc.gov/other/privacy.html).

## Contributing Standard Notice
Anyone is encouraged to contribute to the repository by [forking](https://help.github.com/articles/fork-a-repo)
and submitting a pull request. (If you are new to GitHub, you might start with a
[basic tutorial](https://help.github.com/articles/set-up-git).) By contributing
to this project, you grant a world-wide, royalty-free, perpetual, irrevocable,
non-exclusive, transferable license to all users under the terms of the
[Apache Software License v2](http://www.apache.org/licenses/LICENSE-2.0.html) or
later.

All comments, messages, pull requests, and other submissions received through
CDC including this GitHub page may be subject to applicable federal law, including but not limited to the Federal Records Act, and may be archived. Learn more at [http://www.cdc.gov/other/privacy.html](http://www.cdc.gov/other/privacy.html).

## Records Management Standard Notice
This repository is not a source of government records, but is a copy to increase
collaboration and collaborative potential. All government records will be
published through the [CDC web site](http://www.cdc.gov).

## Additional Standard Notices
Please refer to [CDC's Template Repository](https://github.com/CDCgov/template) for more information about [contributing to this repository](https://github.com/CDCgov/template/blob/main/CONTRIBUTING.md), [public domain notices and disclaimers](https://github.com/CDCgov/template/blob/main/DISCLAIMER.md), and [code of conduct](https://github.com/CDCgov/template/blob/main/code-of-conduct.md).
