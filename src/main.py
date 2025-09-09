import argparse
from Scorer import calculate_scores  # replace scoring_module with the actual filename of your scoring functions, without .py

def main(gs_file, test_file):
    """
    Calls the scoring function to compute precision, recall, F1, and coverage.
    Prints the F1 score.
    """
    dict_d = calculate_scores(gs_file, test_file)
    if dict_d is not None:
        print("\nFinished scoring.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute F1 score for two key files.")
    parser.add_argument("--gold_file", help="Path to the gold standard file")
    parser.add_argument("--test_file", help="Path to the system output file")
    
    args = parser.parse_args()
    
    main(args.gold_file, args.test_file)