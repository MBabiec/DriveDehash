import io
import time
import driver as dr
import hashMagic as hm
import csv

def main():

    service = dr.build_drive_service()

    counter = 0

    already_done = []

    try:
        with open("data/data.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for lines in reader:
                try:
                    already_done.append(lines[0])
                except:
                    pass
    except:
        print("No data.csv file")

    with open("data/data.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)

        items, nextPageToken = dr.get_next_batch(service)

        while items and nextPageToken is not None:
            for item in items:
                itemId = item['id']
                itemName = item['name']
                if "image" in item['mimeType'] and itemId not in already_done:
                    hash = hm.calculate_hash(dr.get_image(service, itemId))
                    writer.writerow([itemId, itemName, hash])
                    print(f"{counter} {itemName} | {hash}")
                    counter += 1
                else:
                    print(f"{counter} {itemName} already done")
                    counter += 1
            items, nextPageToken = dr.get_next_batch(service, nextPageToken)

    service.close()

if __name__ == "__main__":
    main()