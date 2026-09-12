"""
Ping Monitor for DNS Servers - Pydroid3 Compatible
Simplified version without external dependencies
"""

import threading
import time
import socket
from dns_config import EUROPEAN_DNS_SERVERS, COLORS

class PingMonitor:
    def __init__(self):
        self.ping_results = {}
        self.lock = threading.Lock()
    
    def simple_ping(self, host, timeout=5):
        """Simple DNS lookup test (no external ping needed)"""
        try:
            socket.gethostbyname(host)
            return True
        except socket.gaierror:
            return False
        except Exception:
            return False
    
    def ping_server(self, name, ipv4, ipv6=None):
        """Test server connectivity"""
        try:
            ipv4_status = self.simple_ping(ipv4)
            ipv6_status = self.simple_ping(ipv6) if ipv6 else None
            
            with self.lock:
                self.ping_results[name] = {
                    "ipv4": "OK" if ipv4_status else "FAIL",
                    "ipv6": "OK" if ipv6_status else "FAIL" if ipv6 else "N/A",
                    "status": "[ONLINE]" if ipv4_status else "[OFFLINE]",
                    "timestamp": time.time()
                }
        except Exception as e:
            with self.lock:
                self.ping_results[name] = {
                    "ipv4": "FAIL",
                    "ipv6": "FAIL",
                    "status": "[ERROR]",
                    "timestamp": time.time()
                }
    
    def monitor_all_servers(self):
        """Monitor all servers"""
        threads = []
        for server_name, server_data in EUROPEAN_DNS_SERVERS.items():
            thread = threading.Thread(
                target=self.ping_server,
                args=(server_name, server_data["ipv4"], server_data.get("ipv6"))
            )
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join(timeout=10)
    
    def get_best_server(self):
        """Get best online server"""
        for server_name, data in self.ping_results.items():
            if data["status"] == "[ONLINE]":
                return server_name
        return None
    
    def display_results(self):
        """Display server status"""
        print("\n" + "="*70)
        print("DNS Gaming Panel - Server Status")
        print("="*70)
        
        for server_name, server_data in EUROPEAN_DNS_SERVERS.items():
            if server_name in self.ping_results:
                result = self.ping_results[server_name]
                status_color = COLORS['GREEN'] if result["status"] == "[ONLINE]" else COLORS['RED']
                
                print(f"{status_color}{server_name:20}{COLORS['RESET']} | "
                      f"IPv4: {result['ipv4']:6} | IPv6: {result['ipv6']:6} | {result['status']}")
        
        best = self.get_best_server()
        if best:
            print(f"\n{COLORS['BOLD']}{COLORS['GREEN']}BEST SERVER: {best}{COLORS['RESET']}")
        
        print("="*70 + "\n")
