# Flow Log Parser

## Project Description

This project is a Python program designed to parse VPC flow logs and tag each log entry based on a lookup table. It supports the default log format (Version 2) and outputs tag counts and port/protocol combination counts.

## File Structure

- `flow_log_parser.py`: Main Python script for parsing flow logs.
- `lookup_table.csv`: Lookup table containing port, protocol, and tag mappings.
- `flow_logs.txt`: Input file with sample VPC flow logs.
- `output.txt`: Output file with the results.
- `README.md`: Project documentation.

## Requirements

The program uses only Python's built-in libraries:
- `csv` for reading the lookup table.
- `collections.defaultdict` for counting.

No additional third-party libraries are needed.

## Assumptions

- The input flow logs use the default format (Version 2).
- The lookup table (`lookup_table.csv`) supports case-insensitive matching for the protocol.
- The lookup table can contain up to 10,000 entries.
- The input flow log file can be up to 10 MB in size.
- The program only supports common protocols like TCP (`6`), UDP (`17`), ICMP (`1`), and IGMP (`2`).
- Unrecognized `(dstport, protocol)` pairs are labeled as `Untagged`.
