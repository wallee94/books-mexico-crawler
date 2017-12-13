import json
import os


def build_dbook():
    websites = ["gandhi", "casadelibro", "educal", "gonvill"]
    dbook = {}
    for website in websites:
        f = open(os.path.join(os.getcwd(), website + ".com.mx.jl"), "r")
        for line in f:
            # d is the new item
            d = json.loads(line)

            if not d.get("ISBN") or not d.get("price"):
                continue

            isbn = str(int(d.get("ISBN")))  # clean left zeros
            title = d.get("title")
            edit = d.get("editorial")
            author = d.get("author")
            content = d.get("content")
            price = float(d.get("price"))

            if isbn in dbook:
                # if isbn is already saved in dbook
                if len(d.get("content")) > len(dbook[isbn]["content"]):
                    dbook[isbn]["content"] = d.get("content")

                if not dbook[isbn]["edit"]:
                    dbook[isbn]["edit"] = d.get("edit")

                if not dbook[isbn]["title"]:
                    dbook[isbn]["title"] = d.get("title")

                if not dbook[isbn]["author"]:
                    dbook[isbn]["author"] = d.get("author")

                elif d.get("author") and "," not in d.get("author") and "," in dbook[isbn]["author"]:
                    dbook[isbn]["content"] = d.get("author")

                dbook[isbn]["libraries"][website] = {
                    "price": price,
                    "url": d.get("url"),
                }

            else:
                dbook[isbn] = {
                    "title": title,
                    "edit": edit,
                    "author": author,
                    "content": content,
                }
                dbook[isbn]["libraries"] = {
                    website: {
                        "price": price,
                        "url": d.get("url"),
                    }
                }

    return dbook


def print_dbook(dbook):
    counter = 0
    for isbn in dbook:
        if len(dbook[isbn]["libraries"]) > 1:
            print(dbook[isbn])
            counter += 1
            if counter > 3:
                break


def save_dbook(filename, dbook):
    with open(filename + ".txt", "w") as f:
        f.write(json.dumps(dbook))


if __name__ == "__main__":
    dbook = build_dbook()
    with open("isbn.txt", "w") as f:
        for isbn in dbook:
            if isbn:
                f.write(isbn + "\n")