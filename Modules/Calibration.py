import csv
PROCESSED_IMG_PATH = "./images/processed"

def save_calibration(file_name, questions):
    print questions
    target_directory = PROCESSED_IMG_PATH + "/" + file_name
    with open(target_directory + "/calibration.csv", "w+") as csvfile:
        fieldnames = ["question_name", "page_start", "start", "page_end", "end", "criterias"]
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for question in questions:
            cur_q = questions[question]
            writer.writerow({
                'question_name': question,
                'page_start': cur_q['coord'][0][1],
                'start': cur_q['coord'][0][0],
                'page_end': cur_q['coord'][1][1],
                'end': cur_q['coord'][1][0],
                'criterias': cur_q['criterias']
            })

def load_calibration(file_name):
    result = []
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = {
                "name": row["question_name"],
                "page_start": row["page_start"],
                "x_start": row["start"],
                "page_end": row["page_end"],
                "x_end": row["end"],
                "criterias": row["criterias"].split("/")
            }
            result.append(question)
    return result
