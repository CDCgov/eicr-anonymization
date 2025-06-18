"""Main entry point for the EICR anonymization tool."""

from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter

from eicr_anonymization.anonymize_eicr import anonymize


def _parse_arguments() -> Namespace:
    """Parse command-line arguments for the EICR anonymization tool.

    Returns:
        Parsed command-line arguments

    """
    parser = ArgumentParser(
        description="Anonymize eICR and RR XML files in a given directory. Always verify sensitive data has been properly anonymized before sharing processed files."  # noqa: E501
    )
    parser.add_argument(
        "-p",
        "--patient_only",
        action="store_true",
        dest="patient_only",
        default=False,
        help="Use a lighter version of anonymization. Only the following patient fields with be anonymized: name, dates, race, ethnicity, emergency contacts, and clinical notes.",  # noqa: E501
    )

    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.3.0")

    subparsers = parser.add_subparsers(
        description="There is currently only one subcommand.", dest="command"
    )
    debug_parser = subparsers.add_parser(
        "debug",
        help="Debugging/testing mode. WARNING: may expose sensitive data.",
        formatter_class=RawDescriptionHelpFormatter,
        description="""WARNING: Debug mode is intended for development, testing, and debugging only. These options can compromise the security of data anonymization by:

- Making replacement data predictable and repeatable
- Exposing original sensitive data in output

Only use with sample/test data, never with real sensitive data.""",  # noqa: E501
    )
    parser.add_argument(
        "input_location",
        help="This can be either a directory or an xml file. If it is a directory the Anonymization tool will attempt to anonymize all XML files in the directory.",  # noqa: E501
    )

    debug_parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Print table showing original and replacement tags. Will show sensitive information.",
    )
    debug_parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=None,
        help="Set the random seed.",
    )
    debug_parser.add_argument(
        "--siso",
        "--same_in_same_out",
        action="store_true",
        dest="deterministic_functions",
        default=False,
        help="The same value will always be replaced with the same new value regardless of run or seed." # noqa: E501
    )

    return parser.parse_args()


def main() -> None:
    """Run the EICR anonymization tool."""
    args = _parse_arguments()
    print("Starting EICR anonymization...")
    anonymize(args)


if __name__ == "__main__":
    main()
