FROM cgr.dev/chainguard/minio:latest AS minio-bin
FROM cgr.dev/chainguard/minio-client:latest AS mc-bin

FROM alpine:3.20

RUN apk add --no-cache curl ca-certificates bash

COPY --from=minio-bin /usr/bin/minio /usr/bin/minio
COPY --from=mc-bin /usr/bin/mc /usr/bin/mc
COPY init-minio.sh /usr/bin/init-minio.sh

RUN chmod +x /usr/bin/minio /usr/bin/mc /usr/bin/init-minio.sh

ENTRYPOINT ["/bin/sh", "/usr/bin/init-minio.sh"]

