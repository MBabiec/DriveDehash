import hashMagic as hm
import csv

def main():

    hashes_to_check = []
    names = []
    ids = []
    duplicate_pairs = []

    with open("data/data.csv", "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            ids.append(line[0])
            names.append(line[1])
            hashes_to_check.append(line[2])

    for i in range(len(hashes_to_check)):
        for j in range(len(hashes_to_check)):
            if i != j:
                if hm.is_similar(int(hashes_to_check[i], 16), int(hashes_to_check[j], 16)):
                    # print(f"{i} {j} SIMILAR " + str(hex(int(hashes_to_check[i], 16))) + " | " + str(hex(int(hashes_to_check[j], 16))))
                    # print(f"{names[i]} | {names[j]}")
                    duplicate_pairs.append((names[i], ids[i], names[j], ids[j]))

    for pair in duplicate_pairs:
        if (pair[2], pair[3], pair[0], pair[1]) in duplicate_pairs:
            duplicate_pairs.remove((pair[2], pair[3], pair[0], pair[1]))

    with open("data/duplicates.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for pair in duplicate_pairs:
            writer.writerow(pair)
    print("Done")

if __name__ == "__main__":
    main()