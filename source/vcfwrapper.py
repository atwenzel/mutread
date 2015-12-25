"""Defines a function called vcfwrapper that takes a given function for one line of raw
vcf data and operates on it for every data line in the file and collects results as a list of results

Every vcfwrapper-compliant function should be defined to accept a rawline, a meta header object and a list of arguments. It should
return some result that can be compiled into a list.  If necessary, write a separate function to turn this list
into a more useful structure"""

#Global

#Local
import vexcept

#TODO: Implement consistent format for metadata (as a class)

def vcfwrapper(vcfpath, func, meta, arglist):
    """ vcfpath: a relative path to a vcf file
        func: a function pointer (just the name of the function in the scope in which it is defined
        meta: a dictionary of vcf header data.
        arglist: list of arguments (apart from vcfline, to be given to function """
    vcffile = open(vcfpath)
    results = []
    rawline = vcffile.readline()
    while rawline != '':
        if rawline[0] == '#':
            rawline = vcffile.readline()
            continue
        try:
            results.append(func(rawline, meta, arglist))
        except vexcept.NoValueError:
            #Some wrapper functions may not want to add a value to the cumulative list, if so they raise this exception
            pass 
        rawline = vcffile.readline()
    return results

if __name__ == "__main__":
    print("this file defines the wrapper method iterating over vcf files")
