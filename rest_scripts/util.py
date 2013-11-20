import argparse

def getUrlFromArgs(args, default = "http://localhost:8000/api/crises/1"):
    url = default
    if args.url != None:
        url = args.url
    return url

def getFileFromArgs(args, default = None):
    f = default
    if args.file != None:
        f = args.file

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="A full url to use. This overrides all other args")
    parser.add_argument("--file", help="A file to use for post/put data")
    return parser.parse_args()
