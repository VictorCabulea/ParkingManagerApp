def validate_number(plate_number, VALID_ROMANIAN_REGIONS):
    split_plate_number = plate_number.split()
    if len(split_plate_number) == 4:
        if split_plate_number[0] == "RO":
            if split_plate_number[1] in VALID_ROMANIAN_REGIONS:
                if split_plate_number[2].isdigit() and (split_plate_number[3].isalpha() and len(split_plate_number[3]) == 3):
                    return True
                else:
                    return False


def read_valid_regions():
    with open("resources/valid regions/valid_romanian_regions.txt", "r") as file:
        VALID_ROMANIAN_REGIONS = [line.strip() for line in file]

    return VALID_ROMANIAN_REGIONS
