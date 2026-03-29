from shopify_backend.bootstrap.console import CliCommand
import fire


class Command:
    def __init__(self):
        self.shopifyapi = CliCommand()


def main():
    """Trigger function for fire command line interface"""
    fire.Fire(Command)


if __name__ == "__main__":
    main()