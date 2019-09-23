#!/usr/bin/env bash

env=$(tail -c +16 secrets.yaml)
env=${env//\"}
export ${env//: /=}
