#!/usr/bin/python2

from __future__ import print_function
import bs4, mechanize, argparse, sqlite3, string, sys

from openpyxl import Workbook

br = None
options = None
results = set()
subjects = {}

class Result:
    def __init__(self, grade, benchno):
        p('\rCollecting %d ..' % benchno)
        # POST stuff ..
        br.select_form(nr=1)
        br['grade'] = [grade]
        br['beachno'] = str(benchno)
        br.submit()
        # Extracting marks ..
        bs = bs4.BeautifulSoup(br.response().read(), 'lxml')
        info = bs.find(attrs={'class': 'table_cc'})
        if info is None:
            raise ValueError()
        else:
            info = info.findAll('tr')

        self.name = str(info[0].contents[3].text).strip()
        if self.name == '': raise ValueError()
        n = self.name.split()[:3]
        if {'El': True, 'Al': True, 'Abdel': True, 'Abdul': True}.get(n[2], False):
            n = self.name.split()[:4]
        self.name = string.join(n)

        self.marks = {}
        for row in info[1:]:
            if len(row.contents) != 5: continue
            line = str(row.contents[1].text).strip()
            subject = line[:-5].rstrip()
            try:
                mark = float(row.contents[3].text)
            except:
                continue
            self.marks[subject] = mark
            subjects[subject] = int(line[-3 if subject != 'Total' else -4:-1])
        # Finalizing ..
        br.back()

def write_table(sort):
    for fileformat in options.fileformats:
        if fileformat == 'text':
            with options.outfile as f:
                for subject in subjects:
                    f.write('%s [%d]:\n' % (subject, subjects[subject]))
                    for i, o in enumerate(sort[subject], 1):
                        f.write('\t%02d. %-40s\t--->\t%.2f%s\n' % (i, o.name, o.marks[subject], "!!" if o.marks[subject] > subjects[subject] else ''))
                        if i == options.tops: break
        elif fileformat == 'html':
            with options.outfile as f:
                f.write('<link rel="stylesheet" href="tablestyle.css" /><table><tr>')
                for subject in subjects: f.write('<th>%s [%d]</th>' % (subject, subjects[subject]))
                f.write('</tr>')
                for y in range(0, options.tops):
                    f.write('<tr>')
                    for subject in subjects:
                        try:
                            o = sort[subject][y]
                        except IndexError:
                            f.write('<td></td>')
                            continue
                        f.write('<td><span class="rank">%02d</span>. <span class="name">%s</span><span class="mark"> %.2f%s</span></td>' % (y+1, o.name, o.marks[subject], "!!" if o.marks[subject] > subjects[subject] else ''))
                    f.write('</tr>')
                f.write('</table>')
        elif fileformat == 'excel':
            wb = Workbook()
            wsl = wb.active
            x = 1
            for subject in sort:
                wsl.merge_cells(range_string='%s [%s]' % (subject, subjects[subject]), start_row=1, end_row=1, start_column=x, end_column=x+4)
                wsl.cell(row=2, column=x, value='Rank')
                wsl.merge_cells(range_string='Name', start_row=2, end_row=2, start_column=x+1, end_column=x+2)
                wsl.cell(row=2, column=x+4, value='Mark')
                for i, o in enumerate(sort[subject], 1):
                    wsl.cell(row=i+2, column=x, value=i)
                    wsl.merge_cells(range_string=o.name, start_row=i+2, end_row=i+2, start_column=x+1, end_column=x+2)
                    wsl.cell(row=i+2, column=x+4, value=o.marks[subject])
                x += 4
            wb.save(options.outfile)
        elif fileformat == 'sqlite':
            conn = sqlite3.connect(options.outfile.name)
            c = conn.cursor()
            c.execute('create table results (subject string, rank integer(3), name string, mark float(2))')
            for subject in sort:
                for i, o in enumerate(sort[subject], 1):
                    c.execute('INSERT INTO results VALUES (?,?,?,?)', (subject, i, o.name, o.marks[subject],))
            conn.commit()
            c.close()
            conn.close()
        print('Written in %s!' % fileformat)

def parse_args():
    parser = argparse.ArgumentParser(description="Ranks students' results", epilog='(C) 2017 -- Amr Ayman')
    parser.add_argument('-g', '--grade', required=True, choices=['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'M1', 'M2', 'M3', 'S1', 'S2'], help="Student's grade. e.g: J3, M2, ..")
    parser.add_argument('-o', '--outfile', required=True, help='Output file', type=argparse.FileType('w'))
    parser.add_argument('benchnos', nargs='+', type=int, help='Student bench numbers')
    parser.add_argument('-f', default=['html'], nargs='+', choices=['html', 'text', 'excel', 'sqlite'], help='Output file format. You can specify multiple, e.g: -f html excel ..', dest='fileformats')
    parser.add_argument( '--tops', default=10, type=int, help='How many tops ?')
    options = parser.parse_args()
    options.grade = {'J1': '1', 'J2': '2', 'J3': '3', 'J4': '4', 'J5': '5', 'J6': '6', 'M1': '7', 'M2': '8', 'M3': '9', 'S1': '10', 'S2': '11'}.get(options.grade)
    if options.tops > len(options.benchnos):
        options.tops = len(options.benchnos)
    return options

def sort_results(results):
    sorted_results = {}
    for subject in subjects:
        sorted_results[subject] = sorted([res for res in results if subject in res.marks], key=lambda result: result.marks[subject], reverse=True)
        # No activity, pe shit ..
        if sorted_results[subject][0].marks[subject] == sorted_results[subject][-1].marks[subject]:
            sorted_results.pop(subject)
    return sorted_results

def p(p):
    print(p, end='')
    sys.stdout.flush()

if __name__ == '__main__':
    options = parse_args()
    br = mechanize.Browser()
    p('Connecting ...')
    br.open('http://new-sls.net/grades')
    for bench in options.benchnos:
        try:
            results.add(Result(options.grade, bench))
        except ValueError:
            print('Invalid Bench no: %s' % bench, file=sys.stderr)
    print('\rCollected All!        ')
    write_table(sort_results(results))
