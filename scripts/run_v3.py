from scripts.run_version import main
if __name__=='__main__':
 import sys
 sys.argv=[sys.argv[0],'v3']+sys.argv[1:]
 main()
