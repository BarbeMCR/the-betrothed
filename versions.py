"""This files defines the translations of version codes."""

versions = {
    7122: "0.12-build712(2)",
    7130: "0.12",
    7210: "0.13-build721",
    7220: "0.13-build722",
    7310: "0.13-build731",
    8010: "0.13-build801",
    8011: "0.13-build801(1)",
    8030: "0.13-build803",
    8050: "0.13",
    8060: "0.14-build806",
    8061: "0.14-build806(1)",
    8070: "0.14",
    8080: "0.14a"
}

def get_version(version):
    """Get a version translation.

    Arguments:
    version -- the version to check against
    """
    return versions.get(version, "DEV")
