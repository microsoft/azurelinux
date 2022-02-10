---
title: "Extending Mariner with Mock"
categories:
  - Blog
author: Rachel Menge and Cameron Baird
---

## Why Mock

There are several reasons why we would want to use Mock to build Mariner rpms. First, Mock makes it easy for developers and customers to build and/or debug individual rpms. Since it is not running all the build tools, the builds tend to be quicker and can be configured to preserve the chroot for debugging. Because we don't always have control of the development environment, a containerized environment helps ensure a consistent, reproducible setup.

We could run rpmbuild directly in the container, but this requires additional steps to install necessary dependencies, and we want to minimize these developer requirements.

Because Mariner does not (yet) support the mock rpm, we run mock within a Fedora 35 container. We created a Dockerfile to help spin up this container since mock has specific requirements for its user.

```
git clone git@github.com:rlmenge/mariner-mock.git
cd /local/path/to/mariner-mock  # Dockerfile location
docker build -t mock-tester .
sudo docker run --privileged -v /local/path/to/mariner-mock:/mockfiles -it mock-tester:latest /bin/bash
```

For this container to work properly, the `--privileged` option is required to deal with various tmpfs mounts created by mock.
Once in the container, mock will manage the rpm builds, dependencies and logging.

```
# Run mock (inside the container)
# Run init once upon entering the container
mock -r /etc/mock/mariner-1-x86_64.cfg --init 
mock -r /etc/mock/mariner-1-x86_64.cfg --no-cleanup-after --rpmbuild-opts=--noclean <srpm>
```

Running mock like this should give you output similar to the example image below.
![Example mock output]({{site.baseurl}}/assets/images/mock-blog-example.png)

The resulting files are:
 * state.log shows high level commands mock ran
 * root.log shows the packages mock installed in the chroot
 * build.log is the output of the rpmbuild on the src.rpm in the chroot.

In the short term, we will want to upstream out .tpl and .cfg files to the Mock upstream so they're readily available to users who want to extend Mariner functionality. Parallel to that work will be the process of adding mock and its dependencies to the Mariner distribution.

This work was done by Rachel Menge and Cameron Baird as a part of an internal hackathon project.

## Links

 * [Mock](https://github.com/rpm-software-management/mock/tree/main/mock) source code on GitHub.
 * [Mock Documentation](https://rpm-software-management.github.io/mock/)
 * [Fedora's mock guide](https://fedoraproject.org/wiki/Using_Mock_to_test_package_builds) is older, but still helpful for quick examples.
 * [Mariner-mock](https://github.com/rlmenge/mariner-mock) The Mariner-mock work is available here until it's merged into the distribution.
