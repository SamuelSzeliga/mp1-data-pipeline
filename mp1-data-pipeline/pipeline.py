"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path


logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    if verbose == False:
        lvl=logging.INFO
    else:
        lvl=logging.DEBUG
    logging.basicConfig(
    level=lvl,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
    )

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze a data file"
    )
    
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the input file"
    )

    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to the output file"
    )

    parser.add_argument(
        "--format",
        required=False,
        help="Output format: csv or json; default is csv"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        required=False,
        help="Enable verbose logging"
    )

    return parser


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if Path(filepath).is_file():
        logger.info(f"Input file validated: {filepath}")
    else:
        logger.error(f"Input file not found: {filepath}")
        sys.exit(1)


def main():
    """Main pipeline function."""

    args = parse_arguments().parse_args()

    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    logger.debug(f"Arguments parsed: input={args.input}, \noutput={args.output}, format={args.format}")

    validate_input(args.input)

if __name__ == "__main__":
    main()