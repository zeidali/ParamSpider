#!/usr/bin/env python3
from core import requester
from core import extractor
from core import save_it
from urllib.parse import unquote
import requests
import re
import argparse
import os
import sys
import time

start_time = time.time()


def main():
    time.sleep(2)  # Ensure banner from other tool doesn't overlap

    banner = r"""\u001b[36m
            ___                               _    __        
           / _ \___ ________ ___ _  ___ ___  (_)__/ /__ ____
          / ___/ _ `/ __/ _ `/  ' \(_-</ _ \/ / _  / -_) __/
         /_/   \_,_/_/  \_,_/_/_/_/___/ .__/_/\_,_/\__/_/    
                                     /_/                    
                             
                            - coded with <3 by Devansh Batham  
        \u001b[0m
    """
    print(banner)

    parser = argparse.ArgumentParser(description='ParamSpider - a parameter discovery suite')
    parser.add_argument('-d','--domain' , help='Target domain [ex: hackerone.com]', required=True)
    parser.add_argument('-s','--subs' , help='Set False for no subdomains [ex: --subs False]', default="True")
    parser.add_argument('-l','--level' , help='For nested parameters [ex: --level high]')
    parser.add_argument('-e','--exclude', help='Extensions to exclude [ex: --exclude php,aspx]')
    parser.add_argument('-o','--output' , help='Output file name [default: domain.txt]')
    parser.add_argument('-p','--placeholder' , help='Placeholder string after parameter name.', default="FUZZ")
    parser.add_argument('-q', '--quiet', help='Do not print results on screen', action='store_true')
    parser.add_argument('-r', '--retries', help='Number of retries for 4xx/5xx errors', default=3)
    args = parser.parse_args()

    use_subs = args.subs.lower() == "true"
    if use_subs:
        url = f"https://web.archive.org/cdx/search/cdx?url=*.{args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
    else:
        url = f"https://web.archive.org/cdx/search/cdx?url={args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"

    retry = True
    retries = 0
    while retry and retries <= int(args.retries):
        response, retry = requester.connector(url)
        retries += 1

    if response is False:
        return

    response = unquote(response)

    # Extensions to exclude
    black_list = []
    if args.exclude:
        black_list = [f".{ext.strip()}" for ext in args.exclude.split(",")]

        print(f"\u001b[31m[!] URLs containing these extensions will be excluded: {black_list}\u001b[0m\n")

    final_uris = extractor.param_extract(response, args.level, black_list, args.placeholder)
    save_it.save_func(final_uris, args.output, args.domain)

    if not args.quiet:
        print("\u001b[32;1m")
        print('\n'.join(final_uris))
        print("\u001b[0m")

    print(f"\n\u001b[32m[+] Total retries: {retries - 1}\u001b[31m")
    print(f"\u001b[32m[+] Unique URLs found: {len(final_uris)}\u001b[31m")
    output_path = args.output if args.output else f"output/{args.domain}.txt"

    print(f"\u001b[32m[+] Output saved to: \u001b[36m{output_path}\u001b[0m")
    print(f"\u001b[31m[!] Execution time: {str(round(time.time() - start_time, 2))}s\u001b[0m")


if __name__ == "__main__":
    main()
