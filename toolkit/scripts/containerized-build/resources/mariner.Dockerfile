ARG version
FROM mcr.microsoft.com/cbl-mariner/tmp_pkgbuild_${version}
ARG version
ARG mode
ARG enable_local_repo
ARG topdir

COPY resources/_local_repo /etc/yum.repos.d/local_repo.not_a_repo
COPY build_container/welcome.txt /mariner_docker_stuff/welcome.txt
COPY resources/add_shell_functions.txt /mariner_docker_stuff/add_shell_functions.txt
RUN sed -i "s~<SPECS_DIR>~${topdir}/SPECS~" /mariner_docker_stuff/add_shell_functions.txt
RUN sed -i "s~<SOURCES_DIR>~${topdir}/SOURCES~" /mariner_docker_stuff/add_shell_functions.txt
RUN sed -i "s~<RPMS_DIR>~${topdir}/RPMS~" /mariner_docker_stuff/add_shell_functions.txt

COPY resources/builder_splash.txt /mariner_docker_stuff/splash.txt

RUN echo "alias tdnf='tdnf --releasever=$version'"              >> /root/.bashrc && \
    echo "tdnf install -y dnf dnf-plugins-core > /dev/null"     >> /root/.bashrc && \
    cat /mariner_docker_stuff/add_shell_functions.txt           >> /root/.bashrc && \
    echo "cat /mariner_docker_stuff/splash.txt"                 >> /root/.bashrc && \
    echo "cat /mariner_docker_stuff/welcome.txt"                >> /root/.bashrc && \
    echo "if [[ ! -L /repo ]]; then ln -s /mnt/RPMS/ /repo; fi" >> /root/.bashrc && \
    echo "cd  /repo"                                            >> /root/.bashrc

#if enable_local_repo is set to true
RUN if [[ "${enable_local_repo}" == "true" ]]; then echo "enable_local_repo" >> /root/.bashrc; fi
