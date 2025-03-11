FROM debian:bookworm-slim

ARG DEB_VERSION="0.8.33-1"
ARG DEB_CONF_SERVER="mysql-8.0"

RUN cd /tmp \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends lsb-release wget gnupg ca-certificates \
    && wget -O mysql-apt-config.deb https://dev.mysql.com/get/mysql-apt-config_${DEB_VERSION}_all.deb \
    && echo "mysql-apt-config mysql-apt-config/select-server string ${DEB_CONF_SERVER}" | debconf-set-selections \
    && DEBIAN_FRONTEND=noninteractive dpkg -i mysql-apt-config.deb \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends mysql-community-client mysql-shell \
    && rm -rf /tmp/* /var/tmp/* \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/log/apt/* \
    && rm -rf /var/log/dpkg.log \
    && rm -rf /var/log/bootstrap.log \
    && rm -rf /var/log/alternatives.log

CMD ["/usr/bin/mysqlsh"]
