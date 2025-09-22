import asyncio
import logging
from src.core import ProScannerCore
from src.utils.cli_utils import (
    print_banner,
    print_results,
    setup_logging,
    Colors
)
import json

async def interactive_menu():
    """
    Displays an interactive menu for the user.
    """
    scanner = ProScannerCore()
    
    while True:
        print(f"\n{Colors.BOLD}{Colors.GRAD1}Menu:{Colors.RESET}")
        print(f"{Colors.CYAN}1. Scan a single username{Colors.RESET}")
        print(f"{Colors.CYAN}2. Scan usernames from a file{Colors.RESET}")
        print(f"{Colors.CYAN}3. Exit{Colors.RESET}")
        
        choice = input(f"\n{Colors.PURPLE}Enter your choice (1-3): {Colors.RESET}").strip()
        
        if choice == '1':
            username = input(f"{Colors.YELLOW}Enter the username to scan: {Colors.RESET}").strip()
            if username:
                logging.info(f"Scanning single user: @{username}")
                results = await scanner.scan_username(username)
                print_results([results])
            else:
                print(f"{Colors.RED}❌ No username entered. Please try again.{Colors.RESET}")
                
        elif choice == '2':
            file_path = input(f"{Colors.YELLOW}Enter the path to the username file: {Colors.RESET}").strip()
            if file_path:
                try:
                    with open(file_path, 'r') as f:
                        usernames_to_scan = [line.strip() for line in f if line.strip()]
                    
                    if not usernames_to_scan:
                        print(f"{Colors.RED}❌ The file is empty.{Colors.RESET}")
                        continue
                        
                    print(f"🕵️‍♂️ Starting scan for {len(usernames_to_scan)} username(s)...")
                    
                    all_results = []
                    for user in usernames_to_scan:
                        logging.info(f"Scanning: @{user}")
                        result = await scanner.scan_username(user)
                        all_results.append(result)

                    print_results(all_results)
                    
                    # Optional: ask to save results
                    save_choice = input(f"{Colors.YELLOW}Do you want to save the results to a file? (y/n): {Colors.RESET}").lower().strip()
                    if save_choice == 'y':
                        output_file = "scan_results.json"
                        with open(output_file, "w") as f:
                            json.dump(all_results, f, indent=4)
                        print(f"{Colors.GREEN}✅ Results saved to {output_file}{Colors.RESET}")

                except FileNotFoundError:
                    print(f"{Colors.RED}❌ File not found: {file_path}{Colors.RESET}")
            else:
                print(f"{Colors.RED}❌ No file path entered. Please try again.{Colors.RESET}")
                
        elif choice == '3':
            print(f"{Colors.INFO}👋 Exiting ProScanner. Goodbye!{Colors.RESET}")
            break
            
        else:
            print(f"{Colors.RED}❌ Invalid choice. Please select 1, 2, or 3.{Colors.RESET}")

async def main():
    """
    Main entry point for the application.
    """
    setup_logging()
    print_banner()
    await interactive_menu()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Scan cancelled by user. Exiting.")
