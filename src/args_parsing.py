import getopt


def parse_arguments(argv):
    usage = 'compress -f <file> [-o <output file>] haff|num|lzw|fib|gamma|delta|o,ega'
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        print("opts: ", opts)
        print("args: ", args)
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    print('Input file is: ', input_file)
    print('Output file is: ', output_file)