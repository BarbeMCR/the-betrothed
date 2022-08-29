"""This files defines the translations of version codes."""

versions = {
    8290: "0.15",
    8231: "0.15-build823(1)",
    8230: "0.15-build823",
    8190: "0.15-build819",
    8130: "0.15-build813",
    8110: "0.15-build811",
    8081: "0.14b",
    8080: "0.14a",
    8070: "0.14",
    8061: "0.14-build806(1)",
    8060: "0.14-build806",
    8050: "0.13",
    8030: "0.13-build803",
    8011: "0.13-build801(1)",
    8010: "0.13-build801",
    7310: "0.13-build731",
    7220: "0.13-build722",
    7210: "0.13-build721",
    7130: "0.12"
}

def get_version(version):
    """Get a version translation.

    Arguments:
    version -- the version to check against
    """
    return versions.get(version, "DEV")
