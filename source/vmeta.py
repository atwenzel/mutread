"""Defines a class for representing header data from a vcf file. Also methods for extracting data from a string
given current metadata definitions"""

#Global

#Local
import source.vexcept as vexcept

class VData:
    """This class creates and serves a dictionary representing the header data for a vcf file"""
    def __init__(self, vcfpath):
        self.headers = {}
        self.offset = self.gen_offset(vcfpath)
        vcffile = open(vcfpath)
        rawline = vcffile.readline()
        #init dict
        self.headers['version'] = 'N/A'
        self.headers['INFO'] = []
        self.headers['FILTER'] = []
        self.headers['FORMAT'] = []
        self.headers['ALT'] = []
        self.headers['assembly'] = 'N/A'
        self.headers['contig'] = []
        self.headers['SAMPLE'] = []
        self.headers['PEDIGREE'] = []
        self.headers['pedigreeDB'] = 'N/A'
        self.headers['GATKCommandLine'] = 'N/A'
        self.headers['reference'] = 'N/A'
        self.headers['samples'] = []
        #while rawline[0:2] == "##":
        while rawline[0] == '#':
            if "##fileformat" in rawline:
                rawline = rawline.strip('\n').split('=')
                self.headers['version'] = rawline[1]
            elif "##INFO" in rawline:
                rawlist = self.comma_split(self.raw_strip(rawline, "##INFO=<"))
                self.headers['INFO'].append(self.csplit2vals(rawlist))
            elif "##FILTER" in rawline:
                rawlist = self.comma_split(self.raw_strip(rawline, "##FILTER=<"))
                self.headers['FILTER'].append(self.csplit2vals(rawlist))
            elif "##FORMAT" in rawline:
                rawlist = self.comma_split(self.raw_strip(rawline, "##FORMAT=<"))
                self.headers['FORMAT'].append(self.csplit2vals(rawlist))
            elif "##ALT" in rawline:
                rawlist = self.comma_split(self.raw_strip(rawline, "##ALT=<"))
                self.headers['ALT'].append(self.csplit2vals(rawlist))
            elif "##assembly" in rawline:
                rawline = rawline.strip('\n').split('=')
                self.headers['assembly'] = rawline[1]
            elif "##contig" in rawline:
                rawlist = self.comma_split(self.raw_strip(rawline, "##contig=<"))
                self.headers['contig'].append(self.csplit2vals(rawlist))
            elif "##PEDIGREE" in rawline:
                rawlist = self.comma_split(self.raw_strip(rawline, "##PEDIGREE=<"))
                self.headers['PEDIGREE'].append(self.csplit2vals(rawlist))
            elif "##pedigreeDB" in rawline:
                rawline = rawline.strip('\n').split('=')
                self.headers['pedigreeDB'] = rawline[1]
            elif "##GATKCommandLine" in rawline:
                #TODO: parse entire commandline, especially tumor_sample_name and normal_sample_name fields
                rawlist = self.comma_split(self.raw_strip(rawline, "##GATKCommandLine=<"))
                self.headers['GATKCommandLine'] = self.csplit2vals(rawlist)
            elif "##reference" in rawline:
                rawline = rawline.strip('\n').split('=')
                self.headers['reference'] = rawline[1]
            elif "#CHROM" in rawline:
                #Extact the sample names from the first 
                rawlist = rawline.strip('\n').split('\t')
                samp_ind = 9
                while samp_ind < len(rawlist):
                    self.headers['samples'].append(rawlist[samp_ind])
                    samp_ind += 1
            else:
                raise vexcept.HeaderParseError(rawline)

            rawline = vcffile.readline()

    def gen_offset(self, vcfpath):
        """Returns a dict of column number keyed by name"""
        vcffile = open(vcfpath, 'r')
        hline = vcffile.readline()
        while "#CHROM" not in hline:
            hline = vcffile.readline().strip('\n')
        hlist = hline.split('\t')
        retdict = {}
        for i in range(0, len(hlist)):
            retdict[i] = hlist[i].strip('#')
        vcffile.close()
        return retdict

    def split_format(self, formstr, formvals):
        """Returns a dict of the format values"""
        strlist = formstr.split(':')
        vallist = formvals.split(':')
        retdict = {}
        for i in range(0, len(strlist) -1):
            retdict[strlist[i]] = vallist[i]
        return retdict

    def split_line(self, rawline):
        """Uses the offset to turn a data line into a dictionary keyed by header"""
        retdict = {}
        rawlist = rawline.strip('\n').split('\t')
        for i in range(0, len(rawlist)):
            retdict[self.offset[i]] = rawlist[i]
        formstr = retdict['FORMAT']
        for sname in self.headers['samples']:
            retdict[sname] = self.split_format(formstr, retdict[sname])
        return retdict

    #helper functions for init method
    def raw_strip(self, rawline, intro):
        """Strips out unnecessary text from vcf INFO entries"""
        rawline = rawline.strip(intro)
        nrl = ''
        for char in rawline:
            if char == '>' or char == '\n' or char == '<':
                nrl += ''
            else:
                nrl += char
        return nrl
    
    def comma_split(self, rawline):
        """Smarter than split, ignores commas within quotes, <- like these"""
        splitvals = []
        currval = ''
        flag = False
        for i in range(0, len(rawline)-1):
            if rawline[i] == '"':
                flag = not flag
            elif rawline[i] == ',' and flag:
                currval += rawline[i]
            elif rawline[i] == ',' and not flag:
                splitvals.append(currval)
                currval = ''
            else:
                currval += rawline[i]
        if currval != '':
            splitvals.append(currval)
        return splitvals

    def csplit2vals(self, rawlist):
        """Takes an already split list and makes a dict out of it"""
        retdict = {}
        for item in rawlist:
            pair = item.split('=')
            retdict[pair[0]] = pair[1]
        return retdict

    #functions for useful VData access
    def getformat(self, rawform, rawstr):
        """Takes both the raw format line and raw data line from a vcf entry and returns a dict keyed by format ID"""
        formlist = rawform.strip('\n').split(':')
        formstr = rawstr.strip('\n').split(':')
        if len(formlist) != len(formstr):
            raise vexcept.FormatParseError(rawform, rawstr)
        retdict = {}
        for pair in zip(formlist, formstr):
            retdict[pair[0]] = pair[1]
        return retdict
    
    #definitions to allow VData to be accessed like a dict (read-only)
    def __getitem__(self, val):
        return self.headers[val]
    def __setitem__(self, key, val):
        raise vexcept.BadHeaderAccess()
    def __delitem__(self, key, val):
        raise vexcept.BadHeaderAccess()

if __name__ == "__main__":
    print("Defines a class to represent vcf headers")
