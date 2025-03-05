#!/bin/bash
set -e

create_env_file() {
    if [ ! -f .env ]; then
        echo "Creating .env file from environment variables..."
        : ${SERVICE:=""}
        : ${USERNAME:=""}
        : ${PASSWORD:=""}
        : ${CHECK_INTERVAL:=300}
        : ${TARIFF_ID:=""}

        echo "SERVICE=\"$SERVICE\"" > .env
        echo "USERNAME=\"$USERNAME\"" >> .env
        echo "PASSWORD=\"$PASSWORD\"" >> .env
        echo "CHECK_INTERVAL=$CHECK_INTERVAL" >> .env
        echo "TARIFF_ID=\"$TARIFF_ID\"" >> .env
    fi
}

create_env_file

exec "$@"