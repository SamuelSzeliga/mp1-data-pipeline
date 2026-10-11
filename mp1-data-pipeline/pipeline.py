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
from src._init_ import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)


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
        "--config",
        required=True,
        help="Path to config file"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        required=False,
        help="Enable verbose logging"
    )

    return parser


def main():
    """Main pipeline function."""

    args = parse_arguments().parse_args()

    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    logger.debug(f"Arguments parsed: input={args.input}, output={args.output}, config={args.config}")

    validate_input(args.input)
    validate_input(args.config)

    try:
        df_before = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    try:
        required_columns = config["processing"]["validation"].get("required_columns", [])
        numeric_columns = config["processing"]["validation"].get("numeric_columns", [])
        validated_df = validate_dataframe(df_before, required_columns, numeric_columns)
        logger.info(f"Validation: {len(df_before)} rows before, {len(validated_df)} rows after")
    except ValueError:
        sys.exit(1)

    try:
        df_after = (process_data(validated_df, config))
        logger.info(f"Processing complete: {len(validated_df)} -> {len(df_after)} rows")

        save_data(df_after, args.output)
        logger.info(f"Saved cleaned data to {args.output}")
    except ValueError:
        sys.exit(1)

    print(create_cleaning_report(validated_df, df_after))
                

if __name__ == "__main__":
    main()