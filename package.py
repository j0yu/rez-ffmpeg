# -*- coding: utf-8 -*-
name = "ffmpeg"

# Vendor packages: <vendor_version>+local.<our_version>
__version__ = "4.2.2"
version = __version__ + "+local.1.0.0"

description = (
    "A complete, cross-platform solution to record, convert and stream audio and video."
)

authors = ["John Van Sickle", "Joseph Yu"]

variants = [
    ["platform-linux", "arch-x86_64"],
    # # Added just to showcase other variants, i.e. ARM chips for raspberry pi,
    # # Didn't test actually running them myself.
    # # Names pulled from altarch in https://wiki.centos.org/Download
    # ["platform-linux", "arch-aarch64"],
    # ["platform-linux", "arch-armhfp"],
]

tools = ["ffmpeg"]
# @late()
# def tools():
#     import os
#     bin_path = os.path.join(str(this.root), 'bin')
#     executables = []
#     for item in os.listdir(bin_path):
#         path = os.path.join(bin_path, item)
#         if os.access(path, os.X_OK) and not os.path.isdir(path):
#             executables.append(item)
#     return executables


build_command = r"""
set -euf -o pipefail

# Setup variables to be used
case "$REZ_ARCH_VERSION" in
    x86_64) INSTALLER_ARCH="amd64";;
    aarch64) INSTALLER_ARCH="arm64";;
    armhfp) INSTALLER_ARCH="armhf";;
    *)
        printf '\nERROR: Unsupported CPU architecture "%s"\n' \
            "$REZ_ARCH_VERSION"
        exit 1
        ;;
esac
TAR_URL="https://johnvansickle.com/ffmpeg/releases"
TAR_URL+="/ffmpeg-{version}-"$INSTALLER_ARCH"-static.tar.xz"

if [[ "$REZ_BUILD_INSTALL" -eq 1 ]]
then
    # Setup: curl "{CURL_FLAGS}" ...
    # Show progress bar if output to terminal, else silence with error
    declare -a CURL_FLAGS
    CURL_FLAGS=("-L")
    [ -t 1 ] && CURL_FLAGS+=("-#") || CURL_FLAGS+=("-sS")

    printf '\nDownloading "%s"\nand extracting into "%s"\n' \
        "$TAR_URL" "$REZ_BUILD_INSTALL_PATH"

    time curl {CURL_FLAGS} "$TAR_URL" \
    | tar -xJ --strip-components=1 -C "$REZ_BUILD_INSTALL_PATH"
fi
""".format(
    version=__version__, CURL_FLAGS="${{CURL_FLAGS[@]}}",
)


def commands():
    """Commands to set up environment for ``rez env ffmpeg``."""
    import os

    env.PATH.append("{root}")
    env.MANPATH.append(os.path.join(":{root}", "manpages"))  # See: man manpath
