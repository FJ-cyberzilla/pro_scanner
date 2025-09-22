import logging
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import print as rich_print

# Initialize the rich console for all terminal output
console = Console()

class Colors:
    """
    Rich color definitions for consistent styling.
    """
    PURPLE = "purple"
    CYAN = "cyan"
    YELLOW = "yellow"
    GREEN = "green"
    RED = "red"
    GRAY = "dim white"
    BOLD = "bold"
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "green"
    FAILURE = "red"

def setup_logging():
    """Sets up basic logging to console."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] - [%(levelname)s] - %(message)s",
        datefmt="%H:%M:%S"
    )

def print_banner():
    """Prints a styled welcome banner for the application."""
    banner_text = Text(
        """
 dP""b8 Yb  dP 88""Yb 888888 88""Yb 8888P 88 88     88        db    
dP   `"  YbdP  88__dP 88__   88__dP   dP  88 88     88       dPYb   
Yb        8P   88""Yb 88""   88"Yb   dP   88 88  .o 88  .o  dP__Yb  
 YboodP  dP    88oodP 888888 88  Yb d8888 88 88ood8 88ood8 dP""""Yb 
""", style=f"{Colors.BOLD} {Colors.GREEN}"
    )
    
    powered_by_text = Text(
        "Powered by Cyberzilla™ - Osint Reconnaissance - MMXXV - V 5.1.3",
        style=f"{Colors.BOLD} {Colors.YELLOW}"
    )

    console.print(banner_text)
    console.print(powered_by_text, justify="center")

def print_results(results: list):
    """Prints scan results in a well-formatted table."""
    if not results:
        console.print(f"[bold {Colors.YELLOW}]No results to display.[/bold {Colors.YELLOW}]")
        return

    table = Table(title="[bold]Scan Results[/bold]", box=None, show_header=True)
    table.add_column("Username", style=f"{Colors.CYAN}", justify="left")
    table.add_column("Site", style="bold", justify="left")
    table.add_column("Status", justify="left")
    table.add_column("Details", style=f"{Colors.GRAY}", justify="left")

    for result in results:
        username = result.get('username', 'N/A')
        for site_result in result.get('results', []):
            site_name = site_result.get('site', 'N/A')
            status = site_result.get('status', 'N/A')
            details = site_result.get('details', {})

            status_style = {
                "FOUND": f"[bold {Colors.GREEN}]FOUND[/bold {Colors.GREEN}]",
                "NOT_FOUND": f"[bold {Colors.RED}]NOT FOUND[/bold {Colors.RED}]",
                "ERROR": f"[bold {Colors.YELLOW}]ERROR[/bold {Colors.YELLOW}]",
                "UNAVAILABLE": f"[bold {Colors.GRAY}]UNAVAILABLE[/bold {Colors.GRAY}]"
            }.get(status, status)

            details_str = ", ".join([f"{k}: [i]{v}[/i]" for k, v in details.items() if v is not None])
            
            table.add_row(username, site_name, status_style, details_str)

    console.print("\n")
    console.print(table)
