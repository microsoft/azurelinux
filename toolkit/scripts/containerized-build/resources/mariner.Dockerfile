ARG version
FROM mcr.microsoft.com/cbl-mariner/tmp_pkgbuild_${version}
ARG version
ARG mode
ARG enable_local_repo
ARG topdir
ARG mariner_repo

COPY resources/_local_repo /etc/yum.repos.d/local_repo.not_a_repo
COPY build_container/depsearch /mariner_docker_stuff/
COPY build_container/grapher /mariner_docker_stuff/
COPY build_container/specreader /mariner_docker_stuff/
COPY build_container/graph.dot /mariner_docker_stuff/
COPY build_container/welcome.txt /mariner_docker_stuff/welcome.txt
COPY resources/add_shell_functions.txt /mariner_docker_stuff/add_shell_functions.txt
RUN sed -i "s~<TOPDIR>~${topdir}~" /mariner_docker_stuff/add_shell_functions.txt

COPY resources/builder_splash.txt /mariner_docker_stuff/splash.txt

RUN echo "alias tdnf='tdnf --releasever=$version'"              >> /root/.bashrc && \
    cat /mariner_docker_stuff/add_shell_functions.txt           >> /root/.bashrc && \
    echo "cat /mariner_docker_stuff/splash.txt"                 >> /root/.bashrc && \
    echo "cat /mariner_docker_stuff/welcome.txt"                >> /root/.bashrc && \
    echo "if [[ ! -L /repo ]]; then ln -s /mnt/RPMS/ /repo; fi" >> /root/.bashrc && \
    echo "cd  /repo"                                            >> /root/.bashrc && \
    echo "export 'PS1=\e[0m$mariner_repo:\e[34m\$(pwd)\\e[30m$'" >> /root/.bashrc

#if enable_local_repo is set to true
RUN if [[ "${enable_local_repo}" == "true" ]]; then echo "enable_local_repo" >> /root/.bashrc; fi
