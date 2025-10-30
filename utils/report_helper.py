"""
Report Helper
Utilities for generating and managing test reports
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from utils.logger import logger


class ReportHelper:
    """Helper class for test reporting"""
    
    def __init__(self, report_dir: str = "reports"):
        """
        Initialize report helper
        
        Args:
            report_dir: Directory for reports
        """
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True)
        self.test_results = []
        logger.debug(f"ReportHelper initialized with dir: {report_dir}")
    
    def add_test_result(self, test_name: str, status: str, 
                       duration: float = 0.0, 
                       error_message: str = None,
                       screenshot_path: str = None):
        """
        Add test result to collection
        
        Args:
            test_name: Name of the test
            status: Test status (PASSED, FAILED, SKIPPED)
            duration: Test duration in seconds
            error_message: Error message if failed
            screenshot_path: Path to screenshot if available
        """
        result = {
            'test_name': test_name,
            'status': status,
            'duration': round(duration, 2),
            'timestamp': datetime.now().isoformat(),
            'error_message': error_message,
            'screenshot': screenshot_path
        }
        self.test_results.append(result)
        logger.info(f"Added test result: {test_name} - {status}")
    
    def generate_json_report(self, filename: str = None) -> str:
        """
        Generate JSON report
        
        Args:
            filename: Report filename (optional)
        
        Returns:
            Path to generated report
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"test_report_{timestamp}.json"
        
        report_path = self.report_dir / filename
        
        report_data = {
            'summary': self._generate_summary(),
            'test_results': self.test_results,
            'generated_at': datetime.now().isoformat()
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=4)
        
        logger.info(f"JSON report generated: {report_path}")
        return str(report_path)
    
    def generate_html_summary(self, filename: str = None) -> str:
        """
        Generate HTML summary report
        
        Args:
            filename: Report filename (optional)
        
        Returns:
            Path to generated report
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"summary_{timestamp}.html"
        
        report_path = self.report_dir / filename
        summary = self._generate_summary()
        
        html_content = self._create_html_template(summary)
        
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        logger.info(f"HTML summary generated: {report_path}")
        return str(report_path)
    
    def _generate_summary(self) -> Dict[str, Any]:
        """
        Generate test summary statistics
        
        Returns:
            Dictionary with summary data
        """
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASSED')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAILED')
        skipped = sum(1 for r in self.test_results if r['status'] == 'SKIPPED')
        
        total_duration = sum(r['duration'] for r in self.test_results)
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'pass_rate': round(pass_rate, 2),
            'total_duration': round(total_duration, 2)
        }
    
    def _create_html_template(self, summary: Dict) -> str:
        """
        Create HTML template for summary report
        
        Args:
            summary: Summary statistics
        
        Returns:
            HTML string
        """
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Test Execution Summary</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            color: white;
        }}
        .stat-card.total {{ background-color: #2196F3; }}
        .stat-card.passed {{ background-color: #4CAF50; }}
        .stat-card.failed {{ background-color: #f44336; }}
        .stat-card.skipped {{ background-color: #FF9800; }}
        .stat-card.rate {{ background-color: #9C27B0; }}
        .stat-card h2 {{
            margin: 0;
            font-size: 48px;
        }}
        .stat-card p {{
            margin: 10px 0 0 0;
            font-size: 16px;
            opacity: 0.9;
        }}
        .test-list {{
            margin-top: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .status {{
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }}
        .status.passed {{ background-color: #4CAF50; color: white; }}
        .status.failed {{ background-color: #f44336; color: white; }}
        .status.skipped {{ background-color: #FF9800; color: white; }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Test Execution Summary</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary">
            <div class="stat-card total">
                <h2>{summary['total']}</h2>
                <p>Total Tests</p>
            </div>
            <div class="stat-card passed">
                <h2>{summary['passed']}</h2>
                <p>Passed</p>
            </div>
            <div class="stat-card failed">
                <h2>{summary['failed']}</h2>
                <p>Failed</p>
            </div>
            <div class="stat-card skipped">
                <h2>{summary['skipped']}</h2>
                <p>Skipped</p>
            </div>
            <div class="stat-card rate">
                <h2>{summary['pass_rate']}%</h2>
                <p>Pass Rate</p>
            </div>
        </div>
        
        <div class="test-list">
            <h2>Test Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Duration (s)</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for result in self.test_results:
            status_class = result['status'].lower()
            html += f"""
                    <tr>
                        <td>{result['test_name']}</td>
                        <td><span class="status {status_class}">{result['status']}</span></td>
                        <td>{result['duration']}</td>
                        <td>{result['timestamp']}</td>
                    </tr>
"""
        
        html += f"""
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Total Execution Time: {summary['total_duration']} seconds</p>
            <p>Selenium PyTest Framework - Automated Test Report</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def get_failed_tests(self) -> List[Dict]:
        """
        Get list of failed tests
        
        Returns:
            List of failed test results
        """
        return [r for r in self.test_results if r['status'] == 'FAILED']
    
    def get_passed_tests(self) -> List[Dict]:
        """
        Get list of passed tests
        
        Returns:
            List of passed test results
        """
        return [r for r in self.test_results if r['status'] == 'PASSED']
    
    def clear_results(self):
        """Clear collected test results"""
        self.test_results = []
        logger.info("Test results cleared")
    
    def export_to_csv(self, filename: str = None) -> str:
        """
        Export results to CSV
        
        Args:
            filename: CSV filename (optional)
        
        Returns:
            Path to CSV file
        """
        import csv
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"test_results_{timestamp}.csv"
        
        report_path = self.report_dir / filename
        
        with open(report_path, 'w', newline='') as f:
            if self.test_results:
                writer = csv.DictWriter(f, fieldnames=self.test_results[0].keys())
                writer.writeheader()
                writer.writerows(self.test_results)
        
        logger.info(f"CSV report generated: {report_path}")
        return str(report_path)


# Global instance
report_helper = ReportHelper()