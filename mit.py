###############################################################################
# Python script used to read in Datex-Ohmeda Record file and parse out
# ECG12 sub-records.

###############################################################################

# region Import region
import os
import argparse  # command line parser
from struct import *
import numpy as np
import sys
import wfdb
# endregion

# region Globals region

__version__ = '1.0'  # version of script

# endregion


def humansize(nbytes):
    '''
    Append an appropriate suffix designating file size (kb, mb, etc).  Make number of bytes more human readable.

    :param nbytes: number of bytes
    :return: string with number of bytes converted to appropriate human readable size appended with unit size.
    '''
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def main(arg_list=None):
    # region Command Line
    ###############################################################################
    # Get command line arguments.
    parser = argparse.ArgumentParser(description="Process the given MIT directory")
    parser.add_argument('-d', dest='mit_directory',
                        help='name of directory to read and process', required=True)
    parser.add_argument('-o', dest='csv_output_file',
                        help='output file to write metrics to', required=True)
    parser.add_argument('-v', dest='verbose', default=False, action='store_true',
                        help='verbose output flag', required=False)
    parser.add_argument('--version', action='version', help='Print version.',
                        version='%(prog)s Version {version}'.format(version=__version__))

    # Parse the command line arguments
    args = parser.parse_args(arg_list)

    ###############################################################################
    # Test for existence of the directory.
    if os.path.isdir(args.mit_directory) is False:
        print('ERROR, ' + args.csv_input_file + ' does not exist')
        print('\n\n')
        parser.print_help()
        return -1

    # endregion

    ###############################################################################
    # Get a list of all the annotation files...
    an_files = [os.path.join(args.mit_directory, os.path.splitext(f)[0])
                for f in os.listdir(args.mit_directory) if f.endswith('.prf')]

    print('{0:d} annotation files found'.format(len(an_files)))

    ###############################################################################
    # Build a list of an objects...
    an_list = []
    for an_file in an_files:
        an_list.append(wfdb.rdann(an_file, annotator='prf'))

    ###############################################################################
    # Build some metrics strings...
    an_metrics_list = []
    for an in an_list:
        for samp in an.annsamp:
            an_metrics_list.append("{0:s},{1:d},{2:d}".format(an.recordname, len(an.annsamp), samp))

    ###############################################################################
    # and write the metrics...
    print('Write {0:d} metrics to {1:s}'.format(len(an_list),args.csv_output_file))
    with open(args.csv_output_file, 'w') as f:
        f.write('annotation,count,sample offset\n')
        for item in an_metrics_list:
            f.write(item + '\n')

    return 0


###############################################################################
if __name__ == '__main__':
    rv = main()
    exit(rv)
