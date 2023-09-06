import create_tables, import_data, query_and_export_data

def main():
    print(create_tables.create_tables())
    print(import_data.import_data())
    print(query_and_export_data.query_and_export_data())
    return "Finished processing"

if __name__=="__main__":
    main()