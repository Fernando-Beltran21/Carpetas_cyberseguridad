FROM alpine:3.20
RUN apk add --no-cache bash openssh-client sshpass netcat-openbsd
COPY attack.sh /attack.sh
RUN chmod +x /attack.sh
CMD ["sleep", "infinity"]
