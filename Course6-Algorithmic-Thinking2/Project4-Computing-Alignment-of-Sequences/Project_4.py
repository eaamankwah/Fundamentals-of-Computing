"""
Algorithmic Thinking - Module 4
Dynamic Programming and Sequence Alignment
Computing Alginments of sequences
Project File
"""
#from collections import defaultdict 

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Creates scoring matrix using provided input.
    Input:  alphabet =  set of characters
            diag_score = score of remaining diagonal entries
            off_diag_score = score of remaining off diagonal entries
            dash_score = score for any entry indexed by 1 or more dashes
    return: scoring matrix = dictionary of dictionaries
    """
    #set initial variables
    scoring_matrix = {}
    dash = '-'
    characters = alphabet.copy()
    characters.add(dash)

    #compare set of characters against itself to build scoring matrix dictionary
    for char in characters:
        scoring_matrix[char] = {}
        for compare in characters:
            if char == dash or compare == dash:
                score = dash_score
            elif compare == char:
                score = diag_score
            else:
                score = off_diag_score
            scoring_matrix[char][compare] = score

    #return scoring matrix dictionary
    return scoring_matrix

def obtain_gap_val(seq_x, seq_y, scoring_matrix):
    """
    Calculates the gap or dash value from scoring matrix.

    input:  scoring_matrix = dictionary matrix of scores
    return: gap value (int)
    """
    dash = "-"
    row_gap, col_gap = 0, 0

    if len(seq_x) > 0:
        row_gap = scoring_matrix[dash][seq_x[0]]
    if len(seq_y) > 0:
        col_gap = scoring_matrix[dash][seq_y[0]]

    return row_gap, col_gap

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Computes and returns alignment matrix scores for sequence x and sequence y.

    input:  seq_x = sequence x string
            seq_y = sequence y string
            scoring_matrix = dictionary matrix of scores
            global_flag = boolean
    return: alignment matrix = list of lists
    """
    #set initial variables
    align_matrix = [[0]]
    dash = "-"
    gap_value = obtain_gap_val(seq_x, seq_y, scoring_matrix)
    sequence_x, sequence_y = dash + seq_x, dash + seq_y
    mval, nval = len(sequence_x), len(sequence_y)

    #compute initial rows and columns of alignment matrix
    for indx_i in range(1, mval):
        score = indx_i * gap_value[0]
        if not global_flag:
            score = max(score, 0)
        align_matrix.append([score])
    for indx_j in range(1, nval):
        score = indx_j * gap_value[1]
        if not global_flag:
            score = max(score, 0)
        align_matrix[0].append(score)

    #fill in rest of matrix comparing two sequences against each other
    for indx_i in range(1, mval):
        for indx_j in range(1, nval):
            score = max(align_matrix[indx_i - 1][indx_j - 1] + scoring_matrix[sequence_x[indx_i]][sequence_y[indx_j]],
                align_matrix[indx_i - 1][indx_j] + gap_value[0],
                align_matrix[indx_i][indx_j - 1] + gap_value[1])
            if not global_flag:
                score = max(score, 0)
            align_matrix[indx_i].append(score)

    #return alignment matrix list of lists with computed scores
    return align_matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Computes global alignment for two sequences.
    input:  seq_x = sequence x string
            seq_y = sequence y string
            scoring_matrix = dictionary matrix of scores
            alignment_matrix = global alignment matrix lists
    return: tuple of score, align_x, and align_y for global alignment
    """
    #initialize variables
    ival, jval = len(seq_x), len(seq_y)
    new_x, new_y, dash = "", "", "-"
    gap_value = obtain_gap_val(seq_x, seq_y, scoring_matrix)

    #compute global pairwise sequence
    score = alignment_matrix[ival][jval]
    while ival > 0 and jval > 0:
        current = alignment_matrix[ival][jval]
        if current == alignment_matrix[ival - 1][jval - 1] + scoring_matrix[seq_x[ival - 1]][seq_y[jval - 1]]:
            new_x = seq_x[ival - 1] + new_x
            new_y = seq_y[jval - 1] + new_y
            ival, jval = ival - 1, jval - 1
        else:
            if current == alignment_matrix[ival - 1][jval] + gap_value[0]:
                new_x = seq_x[ival - 1] + new_x
                new_y = dash + new_y
                ival = ival - 1
            else:
                new_x = dash + new_x
                new_y = seq_y[jval - 1] + new_y
                jval = jval - 1

    #if values still remain for j and i fill in gaps with dashes
    while ival > 0:
        new_x = seq_x[ival - 1] + new_x
        new_y = dash + new_y
        ival = ival - 1
    while jval > 0:
        new_x = dash + new_x
        new_y = seq_y[jval - 1] + new_y
        jval = jval - 1

    #return tuple with global pairwise score, new X sequence, new Y sequence
    return (score, new_x, new_y)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Computes local alignment for two sequences.
    input:  seq_x = sequence x string
            seq_y = sequence y string
            scoring_matrix = dictionary matrix of scores
            alignment_matrix = global alignment matrix lists
    return: tuple of score, align_x, and align_y  for local alignment
    """
    #initialize variables
    new_x, new_y, dash = "", "", "-"
    score, ival, jval = 0, 0, 0
    gap_value = obtain_gap_val(seq_x, seq_y, scoring_matrix)

    #calculate the max score and the (i, j) location of that value
    for idx_row in range(len(alignment_matrix)):
        for idx_col in range(len(alignment_matrix[0])):
            if alignment_matrix[idx_row][idx_col] > score:
                score = alignment_matrix[idx_row][idx_col]
                ival, jval = idx_row, idx_col

    #compute local pairwise sequence
    while ival > 0 and jval > 0:
        current = alignment_matrix[ival][jval]
        if current == alignment_matrix[ival - 1][jval - 1] + scoring_matrix[seq_x[ival - 1]][seq_y[jval - 1]]:
            new_x = seq_x[ival - 1] + new_x
            new_y = seq_y[jval - 1] + new_y
            ival, jval = ival - 1, jval - 1
        else:
            if current == alignment_matrix[ival - 1][jval] + gap_value[0]:
                if current > 0:
                    new_x = seq_x[ival - 1] + new_x
                    new_y = dash + new_y
                ival = ival - 1
            else:
                if current > 0:
                    new_x = dash + new_x
                    new_y = seq_y[jval - 1] + new_y
                jval = jval - 1

    #return tuple with local pairwise score, new X sequence, new Y sequence
    return (score, new_x, new_y)
