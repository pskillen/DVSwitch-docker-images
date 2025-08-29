SHELL := /usr/bin/bash

.PHONY: build up down test

build:
	docker buildx build --load -f docker/mmdvm_bridge/Dockerfile -t dvswitch/mmdvm_bridge:local .
	docker buildx build --load -f docker/analog_bridge/Dockerfile -t dvswitch/analog_bridge:local .
	docker buildx build --load -f docker/analog_reflector/Dockerfile -t dvswitch/analog_reflector:local .

up:
	docker compose -f compose/docker-compose.local.yml up -d --build

down:
	docker compose -f compose/docker-compose.local.yml down -v --remove-orphans

test:
	set -euxo pipefail; \
	end=$$((SECONDS+300)); \
	while [ $$SECONDS -lt $$end ]; do \
	  unhealthy=$$(docker ps --format '{{.Names}} {{.Status}}' | grep -E '(unhealthy|Restarting)' || true); \
	  if [ -z "$$unhealthy" ]; then \
	    states=$$(docker ps --format '{{.Names}} {{.Status}}'); echo "$$states"; \
	    ready=$$(echo "$$states" | grep -c '(healthy)' || true); \
	    if [ "$$ready" -ge 3 ]; then exit 0; fi; \
	  fi; \
	  sleep 5; \
	done; \
	echo "Services did not become healthy in time" >&2; \
	docker compose -f compose/docker-compose.local.yml logs --no-color || true; \
	exit 1

