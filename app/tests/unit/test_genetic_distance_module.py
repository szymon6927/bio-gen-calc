# {
#   "taxon_number":"6",
#   "locus_number":"1",
#   "type_of_distance":"standard",
#   "type_of_dendrogram":"upgma",
#   "number_of_alleles":[2],
#   "column_0":[0.3,0.7],
#   "column_1":[0.4,0.6],
#   "column_2":[0.5,0.5],
#   "column_3":[0.6,0.4],
#   "column_4":[0.7,0.3],
#   "column_5":[0.8,0.2]
# }

# [0.01686, 0.07421, 0.1772, 0.32277, 0.50239, 0.01961, 0.08004, 0.1772,
# 0.30119, 0.01961, 0.07421, 0.15374, 0.01686, 0.06002, 0.01284]

from ...genetic_distance.utils.StandardDistance import StandardDistance


def test_genetic_distance_basic():
    data = dict()
    data["taxon_number"] = "6"
    data["locus_number"] = "1"
    data["type_of_distance"] = "standard"
    data["type_of_dendrogram"] = "upgma"
    data["number_of_alleles"] = [2]
    data["column_0"] = [0.3, 0.7]
    data["column_1"] = [0.4, 0.6]
    data["column_2"] = [0.5, 0.5]
    data["column_3"] = [0.6, 0.4]
    data["column_4"] = [0.7, 0.3]
    data["column_5"] = [0.8, 0.2]

    gen_distance = StandardDistance(data)
    gen_distance.calcuate_distances()
    results = gen_distance.get_condensed_matrix()

    # expected condesned matrix
    expected_results = [0.01686, 0.07421, 0.1772, 0.32277, 0.50239, 0.01961, 0.08004,
                        0.1772, 0.30119, 0.01961, 0.07421, 0.15374, 0.01686, 0.06002, 0.01284]

    for i, j in zip(results, expected_results):
        assert i == j
