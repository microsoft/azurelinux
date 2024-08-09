Summary:        Basic system utilities; reimplemented in Rust
Name:	        rust-coreutils
Version:	    0.0.26
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/uutils/coreutils
Source0: 	    %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a automatically created tarball with no download link.
Source1:	    rust-coreutils-0.0.26-vendored.tar.gz
Source2:        cargo_config.toml


BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  glibc
Conflicts:  coreutils

%description
This package provides the reimplementation of the GNU core utilities in Rust.

%prep
%setup -q -n coreutils-%{version}
tar --strip-components=1 -xzf %{SOURCE1}
install -D %{SOURCE2} .cargo/config

%build
cargo build --release --offline

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}


utilities=(
    "uniq" "nl" "echo" "shred" "od" "basename" "cat" "split" "md5sum" "shake256sum"
    "tr" "dir" "comm" "pwd" "tee" "head" "ls" "sort" "b3sum" "b2sum"
    "printf" "vdir" "test" "dd" "cut" "df" "shuf" "csplit" "ln"
    "numfmt" "mv" "mktemp" "yes" "pr" "seq" "tail" "sha1sum" "sha224sum"
    "touch" "tac" "basenc" "rmdir" "paste" "sha256sum" "sha3-256sum"
    "dirname" "base32" "factor" "printenv" "sleep" "readlink" "sha3-224sum"
    "du" "truncate" "more" "dircolors" "link" "date" "sum" "false"
    "true" "wc" "mkdir" "expand" "hashsum" "sha3-384sum" "sha512sum"
    "cksum" "base64" "unlink" "fold" "expr" "join" "rm" "sha3-512sum" "shake128sum"
    "ptx" "realpath" "unexpand" "fmt" "env" "tsort" "cp" "sha384sum" "sha3sum"
)

pushd %{buildroot}%{_bindir}
for util in "${utilities[@]}"; do 
    ln -sf coreutils ${util}
done
popd


%files
%{_bindir}/coreutils
%{_bindir}/b2sum
%{_bindir}/b3sum
%{_bindir}/base32
%{_bindir}/base64
%{_bindir}/basename
%{_bindir}/basenc
%{_bindir}/cat
%{_bindir}/cksum
%{_bindir}/comm
%{_bindir}/cp
%{_bindir}/csplit
%{_bindir}/cut
%{_bindir}/date
%{_bindir}/dd
%{_bindir}/df
%{_bindir}/dir
%{_bindir}/dircolors
%{_bindir}/dirname
%{_bindir}/du
%{_bindir}/echo
%{_bindir}/env
%{_bindir}/expand
%{_bindir}/expr
%{_bindir}/factor
%{_bindir}/false
%{_bindir}/fmt
%{_bindir}/fold
%{_bindir}/hashsum
%{_bindir}/head
%{_bindir}/join
%{_bindir}/link
%{_bindir}/ln
%{_bindir}/ls
%{_bindir}/md5sum
%{_bindir}/mkdir
%{_bindir}/mktemp
%{_bindir}/more
%{_bindir}/mv
%{_bindir}/nl
%{_bindir}/numfmt
%{_bindir}/od
%{_bindir}/paste
%{_bindir}/pr
%{_bindir}/printenv
%{_bindir}/printf
%{_bindir}/ptx
%{_bindir}/pwd
%{_bindir}/readlink
%{_bindir}/realpath
%{_bindir}/rm
%{_bindir}/rmdir
%{_bindir}/seq
%{_bindir}/sha1sum
%{_bindir}/sha224sum
%{_bindir}/sha256sum
%{_bindir}/sha3-224sum
%{_bindir}/sha3-256sum
%{_bindir}/sha3-384sum
%{_bindir}/sha3-512sum
%{_bindir}/sha384sum
%{_bindir}/sha3sum 
%{_bindir}/sha512sum
%{_bindir}/shake128sum
%{_bindir}/shake256sum
%{_bindir}/shred
%{_bindir}/shuf
%{_bindir}/sleep
%{_bindir}/sort
%{_bindir}/split
%{_bindir}/sum
%{_bindir}/tac
%{_bindir}/tail
%{_bindir}/tee
%{_bindir}/test
%{_bindir}/touch
%{_bindir}/tr
%{_bindir}/true
%{_bindir}/truncate
%{_bindir}/tsort
%{_bindir}/unexpand
%{_bindir}/uniq
%{_bindir}/unlink
%{_bindir}/vdir
%{_bindir}/wc
%{_bindir}/yes

%changelog 
* Fri May 31 2024 Antonio Salinas t-ansalinas@microsoft.com - 0.0.26
    - Intgrated Rust implementation of GNU coreutils.

