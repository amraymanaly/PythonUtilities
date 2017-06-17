#!/usr/bin/python2
import bs4, mechanize, sys, os

br = None
options = {}
results = []

class Result:
    def __init__(self, grade, benchno):
        # POST stuff ..
        br.select_form(nr=1)
        br['grade'] = [grade]
        br['beachno'] = str(benchno)
        br.submit()
        # Extracting marks ..
        bs = bs4.BeautifulSoup(br.response().read(), 'lxml')
        info = bs.findAll('table')[4].findAll('tr')
        self.name = str(info[0].contents[3].text).strip()
        self.marks = {}
        for row in info[1:]:
            if len(row.contents) < 5: continue
            line = str(row.contents[1].text).strip()
            subject = line[:-5].rstrip()
            try:
                mark = float(row.contents[3].text)
            except:
                continue
            # bound = int(line[-3 if subject != 'Total' else -4:-1])
            # self.marks[subject] = (mark, bound)
            self.marks[subject] = mark
        # Finalizing ..
        br.back()

def help(e):
    print('%s [grade: J1 -> S2] [benchnos] [output file]' % sys.argv[0])
    sys.exit(e)

def parse_args():
    try:
        options['grade'] = {'J1': '0', 'J2': '2', 'J3': '3', 'J4': '4', 'J5': '5', 'J6': '6',
                            'M1': '7', 'M2': '8', 'M3': '9', 'S1': '10', 'S2': '11'}.get(sys.argv[1], None)
        if options['grade'] is None: raise Exception()
        options['out'] = sys.argv[-1]
        open(options['out'], 'w').close()
        options['benchs'] = [int(x) for x in list(set(sys.argv[2:-1]))]
    except:
        help(1)

def sort_results(results, keys):
    sorted_results = {}
    for key in keys:
        sorted_results[key] = sorted(results, key=lambda result: result.marks[key], reverse=True)
    return sorted_results

def html_stuff(sort):
    with open(options['out'], 'w') as f:
        for key in sort.keys():
            f.writelines('In %s:\n' % key)
            for i, o in enumerate(sort[key]):
                f.writelines('\t%02d. %s\t--->\t%f\n' % (i+1, o.name, o.marks[key]))

if __name__ == '__main__':
    parse_args()
    br = mechanize.Browser()
    br.open('http://new-sls.net/grades')
    print('Connecting ...')
    for bench in options['benchs']:
        results.append(Result(options['grade'], bench))
    html_stuff(sort_results(results, results[0].marks.keys()))
