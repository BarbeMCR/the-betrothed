"""This files defines the translations of version codes and levels."""

versions = {
    102040: "0.20",
    11270: "0.19",
    11210: "0.18a",
    11200: "0.18",
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
    return versions.get(version, "unknown")

levels = {
    (1, 0, 0): "Chapter I-A",
    (1, 0, 1): "Chapter I-B",
    (1, 0, 2): "Chapter II-A",
    (1, 0, 3): "Chapter II-B",
    (1, 0, 4): "Chapter II-C"
}

def get_level(part, subpart, level):
    """Get a level translation.

    Arguments:
    part -- the part to check against
    subpart -- the subpart to check against
    level -- the level to check against
    """
    return levels.get((part, subpart, level), "unknown")
