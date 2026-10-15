FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      openssh-server fail2ban rsyslog iptables procps iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Test user (lab only!)
RUN useradd -m -s /bin/bash testuser && echo 'testuser:S3cretPass!' | chpasswd
RUN sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config \
 && sed -i '/imklog/d' /etc/rsyslog.conf

COPY jail.local /etc/fail2ban/jail.local
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 22
ENTRYPOINT ["/entrypoint.sh"]
