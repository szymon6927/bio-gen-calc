class ModuleName:
    CHI_SQUARE = "chi_square"
    CHI_SQUARE_GOODNESS = "chi_square_goodness"
    GENETIC_DISTANCE = "genetic_distance"
    HARDY_WEINBERG = "hardy_weinberg"
    PIC_DOMINANT = "pic_dominant"
    PIC_CODOMINANT = "pic_codominant"
    DOT_PLOT_RAW_SEQ = "dot_plot_raw_seq"
    DOT_PLOT_GENEBANK_IDS = "dot_plot_genebank_ids"
    CONSENSUS_SEQUENCE_RAW_SEQ = "consensus_sequence_raw_seq"
    CONSENSUS_SEQUENCE_FILE_SEQ = "consensus_sequence_file_seq"
    CONSENSUS_SEQUENCE_GENE_BANK = "consensus_sequence_gene_bank"
    SEQUENCES_TOOLS = "sequences_tools"


class NameConverter:
    KEY_TO_NAME = dict()
    KEY_TO_NAME['ho'] = "Homozygotes"
    KEY_TO_NAME['he'] = "Heterozygotes"
    KEY_TO_NAME['rho'] = "Rare homozygotes"
    KEY_TO_NAME['alfa'] = "Level of significance"
    KEY_TO_NAME['amplified_marker'] = "Number or frequency of amplified marker"
    KEY_TO_NAME['absence_marker'] = "Number or frequency of absence marker"
    KEY_TO_NAME['width'] = "Table width"
    KEY_TO_NAME['height'] = "Table heigh"
    KEY_TO_NAME['matrix'] = "Distance matrix"
    KEY_TO_NAME['dendrogram'] = "Dendogram"
    KEY_TO_NAME['dotplot_img'] = "Dot plot"
    KEY_TO_NAME['field_sum'] = "Field sum"
    KEY_TO_NAME['observed'] = "Group of Observed"
    KEY_TO_NAME['expected'] = "Group of Expected"
    KEY_TO_NAME['taxon_number'] = "Number of populations"
    KEY_TO_NAME['locus_number'] = "Number of loci"
    KEY_TO_NAME['type_of_distance'] = "Type of distance"
    KEY_TO_NAME['type_of_dendrogram'] = "Type of dendrogram"
    KEY_TO_NAME['number_of_alleles'] = "Number of alleles"

    SHORTCUT_TO_MODULE_NAME = dict()
    SHORTCUT_TO_MODULE_NAME['chi2_standard'] = "Chi square"
    SHORTCUT_TO_MODULE_NAME['chi_square'] = "Chi square"
    SHORTCUT_TO_MODULE_NAME['chi2_yats'] = "Yate`s Chi square"
    SHORTCUT_TO_MODULE_NAME['dof'] = "dof"
    SHORTCUT_TO_MODULE_NAME['p_standard'] = "Chi square p-value"
    SHORTCUT_TO_MODULE_NAME['p_yats'] = "Yate`s Chi square p-value"
    SHORTCUT_TO_MODULE_NAME['correlation_yats'] = "Yate`s chi-square correlation"
    SHORTCUT_TO_MODULE_NAME['correlation_standard'] = "Chi-square correlation"
