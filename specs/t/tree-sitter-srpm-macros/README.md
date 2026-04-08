# tree-sitter-srpm-macros

RPM macros for Tree-sitter parsers.

## Macros

### Specifying the build system

Declare that this is a Tree-sitter parser with:

```specfile
BuildSystem: tree_sitter
```

The `%prep`, `%conf`, `%generate_buildrequires`, `%build`, `%install`
and `%check` sections will all be provided for you.

This requires RPM version 4.20 (i.e., Fedora 41) or greater.

### Defining packages and their contents


Generate `%package` and `%files` sections for the subpackages built from your package:

```specfile
%{tree_sitter -l language-name [-P] [-R]}
```

Here, _language-name_ is the human-friendly name(s) of the Language
parser(s) provided by this package, to be mentioned in the package
summaries and descriptions.

#### Python and Rust subpackages

> [!WARNING]
> This feature is experimental.

You can build subpackages for Python or Rust bindings by passing `--with=python` or `--with=rust` respectively to `rpmbuild`.  Alternatively, you can pass the `-P` or `-R` options to the `tree_sitter` macro, which will do the same thing.

## Example spec file

```specfile
Name:           tree-sitter-typescript
Version:        0.21.2
Release:        %autorelease
License:        MIT
URL:            https://github.com/tree-sitter/%{name}
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildSystem:    tree_sitter

%{tree_sitter -l %{quote:TypeScript and TSX}}

%changelog
%autochangelog
```
