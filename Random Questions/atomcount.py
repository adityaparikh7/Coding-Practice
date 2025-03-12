from collections import defaultdict

def count_of_atoms(formula):
    def parse(s, i):
        counts = defaultdict(int)
        n = len(s)

        while i < n:
            if s[i].isalpha():
                # Start of an atom name
                start = i
                while i + 1 < n and s[i + 1].islower():
                    i += 1
                atom = s[start:i + 1]

                # Count the number of atoms (default is 1)
                num_start = i + 1
                while i + 1 < n and s[i + 1].isdigit():
                    i += 1
                count = int(s[num_start:i + 1]) if num_start <= i else 1

                counts[atom] += count

            elif s[i] == '(':
                # Start of a group (sub-formula)
                inner_counts, j = parse(s, i + 1)

                # Count the number of groups
                num_start = j + 1
                while j + 1 < n and s[j + 1].isdigit():
                    j += 1
                multiplier = int(s[num_start:j + 1]) if num_start <= j else 1

                for atom, count in inner_counts.items():
                    counts[atom] += count * multiplier

                i = j  # Update i to the position after the closing parenthesis

            elif s[i] == ')':
                # End of a group (sub-formula)
                return counts, i

            i += 1

        return counts

    result = parse(formula, 0)

    # # Sort the atoms alphabetically and format the output
    for atom, count in sorted(result.items()):
        print(f"{atom}: {count}")



# Example usage:
# formula = "K4(ON(SO3)2)2"
formula = input("Enter the formula: ")
print(count_of_atoms(formula))  # Output: "K4N2O14S4"