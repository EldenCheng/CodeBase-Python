import csv

if __name__ == '__main__':
    title_row = ["ID", "PW"]
    first_row = ["A", "1"]
    other_rows = [["B", "2"], ["C", "3"], ["D", "4"]]
    with open("write_test.csv", 'a+', encoding='utf-8', newline='') as f:
        writer_obj = csv.writer(f)
        writer_obj.writerow(title_row)
        writer_obj.writerow(first_row)
        writer_obj.writerows(other_rows)
        f.close()

