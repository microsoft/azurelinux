FROM mcr.microsoft.com/azurelinux/base/core:3.0

COPY requirements.txt /tmp/requirements.txt
RUN tdnf install -y curl ca-certificates tar gzip git npm python3-pip azurelinux-repos-extended && \
    curl -fsSL https://cli.github.com/packages/rpm/gh-cli.repo -o /etc/yum.repos.d/gh-cli.repo && \
    tdnf install -y gh && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt && \
    tdnf clean all && \
    npm install -g @github/copilot

# 777 needed because the container runs as an arbitrary UID via -u $(id -u):$(id -g)
RUN mkdir -p /home/copilot && chmod 777 /home/copilot

ENTRYPOINT ["copilot"]
