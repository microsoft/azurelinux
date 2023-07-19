ARG container_img
FROM ${container_img}
ARG version
ARG enable_local_repo
ARG topdir
ARG mariner_repo
ARG mariner_branch
ARG splash_txt
LABEL containerized-rpmbuild=$mariner_repo/build

COPY resources/_local_repo /etc/yum.repos.d/local_repo.not_a_repo
COPY resources/welcome.txt /mariner_setup_dir/
RUN sed -i "s~<REPO_PATH>~${mariner_repo}~" /mariner_setup_dir/welcome.txt
RUN sed -i "s~<REPO_BRANCH>~${mariner_branch}~" /mariner_setup_dir/welcome.txt
COPY resources/setup_functions.sh /mariner_setup_dir/setup_functions.sh
RUN sed -i "s~<TOPDIR>~${topdir}~" /mariner_setup_dir/setup_functions.sh
COPY resources/$splash_txt /mariner_setup_dir/splash.txt
COPY build_container/depsearch /mariner_setup_dir/
COPY build_container/grapher /mariner_setup_dir/
COPY build_container/specreader /mariner_setup_dir/
COPY build_container/graph.dot /mariner_setup_dir/
COPY build_container/mounts.txt /mariner_setup_dir/

RUN echo "alias tdnf='tdnf --releasever=$version'"               >> /root/.bashrc && \
    echo "source /mariner_setup_dir/setup_functions.sh"          >> /root/.bashrc && \
    echo "if [[ ! -L /repo ]]; then ln -s /mnt/RPMS/ /repo; fi"  >> /root/.bashrc

#if enable_local_repo is set to true
RUN if [[ "${enable_local_repo}" == "true" ]]; then echo "enable_local_repo" >> /root/.bashrc; fi

RUN echo "cat /mariner_setup_dir/splash.txt"                     >> /root/.bashrc && \
    echo "show_help"                                             >> /root/.bashrc && \
    echo "cd /usr/src/mariner/"                                  >> /root/.bashrc
