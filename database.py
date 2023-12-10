import time

locationData = {
    "seattle": [5, 3, 0, 6, 8, 0],
    "portland": [0, 0, 3, 0, 4, 10, 7],
    "reno": [0, 1, 0, 2, 2],
    "burns": [1, 9, 3, 28, 1, 0, 0]
}

def main():
    while True:
        time.sleep(1)
        f = open("branch-booking.txt", "r")
        n = f.read()
        if n == "valid" or n == "invalid" or n == "removed":
            continue
        if n == "":
            continue
        try:
            int(n)
            continue
        except ValueError:
            pass
        f.close()
        dataCheck(n)

def dataCheck(line):
    request = line.lower().split(',')
    response = "invalid"
    try:
        location = locationData[request[0]]
    except KeyError:
        writeResponse(response)
        return
    if len(request) > 3:
        writeResponse(response)
        return
    
    elif len(request) == 3:
        try:
            branch = int(request[1])
            added = int(request[2])
        except ValueError:
            writeResponse(response)
            return
        
        location[branch] =+ added
        response = "removed"

    elif len(request) == 2:
        try:
            branch = int(request[1])
        except ValueError:
            writeResponse(response)
            return
        vacancy = 0
        try:
            vacancy = location[branch]
        except IndexError:
            pass

        if vacancy != 0:
            location[branch] -= 1
            response = "valid"

    elif len(request) == 1:
        for i in range(len(location)):
            if location[i] != 0:
                response = i
                break
        
    writeResponse(response)
    return
    

def writeResponse(resp):
    f = open("branch-booking.txt", "w")
    f.write(str(resp))
    f.close()
    return
            
if __name__ == "__main__":
    main()
