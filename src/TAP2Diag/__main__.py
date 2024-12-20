#!/usr/bin/env python
from TAP2Diag import TAP2DiagConverter, parse_arguments

def main():
    args = parse_arguments()
    tap = args.tapFileName
    config = args.configFileName
    namespaces = args.namespaceFileName
    about = args.aboutFileName
    shapes = args.shapesFileName
    outputFileName = args.outputFileName

    c = TAP2DiagConverter(tap, config, namespaces, shapes, about)
    c.convertAP2mermaid()
    c.dump_mermaid(outputFileName)

if __name__ == "__main__":
    main()
