# function that return a string
# cleaned from spaces and special
# characters for more efficient
# search and comparison
def clear_string(param):
    return str(param).upper().strip().replace(" ", "").replace("-", "").replace(".", "").replace(",", "")
