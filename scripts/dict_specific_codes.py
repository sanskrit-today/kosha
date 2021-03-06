import codecs
import sys
import re
from indic_transliteration.sanscript import transliterate

def convert_shashvatakosha(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    for line in fin:
        output = ''
        line = line.rstrip()
        if line.startswith('#'):
            line = line.lstrip('#')
            parts = line.split(';')
            for part in parts:
                print(part)
                headword, count = part.split(',')
                count = int(transliterate(count, 'devanagari', 'slp1'))
                output += '$' + headword + ';\n'
                output += '#' + ','.join(['' for i in range(count)]) + '\n'
            fout.write(output)
        elif ';{p0' in line:
            fout.write(line.replace(';{p0', ';p{0') + '\n')
        else:
            fout.write(line + '\n')

def remove_footnotes_from_anekarthatilaka(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    writeToFile = True
    for line in fin:
        if '{{' in line:
            writeToFile = False
        if writeToFile:
            fout.write(line)
        if '}}' in line:
            writeToFile = True
    fin.close()
    fout.close()

def verse_num_anekarthasangraha(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    verseNum = '0'
    for line in fin:
        m = re.search('([0-9]+)\n', line)
        if m:
            verseNum = m.group(1)
        elif '॥' in line:
            line = line.rstrip()
            line = line + ' ' + verseNum + ' ' + '॥\n'
            fout.write(line)
        else:
            fout.write(line)
    fin.close()
    fout.close()

def verse_num_kriyanighantu(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    verseNum = '0'
    output = ''
    for line in fin:
        m = re.search('^([०१२३४५६७८९]+)[. ]+([^\n]+)\n', line)
        m1 = re.search('^([^\n]+)\(([०१२३४५६७८९]+)\)\n', line)
        if m:
            output += m.group(2) + ' ' + m.group(1) + ' ॥\n'
        elif m1:
            output += m1.group(1) + m1.group(2) + ' ॥\n'
        else:
            output += line
    output = re.sub('([^ ])([।॥])', '\g<1> \g<2>', output)
    output = re.sub('।[ ]*', '।\n', output)
    fout.write(output)
    fin.close()
    fout.close()

def adjust_nanarthamanjari(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    output = ''
    for line in fin:
        m = re.search('^P', line)
        m1 = re.search('^([^l]+)(l\{[0-9]+\})', line)
        m2 = re.search('^[\t]+(.*)\n', line)
        if m:
            output += line.replace('P', ';p')
        elif m1:
            output += ';' + m1.group(2) + '\n' + m1.group(1).rstrip() + '\n'
        elif m2:
            output += ';c{' + m2.group(1) + '}\n'
        else:
            output += line
    fout.write(output)
    fin.close()
    fout.close()

#convert_shashvatakosha('../anekarthasamuchchaya_shashvata/orig/anekarthasamuchchaya_old.txt', '../anekarthasamuchchaya_shashvata/orig/anekarthasamuchchaya.txt')
#remove_footnotes_from_anekarthatilaka('../anekarthatilaka_mahipa/orig/anekarthatilaka_with_uncorrected_footnotes.txt', '../anekarthatilaka_mahipa/orig/anekarthatilaka.txt')
#verse_num_anekarthasangraha('../anekarthasangraha_hemachandra/orig/anekarthasangraha.txt', '../anekarthasangraha_hemachandra/orig/anekarthasangraha_bad.txt')
#verse_num_kriyanighantu('../kriyanighantu_virapandya/orig/kriyanighantu.txt', '../kriyanighantu_virapandya/orig/kriyanighantu1.txt')
#verse_num_kriyanighantu('../dvirupadikosha_shriharsha/orig/dvirupadikosha.txt', '../dvirupadikosha_shriharsha/orig/dvirupadikosha1.txt')
adjust_nanarthamanjari('../nanarthamanjari_raghava/orig/nanarthamanjari_proofread.txt', '../nanarthamanjari_raghava/orig/nanarthamanjari2.txt')
