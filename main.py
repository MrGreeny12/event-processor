from event_processing import process_baking_log

if __name__ == "__main__":
    input_file = "sources_dataset.csv"
    output_file = "output_dataset.csv"
    process_baking_log(input_file=input_file, output_file=output_file)
