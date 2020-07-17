# /usr/bin/bash

# $0 build|up|down [dev]

if [ $# -eq 0 ]
then
    echo "Usage: $0 build|up|down [npmbuild|web|fe|neo4j...]"
else
    if [ $1 = "build" ]; then docker-compose -f docker-compose-dev.yml build --parallel $2; exit 0; fi
    if [ $1 = "up" ]; then docker-compose -f docker-compose-dev.yml up -d; exit 0; fi
fi