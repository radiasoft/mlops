#!/bin/bash

build_image_base=radiasoft/python3
build_is_public=1

build_as_run_user() {
    install_pip_install mlflow
}
