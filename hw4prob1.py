#
# (c) 2023 Michael Fitzgerald (mpfitz@ucla.edu)
#
# Some code for querying Simbad for making a target list.
#


from astroquery.simbad import Simbad
from astropy import units as u
from astropy.coordinates import SkyCoord

import logging
_log = logging.getLogger('hw4prob1')



def format_target_list(target_list):
    """Query Simbad for list of identifiers; returns dictionary with RA and Dec strings"""

    # an empty dictionary to hold our output
    target_info = {}
    
    # get the Simbad query for M45 (the Pleiades)
    for target_name in target_list:
        _log.debug('querying {}'.format(target_name))
        result_table = Simbad.query_object(f"{target_name}")
        _log.info(result_table)

        # report on results
        n_result = len(result_table)
        _log.info('{}: {} objects found'.format(target_name, n_result))
        if n_result == 0:
            _log.warn('skipping....')
            continue
        if n_result > 1:
            _log.warn('using first result')

        # store RA and DEC strings as tuple for this object
        ra = result_table["RA"]
        dec = result_table["DEC"]
        
        _log.info(f"ra = {ra}")
        _log.info(f"dec = {dec}")
        
        # c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree)
        # The output gives RA and Dec in hmsdms with spaces only (no symbols) on my end
        c = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))
        _log.info(f"c = {c}")
        _log.info(f"type(c) = {type(c)}")
        
        # the result is a RA DEC (hmsdms) string in a single-element list, converted into tuple.
        target_info[target_name] = tuple( c.to_string('hmsdms')[0].split(' ') )
        
        _log.info(f"target_info[target_name] = {target_info[target_name]}")

    # sort dictionary by the "value" (ra,dec)
    target_info = dict(sorted(target_info.items(), key=lambda x:x[1]))

    return target_info


if __name__ == '__main__':

    # set up logging output
    #logging.basicConfig(level=logging.INFO,
    logging.basicConfig(level=logging.DEBUG,
                        format='%(name)-12s: %(levelname)-8s %(message)s',
                        )

    # define target list
    target_list = ['M2',
                   'M45',
                   'HD 189733',
                   '3C 273',
                   'NGC 1068',
                   'AU Mic',
                   'TRAPPIST-1'
                   ]


    target_info = format_target_list(target_list)
    print(target_info)
    print()
    print(target_info.items())  # dictionary as a nested list, with each entry being a tuple containing the name (string) and a coordinate tuple containing RA & Dec.

    # output results to nicely formatted file
    output_fn = 'target_list.txt'
    with open(output_fn, 'w') as f:
        for tn, (ra, dec) in target_info.items():  # "tn" is the target name
            # print the output to file
            #   See https://docs.python.org/3/tutorial/inputoutput.html for string
            #   formatting for the fixed-width output
            # name is left-justified & 20 chars + RA is left-jusitfied & 15 chars + DEC is left-jusitfied & 15 chars
            # use '+' to combine strings. Using the comma ',' adds a single space between the strings.
            # One way of left justifying is with "ljust":
            # print(tn.ljust(20) + ra.ljust(15) + dec.ljust(15), file=f)
            # Alternate, shorter way of left justifying with f strings:
            print(f"{tn:<20}{ra:<15}{dec:<15}", file=f)
