# How to bundle nodejs libraries in Fedora

The upstream Node.js stance on 
[global library packages](https://nodejs.org/en/blog/npm/npm-1-0-global-vs-local-installation/) 
is that they are ".. best avoided if not needed."  In Fedora, we take the same 
stance with our nodejs packages.  You can provide a package that uses nodejs, 
but you should bundle all the nodejs libraries that are needed.

We are providing a sample spec file and bundling script here.  
For more detailed packaging information go to the 
[Fedora Node.js Packaging Guildelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/Node.js/)

## Bundling Script

```
nodejs-packaging-bundler <npm_name> [version] [tarball]
```

nodejs-packaging-bundler is it's own package, nodejs-packaging-bundler and must be installed before use.  
nodejs-packaging-bundler gets the latest npm version available, if no version is given, or uses the existing tarball if one is given. Using npm is preferred for to ease reproducibility. If a local tarball is required (e.g. because the package is missing from npm or its version is too old), please ensure to document how the tarball was created.
It produces four files and puts them in ${HOME}/rpmbuild/SOURCES

 * <npm_name>-<version>.tgz - This is the tarball from npm.org
 * <npm_name>-<version>-nm-prod.tgz - This is the tarball that contains all the bundled nodejs modules <npm_name> needs to run
 * <npm_name>-<version>-nm-dev.tgz - This is the tarball that contains all the bundled nodejs modules <npm_name> needs to test
 * <npm_name>-<version>-bundled-licenses.txt - This lists the bundled licenses in <npm_name>-<version>-nm-prod.tgz

## Sample Spec File

```
%global npm_name my_nodejs_application
...
License:  <license1> and <license2> and <license3>
...
Source0:  http://registry.npmjs.org/%{npm_name}/-/%{npm_name}-%{version}.tgz
Source1:  %{npm_name}-%{version}-nm-prod.tgz
Source2:  %{npm_name}-%{version}-nm-dev.tgz
Source3:  %{npm_name}-%{version}-bundled-licenses.txt
...
BuildRequires: nodejs-devel
...
%prep
%setup -q -n package
cp %{SOURCE3} .
...
%build
# Setup bundled node modules
tar xfz %{SOURCE1}
mkdir -p node_modules
pushd node_modules
ln -s ../node_modules_prod/* .
ln -s ../node_modules_prod/.bin .
popd
...
%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pr index.js lib package.json %{buildroot}%{nodejs_sitelib}/%{npm_name}
# Copy over bundled nodejs modules
cp -pr node_modules node_modules_prod %{buildroot}%{nodejs_sitelib}/%{npm_name}
...
%check
%nodejs_symlink_deps --check
# Setup bundled dev node_modules for testing
tar xfz %{SOURCE2}
pushd node_modules
ln -s ../node_modules_dev/* .
popd
pushd node_modules/.bin
ln -s ../../node_modules_dev/.bin/* .
popd
# Example test run using the binary in ./node_modules/.bin/
./node_modules/.bin/vows --spec --isolate
...
%files
%doc HISTORY.md
%license LICENSE.md %{npm_name}-%{version}-bundled-licenses.txt
%{nodejs_sitelib}/%{npm_name}
```

