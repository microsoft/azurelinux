FROM mcr.microsoft.com/azurelinux/base/core:3.0

RUN tdnf install -y curl ca-certificates tar gzip git azurelinux-repos-extended && \
    curl -fsSL https://gh.io/copilot-install | bash && \
    curl -fsSL https://cli.github.com/packages/rpm/gh-cli.repo -o /etc/yum.repos.d/gh-cli.repo && \
    tdnf install -y gh python3-pip && \
    pip3 install --no-cache-dir mcp python-dotenv && \
    tdnf clean all

RUN mkdir -p /home/copilot && chmod 777 /home/copilot

ENTRYPOINT ["copilot"]
