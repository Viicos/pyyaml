"""Check that the installed wheel is `pyyaml-cp315`, built with the libyaml extension."""

import sys
import sysconfig
from importlib.metadata import PackageNotFoundError, version

import yaml


def main() -> None:
    if (installed := version("pyyaml-cp315")) != yaml.__version__:
        raise SystemExit(f"pyyaml-cp315 {installed} provides yaml {yaml.__version__}")
    try:
        version("PyYAML")
    except PackageNotFoundError:
        pass
    else:
        raise SystemExit("PyYAML is installed alongside pyyaml-cp315")
    if not yaml.__with_libyaml__:
        raise SystemExit("PyYAML was built without the libyaml extension")

    document = {"list": [1, 2.5, None, "text"], "mapping": {"nested": True}}
    dumped = yaml.dump(document, Dumper=yaml.CSafeDumper)
    if yaml.load(dumped, Loader=yaml.CSafeLoader) != document:
        raise SystemExit("The libyaml loader and dumper do not round-trip")

    # Importing an extension that is not marked as free-threading compatible enables the GIL again.
    if sysconfig.get_config_var("Py_GIL_DISABLED") and sys._is_gil_enabled():
        raise SystemExit("Importing the libyaml extension enabled the GIL")


if __name__ == "__main__":
    main()
