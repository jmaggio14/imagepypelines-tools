from .util import make_ping_pipeline
import time

def ping(parser, args):
    """spins up a test pipeline to communicate to the given dashboard"""
    parser.add_argument("host",
                        help="IP address of the dashboard server to ping",
                        type=str)
    parser.add_argument("port",
                        help="port number of the dashboard",
                        type=int)
    parser.add_argument("-i", "--interval",
                        help="interval in milliseconds to ping the dashboard",
                        default=1000,
                        type=int)
    parser.add_argument("--no-repeat",
                        help="flag whether or not to repeat this ping",
                        action="store_true")
    args = parser.parse_args()


    # import imagepypelines in a try-catch for verbose error handling
    try:
        try:
            import imagepypelines as ip
            ip.set_log_level(100)
        except ImportError:
            print("unable to import ImagePypelines - it must be installed separately. Try \"pip install imagepypelines\"")
            raise

        # build the pipeline
        pipeline = make_ping_pipeline()

        # build internal helper function to connect to the dash and run the pipeline
        def connect_and_run():
            if ip.n_dashboards() == 0:
                ip.connect_to_dash('test_dash', args.host, args.port)
                # print message if we connect or fail to connect
                if ip.n_dashboards() == 0:
                    if args.no_repeat:
                        msg = f"unable to connect."
                    else:
                        msg = f"unable to connect... retrying in {args.interval}ms"
                    print(msg)
                else:
                    print("connection success!")

            if ip.n_dashboards():
                print("pinging...")
                pipeline.process(list(range(10)), list(range(10)) )

            time.sleep(args.interval / 1000)

        # connect
        if args.no_repeat:
            connect_and_run()
        else:
            while True:
                connect_and_run()

    except KeyboardInterrupt:
        exit(0)
