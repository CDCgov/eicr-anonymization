"""Main entry point for the EICR anonymization tool."""

from argparse import ArgumentParser, Namespace

from eicr_anonymization.anonymize_eicr import anonymize


def _parse_arguments() -> Namespace:
    """Parse command-line arguments for the EICR anonymization tool.

    Returns:
        Parsed command-line arguments

    """
    parser = ArgumentParser(description="Anonymize eICR XML files.")
    parser.add_argument(
        "input_location",
        help="This can be either a directory or an xml file. If it is a directory the Anonymization tool will attempt to anonymize all XML files in the directory.",  # noqa: E501
    )
    parser.add_argument(
        "-l",
        "--light",
        action="store_true",
        help="Use a lighter version of anonymization. Only the following patient fields with be anonymized: name, dates, race, ethnicity, emergency contacts, and clinical notes.",  # noqa: E501
    )

    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.3.0")

    debug_group = parser.add_argument_group("Debugging and Testing Options")
    debug_group.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Print table showing original and replacement tags. Will show sensitive information.",
    )
    debug_group.add_argument(
        "-s", "--seed", type=int, default=None, help="Set the random seed. For Debugging."
    )
    debug_group.add_argument(
        "--siso",
        "--same_in_same_out",
        action="store_true",
        dest="deterministic_functions",
        default=False,
        help="For the same value will always replace with the same new value regardless of run or seed.",
    )

    return parser.parse_args()


def main() -> None:
    """Run the EICR anonymization tool."""
    args = _parse_arguments()
    print("Starting EICR anonymization...")
    anonymize(args)


if __name__ == "__main__":
    main()
