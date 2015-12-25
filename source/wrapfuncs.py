"""Functions for inserting into the wrapper"""

#Global

#Local
import source.vexcept as vexcept
import source.vmeta as vmeta

def WRAPPER_get_coverage(rawline, meta, arglist):
    """Returns the coverage depth for this line
    arglist[0] is the name of the sample"""
    rawdict = meta.split_line(rawline)
    return int(rawdict[arglist[0]]['DP'])

def WRAPPER_get_pass_alt_freq(rawline, meta, arglist):
    """Returns the alt allele frequency for this line if filter quality
    arglist[0] is the name of the sample
    arglist[1] is the filter quality value"""
    rawdict = meta.split_line(rawline)
    if rawdict['FILTER'] == arglist[1]:
        return float(rawdict[arglist[0]]['FA'])
    else:
        raise vexcept.NoValueError
