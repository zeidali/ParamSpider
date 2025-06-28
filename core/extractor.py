import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)
import re

def param_extract(response, level, black_list, placeholder):
    parsed = list(set(re.findall(r'.*?:\/\/.*\?.*=[^$]', response)))
    final_uris = []

    for i in parsed:
        delim = i.find('=')
        second_delim = i.find('=', i.find('=') + 1)

        if black_list:
            words_re = re.compile("|".join(map(re.escape, black_list)))
            if not words_re.search(i):
                final_uris.append(i[:delim + 1] + placeholder)
                if level == 'high' and second_delim > delim:
                    final_uris.append(i[:second_delim + 1] + placeholder)
        else:
            final_uris.append(i[:delim + 1] + placeholder)
            if level == 'high' and second_delim > delim:
                final_uris.append(i[:second_delim + 1] + placeholder)

    return list(set(final_uris))
