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

list_optparse = optparse.OptionParser(usage="usage: autoTag.py [opting]" + "\n" +
                                            "--show tags: autoTag.py -p project_dir -i"  + "\n" +
                                            "--add tags: autoTag.py -p project_dir -t v1.0"  + "\n" +
                                            "--delete tags: autoTag.py -p project_dir -d -t v1.0" )

group = list_optparse.add_option_group('Dispaly commitors options')
group.add_option('-p', '--path',
                 dest="path", 
                 help='git project location', metavar='PATH')

group.add_option('-d', '--delete',
                 dest="delete", action="store_true", default=False,
                 help='delete tag', metavar='DEL')

group.add_option('-t', '--tag',
                 dest="tag", 
                 help='tag name', metavar='TAG')

group.add_option('-i', '--info',
                 dest="info", action="store_true", default=False,
                 help="display the short total info")

def usage():
    list_optparse.print_help()

def display_info(path):
    cmd = 'git tag'
    tstr = os.popen(cmd).read()
    mtags = tstr.split('\n')
    mtags.remove('')
    bcolors.printDir(path)
    bcolors.printDirsep()
    for tag in mtags:
     bcolors.printAuthor(tag)
    print("")

def main(orig_args):
    opt, args = list_optparse.parse_args(orig_args)
    if args:
     list_optparse.print_usage()
     sys.exit(1)
    
    project_path=opt.path
    if not project_path:
     bcolors.printWarning("missing project path")
     list_optparse.print_usage()
     sys.exit(1)
        
    delete_flag=opt.delete
    tag_name=opt.tag
    if delete_flag:
     if not tag_name:
      bcolors.printWarning("missing tag")
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

    if pathes.__len__() == 0:
     bcolors.printWarning("No valid git project found! ")
     sys.exit(0)

    for gdir in pathes:
     os.chdir(gdir)
     if opt.info == True:
      display_info(gdir)
     elif opt.delete:
      cmd = 'git push origin --delete ' + tag_name 
      tag_str = os.popen(cmd).read()
      cmd = 'git tag -d ' + tag_name
      tag_str = os.popen(cmd).read()
     elif opt.tag:
      cmd = 'git tag -a ' + tag_name + ' -m "version ' + tag_name + '"'
      tag_str = os.popen(cmd).read()
      cmd = 'git push origin ' + tag_name 
      tag_str = os.popen(cmd).read()
     os.chdir(project_path) #for end

    sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
