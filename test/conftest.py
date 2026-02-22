allowed_markers = ("webtest",)


def pytest_collection_modifyitems(items, config):
    # add `always_run` marker to all unmarked items
    for item in items:
        if not any(x.name in allowed_markers for x in item.iter_markers()):
            item.add_marker("always_run")

    # run "always_run" if no marker spec'd
    if not config.getoption("markexpr", "False"):
        config.option.markexpr = "always_run"
