"""Welcome to MutRead.  The goal for all this software is for you to be able to put a vcf files in the 'data' folder
and do anything you can imagine with them.

Questions/concerns: Alex Wenzel (alexanderwenzel2017@u.northwestern.edu)"""

#Global

#Local
import source.plotting as plot
import source.vcfwrapper as wrap
import source.vmeta as vmeta
import source.vstats as vstats
import source.wrapfuncs as wrapfuncs

if __name__ == "__main__":
    #print(wrap.vcfwrapper('data/ssas2t.vcf', vstats.WRAPPER_coverage_hist, 'more', 'garbage'))
    #print(vmeta.VData('data/ssas2t.vcf').headers)
    #print(vmeta.VData('data/ssas2t.vcf')['FORMAT'])
    #print(vmeta.VData('data/ssas2t.vcf')['FORMAT'][0])
    #vmeta.VData('data/ssas2t.vcf')['notaheader'] = 0
    #print(vmeta.VData('data/ssas2t.vcf').headers)

    meta = vmeta.VData('data/ssgh1.vcf')
    #print(meta.headers)
    #print(meta.split_line("chrM\t73\t.\tG\tA\t.\tREJECT\t.\tGT:AD:BQ:DP:FA\t0:5,981:.:985:0.995\t0/1:1,816:27:826:0.999"))
    #print(meta.getformat('GT:AD:BQ:DP:FA', '0:5,981:.:985:0.995'))

    ###HISTOGRAM OF COVERAGE:
    covs = wrap.vcfwrapper('data/ssgh1.vcf', wrapfuncs.WRAPPER_get_coverage, meta, ['H7JMTCCXX_4_150828_FR07935720'])
    plot.plot_hist([covs], ["Coverage Depth"])

    ###HISTOGRAM OF FA:
    fas_tumor = wrap.vcfwrapper('data/ssgh1.vcf', wrapfuncs.WRAPPER_get_pass_alt_freq, meta, ['H7JMTCCXX_4_150828_FR07935719', 'PASS'])
    plot.plot_hist([fas_tumor], ['alt_allele_freq_tumor'])
    fas_normal = wrap.vcfwrapper('data/ssgh1.vcf', wrapfuncs.WRAPPER_get_pass_alt_freq, meta, ['H7JMTCCXX_4_150828_FR07935720', 'PASS'])
    plot.plot_hist([fas_normal], ['alt_allele_freq_normal'])
