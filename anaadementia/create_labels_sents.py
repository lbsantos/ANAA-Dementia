import argparse
import json
import re
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('narratives_file', help='JSON file with training corpus')
    parser.add_argument('json_out', help='JSON file with training corpus')

    args = parser.parse_args()

    labels_sents = {}
    with open(args.narratives_file) as f:
        for line in f:
            line = line.split('\t')
            print(line)
            sent = line[0].rstrip()
            labels = line[1].rstrip().split()
            for label in labels:
                labels_sents[label] = sent
    json.dump(labels_sents, open(args.json_out, 'w'))
