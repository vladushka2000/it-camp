FROM postgres:16.0

ENV POSTGRES_DB "auth"
ENV POSTGRES_USER "admin"
ENV POSTGRES_PASSWORD "admin"
ENV PGDATA /data/postgres

EXPOSE 5432

VOLUME postgres:/data/postgres
