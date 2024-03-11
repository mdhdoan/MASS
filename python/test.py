import pandas as pd
import sys

if __name__ == '__main__':
    file_name = sys.argv[1]
    ontology = pd.read_excel(file_name, index_col = 0)
    print(list(ontology))
