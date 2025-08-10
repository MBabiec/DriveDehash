from PIL import Image
import driver as dr
import csv


def main():
    service = dr.build_drive_service()
    with open("data/duplicates.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for lines in reader:
            print(f"{lines[0]} | {lines[1]}")
            try:
                Image.open(dr.get_image(service, lines[1])).show()
            except:
                print(f"Image {lines[1]} not found")
            try:
                Image.open(dr.get_image(service, lines[3])).show()
            except:
                print(f"Image {lines[3]} not found")

if __name__ == "__main__":
    main()