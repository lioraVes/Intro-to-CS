########################################################
# FILE : ex11.py
# WRITER : Liora Vesnovaty
# EXERCISE : intro2cse ex11 2021
# DESCRIPTION: This program 'builds' a diagnosis tree.
########################################################

import itertools


class Node:
    """ This class creates a node in the tree. Each node has a data and can
        have positive child and negative child (if it doesn't have children
        their value will be None). """
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child


class Record:
    """ This cass creates records. Each record object has an illness and its
        list of symptoms."""
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    """ This function gets a filepath (the file contains patients illness
        and symptoms) and returns a list of Records objects"""
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    """ This class diagnose illness by traveling the tree it gets. """
    def __init__(self, root):
        self.root = root

    def __rec_diagnose(self, symptoms, root):
        """ This recursive function gets a list of symptoms and a root to
            check,and returns the diagnosis. It goes over the symptoms list
            and checks whether the symptoms are in the nodes data, if they
            are it continues to the positive child and if not to the negative
            then calls itself recursively until the root it checks is a leaf
            and that's the diagnosis - the function returns the
            leaf. """
        if root.positive_child is None and root.negative_child is None:
            return root.data

        for s in range(len(symptoms)):
            if symptoms[s] in root.data:
                res = self.__rec_diagnose(symptoms[:], root.positive_child)
                return res

        res = self.__rec_diagnose(symptoms[:], root.negative_child)
        return res

    def diagnose(self, symptoms):
        """ This method gets a list of symptoms and returns the diagnosis.
            It calls the rec_diagnose helper method to get the diagnosis and
            returns it. """
        return self.__rec_diagnose(symptoms, self.root)

    def calculate_success_rate(self, records):
        """ This method gets a list of records and calculates the success
            rate of the tree to diagnose the illness. If the list is empty
            the function will raise Value Error."""
        if len(records) == 0:
            raise ValueError("Got no records!")
        else:
            counter = 0
            for record in records:
                diagnosis = self.diagnose(record.symptoms)
                if diagnosis == record.illness:
                    counter += 1
            return counter / len(records)

    def __rec_all_illness(self, root, lst_illness):
        """ This recursive function returns a list with all the leaves in the
            tree- all the illness. It goes over all the nodes of the tree-
            first all the positives then all the negatives. When it gets to
            a leaf, it adds the leaf data (if its not None) to a list and
            returns to continue the process. Finally it returns a list that
            contains all the illnesses. """
        if root.positive_child is None and root.negative_child is None:
            if root.data is not None:
                lst_illness.append(root.data)
            return lst_illness

        self.__rec_all_illness(root.positive_child, lst_illness)
        self.__rec_all_illness(root.negative_child, lst_illness)

        return lst_illness

    def all_illnesses(self):
        """ This function calls the rec_all_illness function to get the list
            of all the leaves in the tree. Then it sorts it by its
            frequency in the list (reversed-from high to low) and removes
            duplicates. Finally it returns the organized final list."""
        lst_illness = self.__rec_all_illness(self.root, [])
        lst_sorted = sorted(lst_illness, key=lambda x: -lst_illness.count(x))
        lst_no_duplicates = [illness for i, illness in enumerate(lst_sorted)
                             if illness not in lst_sorted[:i]]
        return lst_no_duplicates

    def __rec_path_to_illness(self, root, illness, moves_lst, final_lst):
        """ This recursive function search for illness in the tree and returns
            a list of lists that contains all the possible paths to the
            wanted illness. First, it checks if the current root is a leaf -
            if it is checks if its data is the given illness string - if
            it is it appends the moves_lst to the final list. If the
            current root is not a leaf, it appends True to the moves_lst and
            call itself recursively with the root being the positive child,
            then pop the True from the list and appends False instead and
            again calls itself recursively and pop it. Finally it returns the
            final list."""
        if root.positive_child is None and root.negative_child is None:
            if root.data == illness:
                final_lst.append(moves_lst[:])
            return final_lst

        moves_lst.append(True)
        self.__rec_path_to_illness(root.positive_child, illness, moves_lst,
                                   final_lst)
        moves_lst.pop()
        moves_lst.append(False)
        self.__rec_path_to_illness(root.negative_child, illness, moves_lst,
                                   final_lst)
        moves_lst.pop()
        return final_lst

    def paths_to_illness(self, illness):
        """ This function calls and returns the rec_path_to_illness function
            that returns a list with all possible paths to get to the leaf of
            the given illness. """
        return self.__rec_path_to_illness(self.root, illness, [], [])

    def __identical_trees(self, pos_tree, neg_tree):
        """ This recursive function gets the positive child and the
            negative child as parameters. It compares them and returns True if
            they are identical and False if not. If both are None- returns
            True, if both not None, checks if their data is the same, the
            positive children are the same and the negative children are the
            same (by calling itself recursively) and returns the boolean,
            and if they different- one None and one not returns False. """
        if pos_tree is None and neg_tree is None:
            return True

        if pos_tree is not None and neg_tree is not None:
            return ((pos_tree.data == neg_tree.data) and
                    self.__identical_trees(pos_tree.positive_child,
                                           neg_tree.positive_child)
                    and
                    self.__identical_trees(pos_tree.negative_child,
                                           neg_tree.negative_child))

        return False

    def __remove_empty_false(self, root):
        """ This recursive function removes all the duplicates subtrees from
            the tree. It travels the tree until it gets to a leaf,
            then returns back to its father. It calls the identical_trees
            function to check if the children of the father are identical,
            if they are- the function changes the father root to be one of
            its children. """
        if root.positive_child is None and root.negative_child is None:
            return root

        if root.positive_child:
            root_positive_child_new = self.__remove_empty_false(
                root.positive_child)
            root.positive_child = root_positive_child_new
        if root.negative_child:
            root_negative_child_new = self.__remove_empty_false(
                root.negative_child)
            root.negative_child = root_negative_child_new

        if self.__identical_trees(root.positive_child, root.negative_child):
            root = root.positive_child

        return root

    def __remove_empty_true(self, root):
        """ This recursive function removes all the Nones from the tree.
            It travels the tree until it gets to a leaf then returns to its
            'father' and checks if one of the children is None - if it is it
            changes the root to be the other child and returns. """
        if root.positive_child is None and root.negative_child is None:
            return root

        if root.positive_child:
            root_positive_child_new = self.__remove_empty_true(
                root.positive_child)
            root.positive_child = root_positive_child_new
        if root.negative_child:
            root_negative_child_new = self.__remove_empty_true(
                root.negative_child)
            root.negative_child = root_negative_child_new

        if root.positive_child.data is None:
            root = root.negative_child
        elif root.negative_child.data is None:
            root = root.positive_child
        return root

    def minimize(self, remove_empty=False):
        """ This function minimize the tree according to the remove empty
            value. if its False it will remove the duplicate subtrees (if
            there are any) and if true it will also remove all the Nones
            from tree. """
        if not remove_empty:
            self.root = self.__remove_empty_false(self.root)
        elif remove_empty:
            self.root = self.__remove_empty_true(self.root)
            self.root = self.__remove_empty_false(self.root)

        else:
            return self.root


def __diagnose_illness(records, pos_cur_symptoms, neg_cur_symptoms):
    """ This function decides which illness will be diagnosed for the
        symptoms in the pos_cur_symptoms (and contains none of the symptoms
        in the neg_cur_symptoms list). It checks for each record in
        the records if the illness symptoms match the wanted symptoms and
        adds to the dict_count_illness the name of the illness and the
        number of times it matched the symptoms. In the end the function
        returns the illness that most suits the symptoms (with the maximum
        value) or if nothing was found returns None. """
    dict_count_illness = {}
    for record in records:
        for symptom in pos_cur_symptoms:
            if symptom not in record.symptoms:
                break
        else:
            for symp in neg_cur_symptoms:
                if symp in record.symptoms:
                    break
            else:
                if record.illness not in dict_count_illness:
                    dict_count_illness[record.illness] = 1
                else:
                    dict_count_illness[record.illness] += 1
    if dict_count_illness == {}:
        return None
    else:
        return max(dict_count_illness, key=lambda k: dict_count_illness[k])


def __rec_build_tree(records, symptoms, index, pos_cur_symptoms,
                     neg_cur_symptoms, root_data):
    """ This recursive function 'creates a tree' in which every depth
        the Nodes are items from the symptoms list (same item in every
        depth), and the leaves are illness from the records list that suit
        the symptoms the most. When it gets to a leaf it calls the
        diagnose_illness function to decide which illness will be in
        the leaf. Each time it gets to a positive child it adds its data to
        the pos_cur_symptoms list and when it gets to a negative child it
        adds it to the neg_cur_symptoms list. That is how it keeps track on
        the symptoms and it helps to diagnose the illness later. """
    if index >= len(symptoms):  # that's  a leaf
        illness = __diagnose_illness(records, pos_cur_symptoms,
                                     neg_cur_symptoms)
        return Node(illness, None, None)

    pos_cur_symptoms.append(root_data)
    if index + 1 >= len(symptoms):
        next_root_data = ""
    else:
        next_root_data = symptoms[index + 1]

    positive_root = __rec_build_tree(records, symptoms, index + 1,
                                     pos_cur_symptoms, neg_cur_symptoms,
                                     next_root_data)
    pos_cur_symptoms.pop()

    neg_cur_symptoms.append(root_data)
    negative_root = __rec_build_tree(records, symptoms, index + 1,
                                     pos_cur_symptoms, neg_cur_symptoms,
                                     next_root_data)
    neg_cur_symptoms.pop()

    root = Node(symptoms[index], positive_root, negative_root)
    return root


def __check_valid_type(records, symptoms):
    """ This function goes over the records and symptoms lists and checks if
        one of the items in the lists are not a record object or string- if
        they aren't returns False else True. """
    for record in records:
        if type(record) != Record:
            return False, "records"
    for symptom in symptoms:
        if type(symptom) != str:
            return False, "symptoms"
    return True, True


def build_tree(records, symptoms):
    """ This function builds a tree of the given symptoms and returns a
        Diagnoser object for it. First the function checks the types by
        calling the check_valid_type function, if that function returns
        False,it raise a TypeError. Otherwise the function creates
        a tree by calling the function rec_build_tree and returns a
        Diagnoser object of it. """
    valid_input, param = __check_valid_type(records, symptoms)
    if not valid_input:
        if param == "records":
            raise TypeError("Got wrong type for records!")
        elif param == "symptoms":
            raise TypeError("Got wrong type for symptoms!")

    if not symptoms:
        return Diagnoser(Node(__diagnose_illness(records, [], []), None, None))

    root = __rec_build_tree(records, symptoms, 0, [], [], symptoms[0])

    return Diagnoser(root)


def __double_symptoms(symptoms):
    """ This function checks if one of the symptoms in the symptoms list
        repeats itself. If it is returns True if not- False """
    for symp in symptoms:
        if symptoms.count(symp) > 1:
            return True
    return False


def optimal_tree(records, symptoms, depth):
    """ This function returns Diagnoser object for the tree with the maximum
        success rate of the wanted depth. First it checks if the depth is 0-
        calls build_tree with the records and an empty list - it returns a
        Diagnoser with None leaf only. It also checks if the parameters are
        valid(with the help of double_symptoms function) if not it raises an
        exception- ValueError. Otherwise- the function creates a list that
        contains all the subsets of the symptoms list in the size of depth
        with itertools.combinations. Then for each subset it builds a tree
        by calling the build_tree function, it calculates its success rate
        with calculate_success_rate method and adds to the dict_success_rate
        the tree and its success rate. Finally it returns the key of the
        dict (Diagnoser object) with the maximum value (the maximum success
        rate). """
    if depth == 0:
        return build_tree(records, [])
    if not depth >= 0 or not depth <= len(symptoms):
        raise ValueError("got invalid Value of depth")
    elif __double_symptoms(symptoms):
        raise ValueError("got invalid Value of symptoms")

    subs_symp_list = list(itertools.combinations(symptoms, depth))
    dict_success_rate = {}
    for sub in subs_symp_list:
        tree = build_tree(records, sub)
        success_rate = tree.calculate_success_rate(records)
        dict_success_rate[tree] = success_rate
    return max(dict_success_rate, key=lambda k: dict_success_rate[k])
