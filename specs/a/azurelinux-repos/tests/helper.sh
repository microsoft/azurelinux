#!/bin/sh
# Shared local fixtures let trust and outage tests control package availability
# without depending on live services. RPMs contain only a harmless marker file
# and are deliberately unsigned; repository queries do not require signatures,
# while the trust test expects installation to reject the unsigned package.
# Callers source ../helper.sh and remove the fixture directories after testing.
# azl_make_rpm NAME VERSION OUTDIR : build a tiny noarch, UNSIGNED rpm providing /usr/share/NAME/marker
azl_make_rpm() {
  _n=$1; _v=$2; _out=$3
  _top=$(mktemp -d)
  mkdir -p "$_top/SPECS" "$_out"
  cat > "$_top/SPECS/$_n.spec" <<EOF
Name: $_n
Version: $_v
Release: 1
Summary: azurelinux-repos test fixture $_n
License: MIT
BuildArch: noarch
%description
fixture
%install
mkdir -p %{buildroot}/usr/share/$_n
echo $_n > %{buildroot}/usr/share/$_n/marker
%files
/usr/share/$_n/marker
EOF
  rpmbuild -bb --define "_topdir $_top" --define '_rpmdir %{_topdir}/RPMS' "$_top/SPECS/$_n.spec" >/dev/null 2>&1 || { rm -rf "$_top"; return 1; }
  find "$_top/RPMS" -name '*.rpm' -exec cp {} "$_out"/ \;
  rm -rf "$_top"
}
# azl_make_repo DIR : generate repodata
azl_make_repo() { createrepo_c -q "$1" >/dev/null; }
