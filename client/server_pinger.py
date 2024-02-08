import socket
import time

def format_time(time_in_seconds):
    #Format: Day Hour:Minute:Second ab_Month Year
    return time.strftime("%d %H:%M:%S %b %Y", time.localtime(time_in_seconds))

def compute_stats(time_deltas):
    max_time = max(time_deltas)
    min_time = min(time_deltas)
    avg_time = sum(time_deltas)/len(time_deltas)

    return max_time, min_time, avg_time

address = str(input("Enter server IPv4 address: "))
port = int(input("Enter server port number: "))
print()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cs:
    
    try: 
        cs.connect((address, port))
        cs.settimeout(1)
        noResp = 0
        tds = []
        pings = 0

        for sequence_number in range(10):
            starTime = time.time()
            ping_message = f'ping {sequence_number} {format_time(starTime)}'
            cs.send(ping_message.encode())
            pings+=1

            try:
                server_message = cs.recv(2048).decode()
                print(repr(server_message))
                endTime = time.time()
                rtt = endTime - starTime
                tds.append(rtt)
                print(f"RTT: ", rtt/1000)
                
            except:
                print(f"ping {sequence_number} No Response")
                noResp += 1
        
        print(f"\nPings sent: {pings}")
        print(f"Responses: {pings-noResp}")
        print(f"Success rate: {(pings-noResp)/pings*100}%")
        if len(tds) != 0:
            stats = compute_stats(tds)
            print(f"Max RTT: {stats[0]} ms\n" +
                  f"Min RTT: {stats[1]} ms\n" +
                  f"Average RTT: {stats[2]} ms")


    except Exception as e:
        print("Connection to server failed: ", e)

    finally:
        if noResp == 10:
                print("No response from server")
        print("Closing Connection")