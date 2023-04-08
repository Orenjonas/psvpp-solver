def map_num_to_bit():
    pass


def get_power_set(str: origin_set):
    """
    Implementation of the following algorithm by Rune at stackoverflow:
        https://stackoverflow.com/a/7371357
    Return: list - Power set of the original set
    """

    powerset = []

    for i in range(2**len(origin_set)):
        subset = []

        # For each enabled bit in i add the corresponding letter to subset

        # add subset to powerset


# Set powerset = new Set();
# for(int i between 0 and 2^9)
# {
#   Set subset = new Set();
#   for each enabled bit in i add the corresponding letter to subset
#   add subset to powerset
# }
