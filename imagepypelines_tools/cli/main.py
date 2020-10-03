import argparse

from .build import build
from .pull import pull
from .push import push
from .dashboard import dashboard
from .ping import ping

def main():
    # parsing command line arguments
    parser = argparse.ArgumentParser(prog='imagepypelines',
                                        usage=__doc__)

    # primary argument
    parser.add_argument('action',
                        help="the primary action to perform",
                        # define acceptable commands
                        choices=["shell",
                                    "push",
                                    "pull",
                                    "build",
                                    "dashboard",
                                    'ping',
                                    ]
                        )

    args = parser.parse_known_args()[0]

    ############################################################################
    if args.action == "build":
        build(parser, args)

    ############################################################################
    elif args.action == "pull":
        pull(parser, args)

    ############################################################################
    elif args.action == "push":
        push(parser, args)

    ############################################################################
    elif args.action == "dashboard":
        dashboard(parser, args)

    ############################################################################
    elif args.action == "ping":
        ping(parser, args)


if __name__ == "__main__":
    main()
