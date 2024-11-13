import csv
from collections import defaultdict

def load_lookup_table(lookup_file):
    """
    Load the lookup table from a CSV file.
    Returns a dictionary with keys as (dstport, protocol) and values as a list of tags.
    """
    lookup_dict = defaultdict(list)
    with open(lookup_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Ensure case insensitivity for protocol
            dstport = row['dstport']
            protocol = row['protocol'].lower()
            tag = row['tag']
            lookup_dict[(dstport, protocol)].append(tag)
    return lookup_dict

def process_flow_logs(flow_log_file, lookup_dict):
    """
    Process the flow logs and apply tags based on the lookup table.
    Returns two dictionaries:
    - tag_count: Count of each tag including 'Untagged'.
    - port_protocol_count: Count of each (dstport, protocol) combination.
    """
    tag_count = defaultdict(int)
    port_protocol_count = defaultdict(int)

    with open(flow_log_file, mode='r') as file:
        for line in file:
            fields = line.strip().split()
            if len(fields) < 14:
                continue  # Skip invalid lines

            # Extract relevant fields
            dstport = fields[5]
            protocol_num = fields[7]

            # Map protocol number to its name (case insensitive)
            protocol = {
                '6': 'tcp',
                '17': 'udp',
                '1': 'icmp'
            }.get(protocol_num, 'unknown').lower()

            # If protocol is unknown, mark as 'Untagged'
            if protocol == 'unknown':
                tag = 'Untagged'
            else:
                # Lookup tag (case insensitive)
                tags = lookup_dict.get((dstport, protocol), ['Untagged'])
                for tag in tags:
                    tag_count[tag] += 1

            # Update counters
            tag_count['Untagged'] += tags.count('Untagged')
            port_protocol_count[(dstport, protocol)] += 1

    return tag_count, port_protocol_count

def write_output(tag_count, port_protocol_count, output_file):
    """
    Write formatted output results to the file based on the required format.
    """
    try:
        with open(output_file, "w") as f:
            # Write Tag Counts
            f.write("Tag Counts:\n\n")
            f.write("Tag,Count\n")
            for tag, count in sorted(tag_count.items(), key=lambda x: -x[1]):
                f.write(f"{tag},{count}\n")

            # Write Port/Protocol Combination Counts, sorted by port number
            f.write("\nPort/Protocol Combination Counts:\n\n")
            f.write("Port,Protocol,Count\n")
            # 使用 int(x[0][0]) 获取元组中的第一个元素（端口号）并转换为整数
            for (port, protocol), count in sorted(port_protocol_count.items(), key=lambda x: int(x[0][0])):
                f.write(f"{port},{protocol},{count}\n")

        print("Done, the results are written into 'output.txt' file.")
    except Exception as e:
        print(f"Error writing output file: {e}")

def main():
    lookup_file = "lookup_table.csv"
    flow_log_file = "flow_logs.txt"
    output_file = "output.txt"

    # Load lookup table
    lookup_dict = load_lookup_table(lookup_file)

    # Process flow logs
    tag_count, port_protocol_count = process_flow_logs(flow_log_file, lookup_dict)

    # Write results to output file
    write_output(tag_count, port_protocol_count, output_file)

if __name__ == "__main__":
    main()





