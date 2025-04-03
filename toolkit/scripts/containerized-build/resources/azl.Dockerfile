ARG container_img
FROM ${container_img}
ARG version
ARG enable_local_repo
ARG azl_repo
ARG mode
ARG packages_to_install
LABEL containerized-rpmbuild=$azl_repo/build

COPY resources/local_repo /etc/yum.repos.d/local_repo.disabled_repo
COPY resources/macros.with-check /usr/lib/rpm/macros.d

RUN echo "source /azl_setup_dir/setup_functions.sh"          >> /root/.bashrc && \
    echo "if [[ ! -L /repo ]]; then ln -s /mnt/RPMS/ /repo; fi"  >> /root/.bashrc

#if enable_local_repo is set to true
RUN if [[ "${enable_local_repo}" == "true" ]]; then echo "enable_local_repo" >> /root/.bashrc; fi

RUN echo "cat /azl_setup_dir/splash.txt"                     >> /root/.bashrc && \
    echo "show_help"                                         >> /root/.bashrc

RUN if [[ "${mode}" == "build" ]]; then echo "cd /usr/src/azl || { echo \"ERROR: Could not change directory to /usr/src/azl \"; exit 1; }"  >> /root/.bashrc; fi
RUN if [[ "${mode}" == "test" ]]; then echo "cd /mnt || { echo \"ERROR: Could not change directory to /mnt \"; exit 1; }"  >> /root/.bashrc; fi

# Install packages from bashrc so we can use the previously setup tdnf defaults.
RUN echo "echo installing packages ${packages_to_install}" >> /root/.bashrc && \
    echo "tdnf install --releasever=${version} -qy ${packages_to_install}" >> /root/.bashrc
