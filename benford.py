"""Check conformance of numerical data to Benford's Law."""
import sys
import math
from collections import defaultdict, OrderedDict
import numpy as np
import matplotlib.pyplot as plt

# Benford's Law percentages for leading digits 1-9
BENFORD = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]

def load_data():
    """Open a text file & turn contents into a list of strings."""
    count = 0
    while count <= 5:
        try:
            file_name = input("\nName of file with COUNT data: ")
            with open(file_name) as f:
                lines = f.read().strip().split('\n')
                return lines
        except IOError as ioerr:
            print("Unable to open the file", file_name, ioerr, file=sys.stderr)
            count += 1
    print("\nEnough! Stop and check file name. Terminating.")
    sys.exit(1)

def count_first_digits(data):
    """Count 1st digits and return lists of counts & frequency."""
    first_digits = defaultdict(int)
    for sample in data:
        if sample.startswith('0') or '.' in sample or not sample.isdigit():
            print("\nBad sample = {}".format(sample), file=sys.stderr)
            print("Data should be integer counts only.", file=sys.stderr)
            print("Invalid data detected. Exiting program.\n", file=sys.stderr)
            sys.exit(1)
        else:
            first_digits[sample[0]] += 1
    ordered_digits = OrderedDict(sorted(first_digits.items()))
    data_count = [v for v in ordered_digits.values()]
    total_count = sum(data_count)
    data_pct = [(i / total_count) * 100 for i in data_count]
    return data_count, data_pct, total_count

def get_expected_counts(data_count, total_count):
    """Calculate theoretical Benford's Law count for a total sample count."""
    expected_probs = [i / 100 for i in BENFORD]
    expected_counts = []
    for i in expected_probs:
        count = int(i * total_count)
        expected_counts.append(count)
    return expected_counts

def chi_square(data_count, expected_counts):
    """Calculate Chi Square goodness-of-fit to Benford distribution."""
    chi_square_stat = 0  # Chi Square test statistic
    for i in range(0, 9):
        chi_square1 = (math.pow(data_count[i] - expected_counts[i], 2))
        chi_square2 = chi_square1 / expected_counts[i]
        chi_square_stat += chi_square2
    print("\nChi-squared Test Statistic = {:.3f}".format(chi_square_stat))
    print("Critical value at a P-value of 0.05 is 15.51.")
    
    # chi_square value corresponding to 0.05 P-value for 8 degrees of freedom:
    return chi_square_stat < 15.51

def bar_chart(data_pct):
    """Make bar chart of observed vs expected 1st digit frequency in percent."""
    fig, ax = plt.subplots()

    index = np.arange(len(data_pct))  # 1st digits for x-axis

    # text for labels, title and ticks
    fig.canvas.set_window_title('Percentage First Digits')
    ax.set_title('Data vs. Benford Values', fontsize=15)
    ax.set_ylabel('Frequency (%)', fontsize=16)
    ax.set_xticks(index)
    ax.set_xticklabels(index + 1, fontsize=14)

    # build bars    
    rects = ax.bar(index, data_pct, width=0.95, color='black', label='Data')

    def autolabel(rects):
        """Attach a text label above each bar displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2, height,
                    '{:0.1f}'.format(height), ha='center', va='bottom', 
                    fontsize=13)

    autolabel(rects)

    # plot Benford values as red dots
    ax.scatter(index, BENFORD, s=150, c='red', zorder=2, label='Benford')

    # Hide the right and top spines & add legend
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend(prop={'size':15}, frameon=False)
    
    plt.show()

def main():
    """Call functions and print stats."""
    data = load_data()
    data_count, data_pct, total_count = count_first_digits(data)
    expected_counts = get_expected_counts(data_count, total_count)
    print("\nobserved counts = {}".format(data_count))
    print("expected counts = {}".format(expected_counts, "\n"))
    print("\nFirst Digit Probabilities:")
    for i in range(1, 10):
        print("{}: observed: {:.3f}  expected: {:.3f}".
              format(i, data_pct[i - 1] / 100, BENFORD[i - 1] / 100))

    if chi_square(data_count, expected_counts):
        print("Observed distribution matches expected distribution.")
    else:
        print("Observed distribution does not match expected.", file=sys.stderr)       

    bar_chart(data_pct)    
        
if __name__ == '__main__':
    main()
