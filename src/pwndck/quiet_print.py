class Q:
    quiet: bool = False

    @classmethod
    def set_quiet(cls, quiet: bool = True) -> None:
        Q.quiet = quiet

    @classmethod
    def print(cls, *args, **kwargs) -> None:
        if not Q.quiet:
            print(*args, **kwargs)
