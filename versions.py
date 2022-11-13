"""This files defines the translations of version codes."""

versions = {
    11130: "0.17",
    11060: "0.16",
    8290: "0.15",
    8081: "0.14b",
    8080: "0.14a",
    8070: "0.14",
    8050: "0.13",
    7130: "0.12"
}

def get_version(version):
    """Get a version translation.

    Arguments:
    version -- the version to check against
    """
    return versions.get(version, "DEV")
