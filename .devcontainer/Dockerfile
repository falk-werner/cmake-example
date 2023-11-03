FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y --no-install-recommends \
    build-essential \
    cmake \
    libgtest-dev \
    libgmock-dev \
    clang-tidy \
    valgrind \
    lcov \
    qemu-user \
    qemu-user-static \
    crossbuild-essential-armhf \
    ca-certificates \
    curl \
    git \
    openssh-client

ARG GTEST_VERSION=1.11.0
RUN mkdir -p /opt/gtest
WORKDIR /opt/gtest
RUN curl -sL https://github.com/google/googletest/archive/refs/tags/release-${GTEST_VERSION}.tar.gz -o gtest.tar.gz
RUN tar -xf gtest.tar.gz
ADD cmake/toolchain/arm.cmake /opt/gtest/arm-toolchain.cmake
RUN cmake --toolchain=/opt/gtest/arm-toolchain.cmake -S googletest-release-${GTEST_VERSION} -B arm
RUN cmake --build arm
RUN rm -rf gtest.tar.gz googletest-release-${GTEST_VERSION} arm-toolchain.cmake

ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME
RUN useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

USER $USERNAME

ADD --chown=root:root --chmod=755 .devcontainer/qemu-arm.sh /usr/bin/qemu-arm.sh

