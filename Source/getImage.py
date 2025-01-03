import time
import driver as dr

imageId = "1n6azcFuM6ssbstyYo_HXP3L5p6Nf-bor"

def main():
    start = time.time()
    service = dr.build_drive_service(False)
    im = dr.get_image(service, imageId)
    print(f"Took {time.time() - start} seconds")

if (__name__ == "__main__"):
    main()