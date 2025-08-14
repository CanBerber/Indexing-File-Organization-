#1306220069 Yunus Can Berber File Organization Term Project Spring-2024
import os
import hashlib
import time
import string

def MakeFolder():
    folders = ['Unprocessed_Passwords', 'Processed', 'Code', 'Index']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)



def IndexPass():
    IndexPath = 'Index'
    UnprocessedPath = 'Unprocessed_Passwords'

    for filename in os.listdir(UnprocessedPath):
        with open(os.path.join(UnprocessedPath, filename), 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                password = line.strip()
                IndexFolder = password[0].lower()
                IndexFolder = IndexFolder if IndexFolder in string.ascii_lowercase else 'other'

                if not os.path.exists(os.path.join(IndexPath, IndexFolder)):
                    os.makedirs(os.path.join(IndexPath, IndexFolder))

                HashedPassword = hashlib.md5(password.encode()).hexdigest()
                sha128 = hashlib.sha1(password.encode()).hexdigest()
                sha256 = hashlib.sha256(password.encode()).hexdigest()
                #Using hash values(keys) from haslib library(sha128,sha256,md5) for hashmap
                IndexFile = os.path.join(IndexPath, IndexFolder, IndexFolder + '.txt')

                with open(IndexFile, 'a',encoding='utf-8', errors='ignore') as index:
                    index.write(f"{password}|{HashedPassword}|{sha128}|{sha256}|{filename}\n")



def MoveToProcessed():
    UnprocessedPath = 'Unprocessed_Passwords'
    ProcessedPath = 'Processed'

    for filename in os.listdir(UnprocessedPath):
        source = os.path.join(UnprocessedPath, filename)
        destination = os.path.join(ProcessedPath, filename)
        os.rename(source, destination)



def SearchPassword(query):
    IndexPath = 'Index'
    query = query.strip().lower()
    IndexFolder = query[0].lower()
    IndexFolder = IndexFolder if IndexFolder in string.ascii_lowercase else 'other'

    IndexFile = os.path.join(IndexPath, IndexFolder, IndexFolder + '.txt')

    found = False
    result = []



    with open(IndexFile, 'r', encoding='utf-8', errors='ignore') as index:
        for line in index:
            parts = line.strip().split('|')
            if parts[0] == query:
                result = parts
                found = True
                break



    if not found:
        HashedPassword = hashlib.md5(query.encode()).hexdigest()
        sha128 = hashlib.sha1(query.encode()).hexdigest()
        sha256 = hashlib.sha256(query.encode()).hexdigest()
        result = [f"{query}|{HashedPassword}|{sha128}|{sha256}|search"]
        # Adding searched password to index for other searches
        with open(IndexFile, 'a', encoding='utf-8', errors='ignore') as index:
            index.write(f"{query}|{HashedPassword}|{sha128}|{sha256}|search\n")


    return result



def MeasureSearchTime():
    IndexPath = 'Index'
    totaltime = 0

    for _ in range(10):
        RandomPassword = GenerateRandomPassword()
        start = time.time()
        SearchPassword(RandomPassword)
        end = time.time()
        totaltime += end - start

    averagetime = totaltime / 10
    print("Average search time of 10 random passwords:", averagetime)



def GenerateRandomPassword():
    import random
    import string
    length = random.randint(8, 16)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))



if __name__ == "__main__":#Fixed code block
    MakeFolder()
    IndexPass()
    MoveToProcessed()
    MeasureSearchTime()
    query = input("Enter password for searching: ")
    start = time.time()
    result = SearchPassword(query)
    end = time.time()#End of the time
    print("Search result:", result)
    print("Search time:", end - start, "seconds")