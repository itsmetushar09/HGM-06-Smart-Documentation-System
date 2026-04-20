def extract_title(markdown):

    lines = markdown.split("\n")

    for line in lines:

        if line.startswith("# "):
            return line.replace("# ", "").strip()

    return "Untitled"