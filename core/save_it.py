import os
import errno

def save_func(final_urls, outfile, domain):
    if outfile:
        filename = outfile if "/" in outfile else f"output/{outfile}"
    else:
        filename = f"output/{domain}.txt"

    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

    with open(filename, "w", encoding="utf-8") as f:
        for i in final_urls:
            f.write(i + "\n")
