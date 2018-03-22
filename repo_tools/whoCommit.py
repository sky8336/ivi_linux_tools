#!/usr/bin/python3
import os
import sys
import optparse

dirpath_sepline="**********************************"
author_sepline="=================================="

class bcolors:
        OKPINK = '\033[95m' #pink
        OKCYANINE = '\033[96m' 
        OKBLUE = '\033[94m' #blue
        OKGREEN = '\033[92m' #green
        OKYELLOW = '\033[93m' #yellow
        OKRED = '\033[91m' #
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        def printDir(strr):
            print(bcolors.OKGREEN+strr+bcolors.ENDC)
        def printDirsep():
            print(bcolors.BOLD+bcolors.OKCYANINE +dirpath_sepline+bcolors.ENDC)
        def printAuthsep():
            print(bcolors.BOLD+author_sepline+bcolors.ENDC)
        def printFile(str):
            print(bcolors.UNDERLINE+str+bcolors.ENDC)
        def printAuthor(str):
            print(bcolors.OKBLUE+str+bcolors.ENDC)
        def printWarning(str):
            print(bcolors.OKYELLOW+str+bcolors.ENDC)
        def printComment(str):
            print(bcolors.OKCYANINE +str+bcolors.ENDC)

list_optparse = optparse.OptionParser(usage="usage: whoCommit.py -p [project path] -d [since date]")

group = list_optparse.add_option_group('Dispaly commitors options')
group.add_option('-p', '--path',
                 dest="path", 
                 help='git project location', metavar='PATH')

group.add_option('-d', '--date',
                 dest="date", 
                 help='since date', metavar='DATE')

group.add_option('-i', '--info',
                 dest="info", action="store_true", default=False,
                 help="display the short total info")

def usage():
    list_optparse.print_help()

def display_author_commit(authors, date, path):
    bcolors.printDir(path)
    bcolors.printDirsep()
    for author in authors:
     an="'"+author+"'"
     cmd = 'git log --pretty="" --since=' + date + ' --author=' + an + ' --name-only' + '|sort|uniq'
     files = os.popen(cmd).read()
     modified_files = files.split('\n')
     modified_files.remove('')
     cmd = 'git log --pretty="%ae" --since=' + date  + ' --author=' + an + '|sort|uniq'
     author_email = os.popen(cmd).read()
     author_email = author_email.strip('\n')
     bcolors.printAuthor(author + " " + "<" +author_email + ">")
     bcolors.printAuthsep()
     for mfile in modified_files:
      bcolors.printFile(path+mfile)
     print('')

def display_info(authors, date, path):
    an_num=authors.__len__()
    cmd = 'git log --pretty="" --since=' + date + ' --name-only' + '|sort|uniq'
    fstr = os.popen(cmd).read()
    mfiles = fstr.split('\n')
    mfiles.remove('')
    fnum=mfiles.__len__()
    bcolors.printDir(path)
    print(bcolors.OKCYANINE +"Since " + date + ":",an_num,"authors modified",fnum, "files"+bcolors.ENDC)
    bcolors.printDirsep()
    for author in authors:
        bcolors.printAuthor(author)
    print("")

def main(orig_args):
    opt, args = list_optparse.parse_args(orig_args)
    if args:
        list_optparse.print_usage()
        sys.exit(1)
    
    project_path=opt.path
    if not project_path:
        list_optparse.print_usage()
        sys.exit(1)
        
    since_date=opt.date
    if not since_date:
        list_optparse.print_usage()
        sys.exit(1)

    os.chdir(project_path)
    project_path = os.getcwd()

    if os.path.exists(project_path+'/.repo/manifest.xml'):
     cut_str ="|cut -d '\"' -f2"
     cmd = 'cat .repo/manifest.xml' + '|grep project' + "|awk {'print $2'}"  + cut_str
     pathes = os.popen(cmd).read()
     pathes = pathes.split('\n')
     pathes.remove('')
    else:
     print("can't find the manifest config file, find the git project directly!")
     cmd = 'find ' +project_path + ' -name "*.git"' + "|sed 's/\.git//g'"
     pathes = os.popen(cmd).read()
     pathes = pathes.split('\n')
     pathes.remove('')
     #sys.exit(0)

    if pathes.__len__() == 0:
     print("No valid git project found! ")
     sys.exit(0)

    for gdir in pathes:
        os.chdir(gdir)
        cmd = 'git log --pretty="%an" --since=' + since_date + '|sort|uniq'
        authors_str = os.popen(cmd).read()
        authors=authors_str.split("\n")
        authors.remove('')
        authors_num = authors.__len__()
        if authors_num < 1:
         bcolors.printDir(gdir)
         bcolors.printWarning("No developer commit since "+since_date)
         print("")
         os.chdir(project_path)
         continue
        else:
         if opt.info == True:
          display_info(authors,since_date,gdir)
         else:
          display_author_commit(authors,since_date,gdir)

        os.chdir(project_path)

    sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
