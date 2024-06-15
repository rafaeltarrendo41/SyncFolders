import time 
import os
import shutil
import argparse
import logging


def sync_folders(source_path, replica_path):

    #creates the replica folders if it doesn't exist
    if not os.path.exists(replica_path):
        logging.info("Directory created:" + replica_path)
        os.makedirs(replica_path)

    #walks through the source folder
    for root, dirs, files in os.walk(source_path):

        #create corresponding directories in the replcia folder
        for dir in dirs:
            dir_path = os.path.join(root, dir).replace(source_path, replica_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        #create corresponding files in the replica folder
        for file in files:
            file_path = os.path.join(root, file)
            replica_file_path = file_path.replace(source_path, replica_path)
            
            #check if the file exists in the replica folder
            if os.path.exists(replica_file_path):

                #check if the file has been modified
                if os.path.getmtime(file_path) > os.path.getmtime(replica_file_path):
                    #copy the updated file
                    shutil.copy(file_path, replica_file_path)
                    logging.info("File updated: " + replica_file_path)
            else:
                #copy the new file
                shutil.copy(file_path, replica_file_path)
                logging.info("File created: " + replica_file_path)
    
    for root, dirs, files in os.walk(replica_path):
        for file in files:
            file_path = os.path.join(root, file)
            #check if the file has been deleted
            if not os.path.exists(file_path.replace(replica_path, source_path)):
                os.remove(file_path)
                logging.info("File deleted: " + file_path)
        
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            #check if the directory has been deleted
            if not os.path.exists(dir_path.replace(replica_path, source_path)):
                os.rmdir(dir_path)
                logging.info("Directory deleted: " + dir_path)


    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", help="Source folder", required=True)
    parser.add_argument("-r", "--replica", help="Replica folder", required=True)    
    parser.add_argument("-i", "--interval", help="Interval in seconds", required=True)  
    parser.add_argument("-l", "--log", help="Log File", required=True) 
    args = parser.parse_args()

    logging.basicConfig(filename=args.log, level=logging.INFO)
    
    while True:
        sync_folders(args.source, args.replica)
        time.sleep(int(args.interval))
        
if __name__ == "__main__":
    main()

# To run
# python SyncFolders.py -s SourcePath -r ReplicaPath -i Int_Interval -l LogPath
    