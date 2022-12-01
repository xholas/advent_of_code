
def main():
    # Load input data
    with open("input_day_01.txt", "r") as file_in:
        str_in = file_in.read()

    # Trimming whitespaces is needed
    # Empty line at the end of file causes creation of empty "list of calories"
    str_in = str_in.strip()

    # Separate inventories - split by empty line (who following ends of line)
    inventories = str_in.split("\n\n")

    # For each inventory - get the sum of calories
    calories_sum_list = []
    for inventory in inventories:
        # Get items - split to separate line
        items_str = inventory.split("\n")
        # Convert strings to integer values
        items_int = [int(i) for i in items_str]
        # Sum items
        calories_sum = sum(items_int)
        # Save the sum to list
        calories_sum_list.append(calories_sum)

    # Find the Elf carrying the most Calories.
    # How many total Calories is that Elf carrying?
    # In other words: what is the biggest sum in the list?
    print(max(calories_sum_list))


if __name__ == '__main__':
    main()
