# Building systemd rpms for local development using rpmbuild --build-in-place

This approach is based on filbranden's [git-rpmbuild](https://github.com/filbranden/git-rpmbuild)
and his [talk during ASG2019](https://www.youtube.com/watch?v=fVM1kJrymRM).

```
git clone https://github.com/systemd/systemd
fedpkg clone systemd fedora-systemd
cd systemd
rpmbuild -bb --build-in-place --noprep --define "_sourcedir $PWD/../fedora-systemd" --define "_rpmdir $PWD/rpms" --with inplace ../fedora-systemd/systemd.spec
sudo dnf upgrade --setopt install_weak_deps=False rpms/*/*.rpm
```

`--without lto` and `--without tests` may be useful to speed up the build.
