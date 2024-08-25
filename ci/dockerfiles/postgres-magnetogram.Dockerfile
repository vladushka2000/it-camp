FROM postgres:16.0

ENV POSTGRES_DB "magnetogram"
ENV POSTGRES_USER "admin"
ENV POSTGRES_PASSWORD "admin"
ENV PGDATA /data/postgres

EXPOSE 5431

VOLUME postgres:/data/postgres
