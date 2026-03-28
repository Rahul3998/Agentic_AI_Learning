import platform
import psutil
import socket

class SystemAgent:
    def handle(self, query: str):
        query = query.lower()

        try:
            if "os" in query:
                return self.get_os_info()

            elif "cpu" in query:
                return self.get_cpu_info()

            elif "ram" in query or "memory" in query:
                return self.get_ram_info()

            elif "disk" in query:
                return self.get_disk_info()

            elif "network" in query:
                return self.get_network_info()

            elif "all" in query or "system" in query:
                return self.get_all_info()

            else:
                return "Unknown system query"

        except Exception as e:
            return f"Error: {str(e)}"

    # -------- Individual Info --------
    def get_os_info(self):
        return {
            "OS": platform.system(),
            "Version": platform.version(),
            "Release": platform.release()
        }

    def get_cpu_info(self):
        return {
            "Processor": platform.processor(),
            "Cores": psutil.cpu_count(logical=True),
            "Usage (%)": psutil.cpu_percent(interval=1)
        }

    def get_ram_info(self):
        mem = psutil.virtual_memory()
        return {
            "Total (GB)": round(mem.total / (1024**3), 2),
            "Used (GB)": round(mem.used / (1024**3), 2),
            "Usage (%)": mem.percent
        }

    def get_disk_info(self):
        disk = psutil.disk_usage('/')
        return {
            "Total (GB)": round(disk.total / (1024**3), 2),
            "Used (GB)": round(disk.used / (1024**3), 2),
            "Usage (%)": disk.percent
        }

    def get_network_info(self):
        return {
            "Hostname": socket.gethostname(),
            "IP Address": socket.gethostbyname(socket.gethostname())
        }

    def get_all_info(self):
        return {
            "OS": self.get_os_info(),
            "CPU": self.get_cpu_info(),
            "RAM": self.get_ram_info(),
            "Disk": self.get_disk_info(),
            "Network": self.get_network_info()
        }

# def main():
#     system_agent = SystemAgent()

#     print("🤖 Multi-Agent System Ready")

#     while True:
#         query = input(">> ")

#         if query.lower() == "exit":
#             break

#         # Simple routing
#         if any(word in query.lower() for word in ["add", "sub", "mul", "div", "sqrt", "sin", "cos", "tan", "log"]):
#             result = math_agent.handle(query)

#         elif any(word in query.lower() for word in ["cpu", "ram", "memory", "disk", "os", "system"]):
#             result = system_agent.handle(query)

#         else:
#             result = "I don't understand the query"

#         print("Result:", result)


# if __name__ == "__main__":
#     main()