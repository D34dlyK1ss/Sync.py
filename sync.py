import os
import shutil
import time
import logging

def synchronize_folders(source_folder, replica_folder, log_file, synchronization_interval):
    logging.basicConfig(filename=log_file, level=logging.INFO)

    while True:
        for root, dirs, files in os.walk(source_folder):
            relative_path = os.path.relpath(root, source_folder)
            replica_path = os.path.join(replica_folder, relative_path)

            if not os.path.exists(replica_path):
                os.makedirs(replica_path)

            for file in files:
                source_file = os.path.join(root, file)
                replica_file = os.path.join(replica_path, file)

                if not os.path.exists(replica_file) or os.path.getmtime(source_file) > os.path.getmtime(replica_file):
                    shutil.copy2(source_file, replica_file)
                    logging.info(f"Copied {source_file} to {replica_file}")
                    print(f"Copied {source_file} to {replica_file}")

            for replica_file in os.listdir(replica_path):
                source_file = os.path.join(root, replica_file)
                if not os.path.exists(source_file):
                    os.remove(os.path.join(replica_path, replica_file))
                    logging.info(f"Removed {os.path.join(replica_path, replica_file)}")
                    print(f"Removed {os.path.join(replica_path, replica_file)}")

        time.sleep(synchronization_interval)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Synchronize folders.')
    parser.add_argument('source_folder', type=str, help='Path to the source folder')
    parser.add_argument('replica_folder', type=str, help='Path to the replica folder')
    parser.add_argument('log_file', type=str, help='Path to the log file')
    parser.add_argument('synchronization_interval', type=int, help='Synchronization interval in seconds')

    args = parser.parse_args()

    synchronize_folders(args.source_folder, args.replica_folder, args.log_file, args.synchronization_interval)