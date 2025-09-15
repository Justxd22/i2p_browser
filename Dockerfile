FROM alpine:3.14 AS membarrier
WORKDIR /tmp
COPY membarrier_check.c .
RUN apk --no-cache add build-base linux-headers
RUN gcc -static -o membarrier_check membarrier_check.c
RUN strip membarrier_check

# Pull base image.
FROM jlesage/baseimage-gui:alpine-3.22-v4.9.0

ARG FIREFOX_VERSION=142.0-r0
WORKDIR /tmp

# Install Firefox.
RUN \
     add-pkg \
     firefox=${FIREFOX_VERSION} \
     i2pd \
     curl \
        python3 \
        python3-tkinter \
        py3-requests \
        mesa-dri-gallium \
        # Audio support.
        libpulse \
        # Icons used by folder/file selection window (when saving as).
        adwaita-icon-theme \
        # A font is needed.
        font-dejavu \
        # The following package is used to send key presses to the X process.
        xdotool \
        && \
    # Remove unneeded icons.
    find /usr/share/icons/Adwaita -type d -mindepth 1 -maxdepth 1 -not -name 16x16 -not -name scalable -exec rm -rf {} ';' && \
    true

# Add files.
COPY rootfs/ /
COPY --from=membarrier /tmp/membarrier_check /usr/bin/
COPY loading_screen.py /usr/bin/loading_screen.py
COPY i2pd.conf /defaults/i2pd.conf
RUN chmod +x /usr/bin/loading_screen.py
ENV WEB_AUDIO=1

# Set Tab details
RUN \
    install_app_icon.sh "https://github.com/jlesage/docker-templates/raw/master/jlesage/images/firefox-icon.png" && \
    set-cont-env APP_NAME "Firefox" && \
    set-cont-env APP_VERSION "$FIREFOX_VERSION" && \
    set-cont-env DOCKER_IMAGE_VERSION "$DOCKER_IMAGE_VERSION" && \
    true
