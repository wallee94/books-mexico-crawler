import json
import os


def build_dbook():
    websites = ["gandhi.com.mx", "casadelibro.com.mx", "educal.com.mx", "gonvill.com.mx"]
    dbook = {}
    for website in websites:
        f = open(os.path.join(os.getcwd(), "results/" + website + ".jl"), "r")
        for line in f:
            # d is the new item
            d = json.loads(line)

            isbn = d.get("ISBN")
            title = d.get("title")
            edit = d.get("editorial")
            author = d.get("author")
            content = d.get("content")

            if not isbn:
                continue

            if isbn in dbook:
                # if isbn is already saved in dbook
                dbook[isbn]["libraries"][website] = {
                    "price": d.get("price"),
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
                        "price": d.get("price"),
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
    print_dbook(dbook)
