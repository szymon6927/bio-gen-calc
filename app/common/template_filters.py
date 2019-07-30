from ast import literal_eval


def to_dict(string):
    return literal_eval(string)


def translate_name(name):
    translator = {}

    translator['ho'] = "Homozygotes"
    translator['he'] = "Heterozygotes"
    translator['rho'] = "Rare homozygotes"
    translator['alfa'] = "Level of significance"
    translator['amplified_marker'] = "Number or frequency of amplified marker"
    translator['absecnce_marker'] = "Number or frequency of absecnce marker"
    translator['width'] = "Table height"
    translator['height'] = "Table width"
    translator['matrix'] = "Distance matrix"
    translator['dendrogram'] = "Dendogram"
    translator['dotplot_img'] = "Dot plot"
    translator['field_sum'] = "Field sum"
    translator['observed'] = "Group of Observed"
    translator['expected'] = "Group of Expected"
    translator['taxon_number'] = "Number of populations"
    translator['locus_number'] = "Number of loci"
    translator['type_of_distance'] = "Type of distance"
    translator['type_of_dendrogram'] = "Type of dendrogram"
    translator['number_of_alleles'] = "Number of alleles"

    return translator.get(name, name)


def remove_first_last_double_quotes(text):
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]

        return text
