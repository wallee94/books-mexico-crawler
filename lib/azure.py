import os
import json


def build_urls_from_azure(output_filename="output_file.txt", sub_folder=""):
    output_file = open(output_filename, "w")
    files_path = os.path.join(os.getcwd(), sub_folder)
    for filename in os.listdir(files_path):
        with open(os.path.join(files_path, filename), "r") as file:
            for line in file:
                try:
                    url_obj = json.loads(line)
                    url = url_obj.get("url")
                    if url:
                        output_file.write(url + "\n")
                except:
                    print("ERROR in file [%s] trying to decode: [%s]" % (filename, line))
    output_file.close()


if __name__ == "__main__":
    build_urls_from_azure()