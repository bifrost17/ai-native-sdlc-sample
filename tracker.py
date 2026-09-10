"""Dataset v1 baseline contract: list, show, and complete local JSON requests."""

import argparse
import json
from pathlib import Path
import sys


def display(request):
    return "\t".join((request["id"], request["status"], request["owner"] or "-", request["title"]))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Local team request tracker")
    parser.add_argument("--data", default="requests.json")
    commands = parser.add_subparsers(dest="command", required=True)
    list_command = commands.add_parser("list")
    list_command.add_argument("--owner")
    summary_command = commands.add_parser("summary")
    summary_command.add_argument("--owner")
    summary_command.add_argument("--output")
    for name in ("show", "complete"):
        command = commands.add_parser(name)
        command.add_argument("id")
    args = parser.parse_args(argv)
    path = Path(args.data)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        requests = data["requests"]
        if args.command == "list":
            if args.owner is not None:
                requests = [request for request in requests if request["owner"] == args.owner]
            for request in requests:
                print(display(request))
            return 0
        if args.command == "summary":
            if args.owner is not None:
                requests = [request for request in requests if request["owner"] == args.owner]
            open_count = sum(1 for request in requests if request["status"] == "open")
            done_count = sum(1 for request in requests if request["status"] == "done")
            text = "open\t" + str(open_count) + "\ndone\t" + str(done_count) + "\n"
            if args.output is not None:
                output_path = Path(args.output)
                try:
                    with output_path.open("x", encoding="utf-8") as output_file:
                        output_file.write(text)
                except FileExistsError:
                    print("Output file already exists: " + args.output, file=sys.stderr)
                    return 2
                except OSError as error:
                    print("Cannot write summary output: " + str(error), file=sys.stderr)
                    return 2
                return 0
            print(text, end="")
            return 0
        request = next((row for row in requests if row["id"] == args.id), None)
        if request is None:
            print("Request not found: " + args.id, file=sys.stderr)
            return 1
        if args.command == "complete" and request["status"] != "done":
            request["status"] = "done"
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(display(request))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Cannot read or update requests: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
