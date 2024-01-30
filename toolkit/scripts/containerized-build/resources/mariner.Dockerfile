ARG container_img
FROM ${container_img}
ARG version
ARG enable_local_repo
ARG mariner_repo
ARG mode
ARG extra_packages
LABEL containerized-rpmbuild=$mariner_repo/build

COPY resources/local_repo /etc/yum.repos.d/local_repo.disabled_repo

RUN echo "alias tdnf='tdnf --releasever=$version'"               >> /root/.bashrc && \
    echo "source /mariner_setup_dir/setup_functions.sh"          >> /root/.bashrc && \
    echo "if [[ ! -L /repo ]]; then ln -s /mnt/RPMS/ /repo; fi"  >> /root/.bashrc

#if enable_local_repo is set to true
RUN if [[ "${enable_local_repo}" == "true" ]]; then echo "enable_local_repo" >> /root/.bashrc; fi

RUN echo "cat /mariner_setup_dir/splash.txt"                     >> /root/.bashrc && \
    echo "show_help"                                             >> /root/.bashrc

RUN if [[ "${mode}" == "build" ]]; then echo "cd /usr/src/mariner || { echo \"ERROR: Could not change directory to /usr/src/mariner \"; exit 1; }"  >> /root/.bashrc; fi
RUN if [[ "${mode}" == "test" ]]; then echo "cd /mnt || { echo \"ERROR: Could not change directory to /mnt \"; exit 1; }"  >> /root/.bashrc; fi

# TODO: Remove when PMC is available for 3.0
RUN if [[ "${version}" == "3.0" ]]; then echo "enable_mariner3_repo $extra_packages"  >> /root/.bashrc; else tdnf --releasever=$version install -y vim git $extra_packages ; fi

# TODO: Re-enable when PMC is available for 3.0
# Install vim & git in the build env
#RUN tdnf --releasever=$version install -y vim git $extra_packages
