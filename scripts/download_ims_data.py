#!/usr/bin/env python3
"""IMS IRIS/FDSN data downloader"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="Download IMS infrasound data")
    parser.add_argument("--stations", nargs="+", help="Station IDs")
    parser.add_argument("--start", required=True, help="Start time")
    parser.add_argument("--end", required=True, help="End time")
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()
    
    # TODO: Implement data download
    print(f"Downloading data for stations: {args.stations}")
    print(f"Time range: {args.start} to {args.end}")


if __name__ == "__main__":
    main()
