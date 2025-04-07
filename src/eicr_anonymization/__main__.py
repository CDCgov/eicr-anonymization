"""Main entry point for the EICR anonymization tool."""

from argparse import ArgumentParser, Namespace

from eicr_anonymization.anonymize_eicr import anonymize


def _parse_arguments() -> Namespace:
    """Parse command-line arguments for the EICR anonymization tool.

    Returns:
        Parsed command-line arguments

    """
    parser = ArgumentParser(description="Anonymize eICR XML files.")
    parser.add_argument("input_location", help="Directory containing eICR XML files.")
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Print table showing original and replacement tags. Will show sensitive information.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the EICR anonymization tool."""
    args = _parse_arguments()
    anonymize(args)


if __name__ == "__main__":
    main()
