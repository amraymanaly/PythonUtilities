#!/usr/bin/python2

# TODO:
#   1. Add Excel Spreadsheet support
#   2. Check for invalid bench numbers

import bs4, mechanize, argparse, string

br = None
options = None
results = []

class Result:
    def __init__(self, grade, benchno):
        print('Collecting %d ..' % benchno)
        # POST stuff ..
        br.select_form(nr=1)
        br['grade'] = [grade]
        br['beachno'] = str(benchno)
        br.submit()
        # Extracting marks ..
        bs = bs4.BeautifulSoup(br.response().read(), 'lxml')
        info = bs.find(attrs={'class': 'table_cc'}).findAll('tr')
        self.name = str(info[0].contents[3].text).strip()
        self.marks = {}
        for row in info[1:]:
            if len(row.contents) != 5: continue
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

def write_table(sort):
    keys = sort.keys()
    if options.fileformat == 'text':
        with options.outfile as f:
            for key in keys:
                f.write('%s:\n' % key)
                for i, o in enumerate(sort[key]):
                    f.write('\t%02d. %-40s\t--->\t%.2f\n' % (i+1, o.name, o.marks[key]))
                    if i == options.tops-1: break
    elif options.fileformat == 'html':
        with options.outfile as f:
            f.write('<link rel="stylesheet" href="tablestyle.css" /><table><tr>')
            for key in keys: f.write('<th>%s</th>' % key)
            f.write('</tr>')
            for y in range(0, options.tops):
                f.write('<tr>')
                for x in range(0, len(keys)):
                    try:
                        o = sort[keys[x]][y]
                    except IndexError:
                        continue
                    f.write('<td>%02d. %s\t<span class="mark">%.2f</span></td>' % (y+1, string.join(o.name.split()[:3]), o.marks[keys[x]]))
                f.write('</tr>')
            f.write('</table>')
    elif options.fileformat == 'excel':
        raise NotImplementedError()

def parse_args():
    parser = argparse.ArgumentParser(description="Ranks students' results", epilog='(C) 2017 -- Amr Ayman')
    parser.add_argument('grade', choices=['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'M1', 'M2', 'M3', 'S1', 'S2'], help="Student's grade. e.g: J3, M2, ..")
    parser.add_argument('outfile', help='Output file', type=argparse.FileType('w'))
    parser.add_argument('benchnos', nargs='+', type=int, help='Student bench numbers')
    parser.add_argument('-f', default='html', choices=['html', 'text', 'excel'], help='Output file format', dest='fileformat')
    parser.add_argument( '--tops', default=10, type=int, help='How many tops ?')
    options = parser.parse_args()
    options.grade = {'J1': '1', 'J2': '2', 'J3': '3', 'J4': '4', 'J5': '5', 'J6': '6', 'M1': '7', 'M2': '8', 'M3': '9', 'S1': '10', 'S2': '11'}.get(options.grade)
    return options

def sort_results(results, keys):
    sorted_results = {}
    for key in keys:
        sorted_results[key] = sorted(results, key=lambda result: result.marks[key], reverse=True)
    return sorted_results

if __name__ == '__main__':
    options = parse_args()
    br = mechanize.Browser()
    br.open('http://new-sls.net/grades')
    print('Connecting ...')
    for bench in options.benchnos:
        results.append(Result(options.grade, bench))
    write_table(sort_results(results, results[0].marks.keys()))
