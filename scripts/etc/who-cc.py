import sys


for line in sys.stdin:
  print (line)
sys.exit(0)
# import sys
# for line in sys.stdin:
#     sys.stdout.write(line)

for line in sys.stdin:
    print(line)

sys.exit(0)
# cat partials/raw/etc/whocc/AMRO.csv | ./scripts/etc/whocc.py

def whocc_shity_csv_stdin():
    contents = ''
    for line in sys.stdin:
        contents += line + "\n"
    return contents

def whocc_shity_csv_clean(contents):
    refs = """WHO Collaborating Centres

Global database"""
    new = "WHO Collaborating Centres Global database"
    contents = contents.replace(refs, new)
    return contents

print('started')
whocc_shity_csv_stdin()

# print(whocc_shity_csv_clean(whocc_shity_csv_stdin()))